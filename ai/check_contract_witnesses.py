"""Replay concrete witnesses using CrossHair's actual parsed expressions.

Requires audit_reviewed_pilot.py output. Does not alter generated contracts.
These finite witnesses are not a benchmark mutation score or exhaustive proof.
"""
import importlib.util
import json
from pathlib import Path
import sys

from crosshair.condition_parser import Pep316Parser
from crosshair.fnutil import FunctionInfo


out = Path('ai/evidence/qwen-complete')
cases = [
    ('HumanEval_40_2', 'triples_sum_to_zero', {'l': [0, 0, 0]}, False, True),
    ('HumanEval_8_3', 'sum_product', {'numbers': [2, 3]}, (5, 1), (5, 6)),
    ('HumanEval_8_3', 'sum_product', {'numbers': [0, 2]}, (2, 0), (2, 0)),
    ('HumanEval_8_2', 'sum_product', {'numbers': []}, (0, 999), (0, 1)),
]
rows = []
for sample, entry, arguments, candidate, expected in cases:
    path = out / 'fence_only_copies' / (sample + '.py')
    spec = importlib.util.spec_from_file_location(sample, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[sample] = module
    spec.loader.exec_module(module)
    conditions = Pep316Parser().get_fn_conditions(FunctionInfo.from_fn(getattr(module, entry)))
    assert not list(conditions.syntax_messages())
    bindings = {**arguments, '__return__': candidate}
    evaluated = {}
    for kind, clauses in [('pre', conditions.pre), ('post', conditions.post)]:
        evaluated[kind] = []
        for clause in clauses:
            value = clause.evaluate(bindings)
            evaluated[kind].append({'expression': clause.expr_source,
                                    'value_repr': repr(value), 'truth': bool(value)})
    row = {'sample': sample, 'input': arguments, 'candidate_output': candidate,
           'task_expected_output': expected,
           'pre_holds': all(c['truth'] for c in evaluated['pre']),
           'post_holds': all(c['truth'] for c in evaluated['post']),
           'checks': evaluated,
           'scope': 'concrete witness using actual CrossHair condition parser; not exhaustive verification'}
    rows.append(row)
    print(sample, arguments, 'candidate', candidate, 'expected', expected,
          'pre', row['pre_holds'], 'post', row['post_holds'])
(out / 'concrete_contract_witnesses.json').write_text(json.dumps(rows, indent=2) + '\n')
