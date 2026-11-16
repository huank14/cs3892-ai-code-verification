"""Live demo: one contract, one implementation, CrossHair output streamed, then interpreted.

    .venv/Scripts/python -m pipeline.demo --task HumanEval/8 --contract qwen_v1_8_3 --impl reference
    .venv/Scripts/python -m pipeline.demo --task HumanEval/6 --contract human --impl mutant_m1 --bounded

Steps: (1) show the contract exactly as written, (2) compose it with the implementation,
(3) run `crosshair check` and stream its output, (4) explain each postcondition's verdict,
(5) re-execute every counterexample in a fresh process and show which condition fails.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from .compose import compose
from .crosshair_run import LINE_RE, classify
from .run_matrix import REPO, discover, rel, task_dir, worker

EXPLAIN = {
    'confirmed': 'holds on every execution path under the precondition (proof relative to CrossHair\'s model)',
    'not_confirmed': 'no counterexample found within the budget: inconclusive, NOT a proof',
    'counterexample': 'COUNTEREXAMPLE: an input satisfies pre but this post is false',
    'exception': 'the call raised on an input satisfying pre',
    'pre_unsat': 'no input satisfying the precondition was found',
    'other': 'tool message',
}


def banner(text: str) -> None:
    print(f'\n=== {text} ' + '=' * max(0, 70 - len(text)), flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--task', required=True)
    ap.add_argument('--contract', required=True, help='human or qwen_v2_6_1 etc.')
    ap.add_argument('--impl', required=True, help='reference, mutant_<id>, or qwen_<...>_impl')
    ap.add_argument('--timeout', type=float, default=30)
    ap.add_argument('--bounded', action='store_true')
    ap.add_argument('--out', default=str(Path(__file__).resolve().parent.parent / 'results' / 'scratch-demo'))
    a = ap.parse_args(argv)

    samples = json.loads((REPO / 'ai/analysis/samples.json').read_text(encoding='utf-8'))
    entry, contracts, impls = discover(a.task, samples)
    c = next(x for x in contracts if x.contract_id == a.contract)
    impl = next(x for x in impls if x['impl_id'] == a.impl)
    bound = None
    if a.bounded:
        bound = json.loads((task_dir(a.task) / 'task.json').read_text(encoding='utf-8'))['analysis_bound']

    banner(f'1. Contract {c.contract_id} for {a.task} (verbatim from {rel(c.source_path)})')
    for line in c.docstring_src.splitlines():
        if line.strip() and not line.strip().startswith('>>>'):
            print('   ' + line.strip())
    if bound:
        print(f'   + harness analysis bound (first pre:): {bound}')

    banner(f'2. Implementation {impl["impl_id"]} ({rel(impl["path"])})')
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    module = out / f'{c.contract_id}__{impl["impl_id"]}.py'
    module.write_text(compose(impl['path'], c, use_contract_signature=a.bounded, extra_pre=bound), encoding='utf-8')
    print(f'   composed module: {rel(module)}')
    conds = worker('conditions', module, entry)
    posts = {p['line']: p['expr'] for p in conds['post']}

    cmd = [sys.executable, '-m', 'crosshair', 'check', str(module), '--analysis_kind=PEP316',
           '--report_all', f'--per_condition_timeout={a.timeout}']
    banner('3. crosshair check (live)')
    print('   $ crosshair check ' + module.name + f' --analysis_kind=PEP316 --report_all --per_condition_timeout={a.timeout}')
    t0 = time.perf_counter()
    reports = []
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as p:
        for raw in p.stdout:
            m = LINE_RE.match(raw.rstrip())
            if m:
                print(f'   line {m["line"]}: {m["level"]}: {m["msg"]}', flush=True)
                reports.append({'line': int(m['line']), **classify(m['msg'])})
            elif raw.strip():
                print('   ' + raw.rstrip(), flush=True)
    print(f'   ({time.perf_counter() - t0:.1f}s)')

    banner('4. What each postcondition verdict means')
    for r in reports:
        expr = posts.get(r['line'], '(not a postcondition line)')
        print(f'   [{r["status"]:>14}] {expr}\n                    -> {EXPLAIN[r["status"]]}')

    cex = [r for r in reports if r['status'] in ('counterexample', 'exception') and r.get('call')]
    if cex:
        banner('5. Re-executing each counterexample in a fresh process')
    for r in cex:
        extra = [task_dir(a.task) / 'reference.py'] if impl['kind'] != 'reference' else []
        rp = worker('replay', module, entry, r['call'], *extra)
        print(f'   input : {r["call"]}')
        print(f'   output: {rp.get("return_repr", rp.get("raised"))}')
        for pc in rp.get('post', []):
            mark = 'FALSE' if pc.get('value') is False else ('ERROR' if 'error' in pc else 'true ')
            print(f'     {mark}  {pc["expr"]}')
        if 'reference' in rp:
            ref = rp['reference']
            print(f'   reference output on the same input: {ref.get("return_repr")} -> '
                  f'{"satisfies" if rp["reference_satisfies_contract"] else "ALSO VIOLATES"} the contract')
    if not cex:
        print('\n   No counterexample. Verdict:',
              'ACCEPTED_PROVEN' if reports and all(r['status'] == 'confirmed' for r in reports) else 'INCONCLUSIVE')


if __name__ == '__main__':
    main()
