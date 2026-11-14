"""Finite semantic probes, separate from the team's formal mutant evaluation.

Use only after reviewing the generated modules and running audit_reviewed_pilot.
No generated contracts are repaired. Canonical solutions are used only AFTER
generation to calculate reference outputs; they were never generation inputs.
"""
import argparse
import gzip
import importlib.util
import json
from pathlib import Path
import sys

from crosshair.condition_parser import Pep316Parser
from crosshair.fnutil import FunctionInfo


CASES = {
    'HumanEval/0': [([], 0.0), ([1.0], 0.0), ([0.0, 0.0], 0.0),
                    ([0.0, 0.0], 0.1), ([0.0, 1.0], 1.0),
                    ([0.0, 1.0], 1.1), ([0.0, 5.0, 0.1], 0.2),
                    ([0.0, 0.0], -1.0)],
    'HumanEval/6': [('()',), ('(())',), ('(()()) ((())) ()',),
                    ('() (())',), ('((())) ()',), ('() ()',)],
    'HumanEval/8': [([],), ([0],), ([2, 3],), ([0, 2],), ([-2, 3],), ([1, 1, 1],)],
    'HumanEval/12': [([],), ([''],), (['a', 'b'],), (['aa', 'bb', 'c'],),
                     (['a', 'ccc', 'bb'],), (['', 'x', 'x'],)],
    'HumanEval/28': [([],), ([''],), (['a', 'b'],), (['a', 'a'],),
                     (['ab', '', 'c'],), (['x', 'yz'],)],
    'HumanEval/40': [([],), ([0],), ([0, 0, 0],), ([1, 2, -3],),
                     ([1, 2, 3],), ([1, 1, -2],), ([1, 3, -2, 1],)],
}


def wrong_outputs(task, expected):
    if task in ('HumanEval/0', 'HumanEval/40'):
        choices = [not expected]
    elif task == 'HumanEval/8':
        total, product = expected
        choices = [(total, 0), (total, 1), (total, 999),
                   (total + 1, product), (product, total)]
    elif task == 'HumanEval/6':
        choices = [[], expected[::-1], [x + 1 for x in expected],
                   [0 for _ in expected], expected[:-1]]
    elif task == 'HumanEval/12':
        choices = [None, '', 'a', 'b', 'aa', 'bb', 'ccc', 'x']
    else:
        choices = ['', expected[::-1], expected + 'x', ' '.join(expected)]
    seen = set()
    for value in choices:
        if value != expected and repr(value) not in seen:
            seen.add(repr(value))
            yield value


def evaluate(clauses, bindings):
    values = []
    try:
        for clause in clauses:
            value = clause.evaluate(bindings)
            values.append({'expression': clause.expr_source, 'value_repr': repr(value), 'truth': bool(value)})
            if not bool(value):
                # The conjunction already rejects this candidate; do not evaluate
                # later index/length clauses under a false earlier guard.
                return {'holds': False, 'clauses': values, 'short_circuited': True}
        return {'holds': all(v['truth'] for v in values), 'clauses': values}
    except Exception as e:
        return {'error_type': type(e).__name__, 'error': str(e), 'clauses': values}


def main(args):
    root = Path(args.audit_directory)
    audit = json.loads((root / 'reviewed_pilot_audit.json').read_text())
    tasks = {t['task_id']: t for t in map(json.loads, gzip.open(args.dataset, 'rt'))}
    rows = []
    for record in audit['rows']:
        if record.get('contract_parser_status') != 'parsed':
            continue
        task_id, sample = record['task_id'], record['sample']
        task = tasks[task_id]
        spec = importlib.util.spec_from_file_location('probe_' + sample, root / 'fence_only_copies' / (sample + '.py'))
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        fn = getattr(mod, task['entry_point'])
        conditions = Pep316Parser().get_fn_conditions(FunctionInfo.from_fn(fn))
        reference_namespace = {}
        exec(compile(task['prompt'] + task['canonical_solution'], '<reviewed-canonical>', 'exec'), reference_namespace)
        reference = reference_namespace[task['entry_point']]
        names = list(conditions.sig.parameters)
        probes = []
        for args_tuple in CASES[task_id]:
            expected = reference(*args_tuple)
            bindings = dict(zip(names, args_tuple))
            pre = evaluate(conditions.pre, bindings)
            identity_groups = {}
            for name, value in bindings.items():
                if isinstance(value, list):
                    groups = {}
                    for index, element in enumerate(value):
                        groups.setdefault(id(element), []).append(index)
                    identity_groups[name] = [indices for indices in groups.values() if len(indices) > 1]
            probe = {'input': bindings, 'shared_object_index_groups': identity_groups,
                     'expected': expected, 'pre': pre}
            if pre.get('holds'):
                probe['reference_post'] = evaluate(conditions.post, {**bindings, '__return__': expected})
                probe['wrong_outputs'] = [{'output': wrong, 'post': evaluate(conditions.post, {**bindings, '__return__': wrong})}
                                          for wrong in wrong_outputs(task_id, expected)]
            probes.append(probe)
        pre_exclusions = [p for p in probes if p['pre'].get('holds') is False]
        false_rejections = [p for p in probes if p.get('reference_post', {}).get('holds') is False]
        missed_wrong = [{'input': p['input'], 'expected': p['expected'], **w}
                        for p in probes for w in p.get('wrong_outputs', []) if w['post'].get('holds') is True]
        runtime_errors = [p for p in probes if 'error_type' in p['pre'] or 'error_type' in p.get('reference_post', {})
                          or any('error_type' in w['post'] for w in p.get('wrong_outputs', []))]
        reference_runtime_errors = [p for p in probes if 'error_type' in p['pre'] or 'error_type' in p.get('reference_post', {})]
        rows.append({'sample': sample, 'task_id': task_id,
                     'pre_exclusion_count': len(pre_exclusions), 'false_rejection_count': len(false_rejections),
                     'missed_wrong_output_count': len(missed_wrong), 'runtime_error_input_count': len(runtime_errors),
                     'reference_runtime_error_input_count': len(reference_runtime_errors),
                     'observed_semantic_failure': bool(pre_exclusions or false_rejections or missed_wrong),
                     'probes': probes})
    result = {'protocol': 'finite canonical-reference and output-perturbation probes; not a mutation score or proof',
              'eligible_contracts': len(rows),
              'contracts_with_observed_semantic_failure': sum(r['observed_semantic_failure'] for r in rows),
              'contracts_with_runtime_errors': sum(bool(r['runtime_error_input_count']) for r in rows),
              'contracts_with_reference_runtime_errors': sum(bool(r['reference_runtime_error_input_count']) for r in rows),
              'rows': rows}
    (root / 'semantic_probes.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--audit-directory', required=True)
    p.add_argument('--dataset', required=True)
    main(p.parse_args())
