"""Audit the 18 manually reviewed pilot outputs; not a general untrusted-code sandbox.

Run with the diagnostic CrossHair environment from the repo root. Generated
modules and official test bodies must be reviewed before calling this script.
Recovered fence-only copies are separate from the strict generation metric.
"""
import argparse
import ast
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

from crosshair.condition_parser import Pep316Parser
from crosshair.fnutil import FunctionInfo


def main(args):
    tasks = {t['task_id']: t for t in map(json.loads, gzip.open(args.dataset, 'rt'))}
    run = Path(args.run)
    out = Path(args.output)
    modules = out / 'fence_only_copies'
    modules.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(run.glob('HumanEval_*.txt')):
        if path.name.endswith('.error.txt'):
            continue
        text = path.read_text()
        closed = re.fullmatch(r'\s*```(?:python|py)\s*\n(.*?)```\s*', text, re.S)
        recovered = re.fullmatch(r'\s*```(?:python|py)\s*\n(.*)', text, re.S)
        if closed:
            code, normalization = closed[1], 'remove surrounding fence'
        elif recovered and '```' not in recovered[1]:
            code, normalization = recovered[1], 'remove opening fence; closing fence absent'
        else:
            rows.append({'sample': path.stem, 'status': 'unsupported_format'})
            continue
        record = json.loads(path.with_suffix('.json').read_text())
        module_path = modules / (path.stem + '.py')
        module_path.write_text(code)
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            rows.append({'sample': path.stem, 'task_id': record['task_id'],
                         'source_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                         'strict_extraction_status': record['extraction']['status'],
                         'normalization': normalization, 'implementation_tests_pass': False,
                         'implementation_status': 'python_syntax_error',
                         'contract_parser_status': 'python_syntax_error',
                         'contract_errors': [{'line': e.lineno, 'message': str(e)}]})
            continue
        # Gate imports/top-level execution for these already manually reviewed samples.
        for node in tree.body:
            if isinstance(node, ast.Import):
                assert all(n.name in ('typing', 'math', 'itertools') for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert node.module in ('typing', 'math', 'itertools')
            elif isinstance(node, ast.If):
                # This reviewed sample has a standard doctest-only script guard.
                assert ast.unparse(node.test) == "__name__ == '__main__'"
                assert all((isinstance(n, ast.Import) and all(a.name == 'doctest' for a in n.names))
                           or (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                               and ast.unparse(n.value.func) == 'doctest.testmod') for n in node.body)
            else:
                assert isinstance(node, ast.FunctionDef) or (
                    isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str))
        task = tasks[record['task_id']]
        # Input tests are never in generation prompts; this is post-generation testing.
        # Match importing a HumanEval candidate function, not running its CLI guard.
        harness = "__name__ = 'reviewed_under_test'\n" + code + '\n' + task['test'] + '\ncheck(' + task['entry_point'] + ')\n'
        test_path = modules / (path.stem + '_tests.py')
        test_path.write_text(harness)
        tested = subprocess.run([sys.executable, '-I', str(test_path)],
                                capture_output=True, text=True, timeout=10)
        (out / (path.stem + '_test_output.txt')).write_text(tested.stdout + tested.stderr)
        name = 'reviewed_' + path.stem
        spec = importlib.util.spec_from_file_location(name, module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        conditions = Pep316Parser().get_fn_conditions(
            FunctionInfo.from_fn(getattr(mod, task['entry_point'])))
        errors = [{'line': e.line_num, 'message': e.message} for e in conditions.syntax_messages()]
        explicit_posts = [c.expr_source for c in conditions.post if c.expr_source.strip()]
        parser_status = ('syntax_error' if errors else
                         'parsed' if explicit_posts else 'missing_postcondition')
        rows.append({'sample': path.stem, 'task_id': task['task_id'],
                     'source_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                     'strict_extraction_status': record['extraction']['status'],
                     'normalization': normalization, 'implementation_tests_pass': tested.returncode == 0,
                     'contract_parser_status': parser_status,
                     'contract_errors': errors,
                     'preconditions': [c.expr_source for c in conditions.pre],
                     'postconditions': [c.expr_source for c in conditions.post],
                     'scope': 'finite official tests and contract syntax; not full correctness or mutation score'})
    result = {'samples': len(rows),
              'implementation_test_passes_after_fence_only_extraction': sum(r.get('implementation_tests_pass', False) for r in rows),
              'contract_syntax_passes_after_fence_only_extraction': sum(r.get('contract_parser_status') == 'parsed' for r in rows),
              'rows': rows}
    (out / 'reviewed_pilot_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', default='ai/runs/qwen-pilot')
    p.add_argument('--dataset', required=True)
    p.add_argument('--output', default='ai/evidence/qwen-complete')
    main(p.parse_args())
