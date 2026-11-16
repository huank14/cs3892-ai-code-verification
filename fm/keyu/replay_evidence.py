"""Replay archived symbolic witnesses without retaining generated modules.

From fm/: python -m keyu.replay_evidence --out results/keyu-replay/replay.json
This does not run a new CrossHair search or modify the original run records.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from pipeline.compose import compose, load_contract
from pipeline.worker import load, mode_replay, parse_call

FM = Path(__file__).resolve().parent.parent
REPO = FM.parent


def replay_all():
    directory = FM / 'results/keyu-mutants-t60'
    records = [json.loads(line) for line in (directory / 'results.jsonl').read_text().splitlines()]
    metadata = json.loads((directory / 'run_meta.json').read_text())
    if len(records) != metadata['jobs'] or 'finished_utc' not in metadata:
        raise ValueError('The archived run is incomplete')
    rows = []
    with tempfile.TemporaryDirectory(prefix='keyu-replay-') as temp:
        for record in records:
            task = FM / 'tasks' / record['task_id'].replace('/', '_')
            entry = json.loads((task / 'task.json').read_text())['entry_point']
            contract = load_contract(task / 'human_contract.py', entry,
                                     record['contract_id'], record['task_id'])
            domain = load(str(task / 'input_domain.py'), '_replay_domain').in_domain
            calls = []
            for mode, run in record['runs'].items():
                witnesses = [r for r in run.get('replays', [])
                             if r.get('confirmed') and r.get('discriminating') is True
                             and r['report']['status'] == 'counterexample']
                if not witnesses:
                    continue
                source = compose(REPO / record['impl_source'], contract,
                                 use_contract_signature=record['contract_signature'],
                                 extra_pre=record['analysis_bound'] if mode == 'bounded' else None)
                module = Path(temp) / f"{task.name}_{record['impl_id']}_{mode}.py"
                module.write_text(source)
                environment = dict(vars(load(str(module), '_replay_module')))
                for witness in witnesses:
                    call = witness['report']['call']
                    args, kwargs = parse_call(call, entry, environment)
                    result = mode_replay(str(module), entry, call, str(task / 'reference.py'))
                    in_domain = bool(domain(*args, **kwargs))
                    confirmed = bool(in_domain and result['pre_holds']
                                     and result.get('violated_lines')
                                     and not result.get('contract_error_lines')
                                     and 'raised' not in result
                                     and result.get('reference_satisfies_contract'))
                    same_returns = (result.get('return_repr') == witness['replay'].get('return_repr')
                                    and result['reference'].get('return_repr')
                                    == witness['replay']['reference'].get('return_repr'))
                    calls.append({'mode': mode, 'call': call, 'in_domain': in_domain,
                                  'replay_confirmed': confirmed, 'same_recorded_returns': same_returns})
            passed = record['verdict'] == 'REJECTED' and bool(calls) and all(
                c['replay_confirmed'] and c['same_recorded_returns'] for c in calls)
            rows.append({'task_id': record['task_id'], 'mutant_id': record['impl_id'],
                         'archived_verdict': record['verdict'], 'passed': passed, 'calls': calls})
    return {'kind': 'Concrete replay of archived symbolic counterexamples; no new search',
            'checks': len(rows), 'passed': sum(r['passed'] for r in rows), 'rows': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    options = parser.parse_args()
    report = replay_all()
    options.out.parent.mkdir(parents=True, exist_ok=True)
    options.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'checks': report['checks'], 'passed': report['passed'],
                      'out': str(options.out)}))
    if report['passed'] != report['checks']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
