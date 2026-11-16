"""Isolated executor, always run in a subprocess (python -I) with a timeout.

Modes (JSON on stdout):
  conditions MODULE ENTRY            -> parsed pre/post conditions with line numbers
  replay     MODULE ENTRY CALL       -> re-execute a CrossHair call string, evaluate pre/post
  concrete   MODULE ENTRY TASK_DIR   -> evaluate pre/post on official-test inputs (+ witness inputs)

Only run on reviewed code: this is process isolation, not a security sandbox.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
import inspect
import json
import sys
import types
from pathlib import Path

from crosshair.condition_parser import Pep316Parser
from crosshair.fnutil import FunctionInfo


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def conditions_of(fn):
    return Pep316Parser().get_fn_conditions(FunctionInfo.from_fn(fn))


def describe(conds) -> dict:
    return {
        'pre': [{'line': c.line, 'expr': c.expr_source} for c in conds.pre],
        'post': [{'line': c.line, 'expr': c.expr_source} for c in conds.post],
        'syntax_errors': [{'line': e.line_num, 'message': e.message} for e in conds.syntax_messages()],
    }


def _eval_all(clauses, bindings) -> list[dict]:
    out = []
    for c in clauses:
        try:
            out.append({'line': c.line, 'expr': c.expr_source, 'value': bool(c.evaluate(bindings))})
        except Exception as e:  # contract itself fails on this input
            out.append({'line': c.line, 'expr': c.expr_source, 'error': f'{type(e).__name__}: {e}'})
    return out


def check_input(fn, conds, args: list, kwargs: dict) -> dict:
    """Evaluate pre on the input, call fn, evaluate every post on (input, result)."""
    sig = inspect.signature(fn)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()
    old = copy.deepcopy(dict(bound.arguments))
    pre = _eval_all(conds.pre, copy.deepcopy(old))
    res = {'input_repr': {k: repr(v) for k, v in old.items()}, 'pre': pre,
           'pre_holds': all(p.get('value') is True for p in pre)}
    if not res['pre_holds']:
        return res
    try:
        ret = fn(*bound.args, **bound.kwargs)
    except Exception as e:
        res['raised'] = f'{type(e).__name__}: {e}'
        return res
    res['return_repr'] = repr(ret)
    bindings = dict(bound.arguments, __return__=ret, __old__=types.SimpleNamespace(**old))
    res['post'] = _eval_all(conds.post, bindings)
    res['violated_lines'] = [p['line'] for p in res['post'] if p.get('value') is False]
    res['contract_error_lines'] = [p['line'] for p in res['post'] if 'error' in p]
    return res


def parse_call(call: str, entry: str, env: dict):
    node = ast.parse(call.strip(), mode='eval').body
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == entry):
        raise ValueError(f'unexpected call expression: {call!r}')
    ev = lambda n: eval(compile(ast.Expression(n), '<cex>', 'eval'), env)
    return [ev(a) for a in node.args], {k.arg: ev(k.value) for k in node.keywords}


def mode_conditions(module, entry):
    fn = getattr(load(module, '_under_test'), entry)
    return describe(conditions_of(fn))


def mode_replay(module, entry, call, reference=None):
    """Re-execute; with `reference`, also check the reference output against the same contract
    at the same input (a kill only discriminates if the reference satisfies the contract there)."""
    mod = load(module, '_under_test')
    fn = getattr(mod, entry)
    conds = conditions_of(fn)
    args, kwargs = parse_call(call, entry, dict(vars(mod)))
    out = check_input(fn, conds, copy.deepcopy(args), copy.deepcopy(kwargs))
    if reference:
        ref = getattr(load(reference, '_reference'), entry)
        r = check_input(ref, conds, args, kwargs)
        out['reference'] = r
        out['reference_satisfies_contract'] = bool(r['pre_holds'] and 'raised' not in r
                                                   and not r.get('violated_lines') and not r.get('contract_error_lines'))
    return out


def recorded_test_inputs(task_dir: Path, entry: str) -> list[list]:
    """Run the official HumanEval check() against a recorder wrapping the reference."""
    ref = getattr(load(str(task_dir / 'reference.py'), '_reference'), entry)
    calls = []

    def recorder(*args):
        calls.append(copy.deepcopy(list(args)))
        return ref(*args)

    env = {}
    exec(compile((task_dir / 'tests.py').read_text(encoding='utf-8'), 'tests.py', 'exec'), env)
    env['check'](recorder)
    return calls


def mode_concrete(module, entry, task_dir):
    task_dir = Path(task_dir)
    mod = load(module, '_under_test')
    fn = getattr(mod, entry)
    conds = conditions_of(fn)
    ref = getattr(load(str(task_dir / 'reference.py'), '_reference'), entry)
    inputs = [('test', a) for a in recorded_test_inputs(task_dir, entry)]
    manifest = task_dir / 'mutants' / 'manifest.json'
    if manifest.exists():
        for m in json.loads(manifest.read_text(encoding='utf-8')):
            if 'witness' in m:
                inputs.append((f"witness:{m['id']}", m['witness']['args']))
    rows = []
    for origin, args in inputs:
        r = check_input(fn, conds, copy.deepcopy(args), {})
        r['origin'] = origin
        try:
            r['reference_return_repr'] = repr(ref(*copy.deepcopy(args)))
            r['differs_from_reference'] = r.get('return_repr') is not None and \
                r['return_repr'] != r['reference_return_repr']
        except Exception as e:
            r['reference_raised'] = f'{type(e).__name__}: {e}'
        rows.append(r)
    return {'inputs': len(rows),
            'pre_excluded': sum(not r['pre_holds'] for r in rows),
            'post_violations': sum(bool(r.get('violated_lines')) for r in rows),
            'contract_errors': sum(bool(r.get('contract_error_lines')) for r in rows),
            'raised': sum('raised' in r for r in rows),
            'rows': rows}


def main(argv):
    mode, *rest = argv
    try:
        out = {'conditions': mode_conditions, 'replay': mode_replay, 'concrete': mode_concrete}[mode](*rest)
        out['ok'] = True
    except Exception as e:
        out = {'ok': False, 'error': f'{type(e).__name__}: {e}'}
    sys.stdout.write(json.dumps(out, default=repr))


if __name__ == '__main__':
    main(sys.argv[1:])
