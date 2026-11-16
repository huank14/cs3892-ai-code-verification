"""Turn results.jsonl into summary.csv and summary.md.

Definitions (also on the slides):
  For contract c and validated mutant set M of a task:
    killed(c, m)  <=> CrossHair reports an input x with pre_c(x) and not post_c(x, m(x)),
                      re-executing m(x) reproduces the violation, and post_c(x, ref(x)) holds
                      (the contract tells m apart from the reference at x; verdict REJECTED).
    MS(c) = |{m in M : killed(c, m)}| / |M|; contracts that reject the reference are flagged.
  A contract that rejects the reference implementation (REJECTED on `reference`, or a post
  violation on an official-test input) is counted as over-restrictive, not as strong.
  REJECTED_EXCEPTION (mutant raises on a valid input) and INCONCLUSIVE are reported separately.
Usage: python -m pipeline.summarize results/<run>
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


DETERMINATE = {'REJECTED', 'REJECTED_EXCEPTION', 'REJECTED_NONDISCRIMINATING', 'ACCEPTED_PROVEN',
               'ACCEPTED_PROVEN_BOUNDED'}


def summarize(out: Path) -> None:
    out = Path(out)
    recs = [json.loads(l) for l in (out / 'results.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    by = defaultdict(list)
    for r in recs:
        by[(r['task_id'], r['contract_id'])].append(r)
    rows = []
    for (task, cid), rs in sorted(by.items()):
        ref = next((r for r in rs if r['impl_kind'] == 'reference'), None)
        muts = [r for r in rs if r['impl_kind'] == 'mutant']
        conc = lambda r: r.get('concrete', {}) or {}
        ref_conc_bad = bool(ref and (conc(ref).get('post_violations') or conc(ref).get('contract_errors')))
        over = bool(ref and (ref['verdict'] == 'REJECTED' or ref_conc_bad))
        count = lambda v: sum(r['verdict'] == v for r in muts)
        killed = count('REJECTED')
        row = {
            'task': task, 'contract': cid,
            'reference_verdict': ref['verdict'] if ref else '',
            'reference_concrete_violations': conc(ref).get('post_violations', '') if ref else '',
            'reference_concrete_pre_excluded': conc(ref).get('pre_excluded', '') if ref else '',
            'over_restrictive': over,
            'mutants': len(muts), 'killed': killed,
            'killed_by_exception': count('REJECTED_EXCEPTION'),
            'nondiscriminating': count('REJECTED_NONDISCRIMINATING'),
            'accepted_proven': count('ACCEPTED_PROVEN') + count('ACCEPTED_PROVEN_BOUNDED'), 'inconclusive': count('INCONCLUSIVE'),
            'errors': sum(r['verdict'] not in ('REJECTED', 'REJECTED_EXCEPTION', 'REJECTED_NONDISCRIMINATING',
                                               'ACCEPTED_PROVEN', 'ACCEPTED_PROVEN_BOUNDED', 'INCONCLUSIVE')
                          for r in muts),
            'concrete_killed': sum(bool(conc(r).get('post_violations')) for r in muts),
            'mutation_score': '' if not muts else f'{killed / len(muts):.2f}',
            'self_impl_verdict': next((r['verdict'] for r in rs if r['impl_kind'] == 'qwen'
                                       and r['impl_id'] == cid + '_impl'), ''),
        }
        if cid == 'human':
            q = [r for r in rs if r['impl_kind'] == 'qwen']
            row['human_vs_qwen_impls'] = ' '.join(f"{r['impl_id'].removeprefix('qwen_').removesuffix('_impl')}="
                                                  f"{r['verdict']}" for r in sorted(q, key=lambda r: r['impl_id']))
        rows.append(row)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(out / 'summary.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fields)
        w.writeheader()
        w.writerows(rows)
    md = ['# Verification summary', '', f'Source: `{(out / "results.jsonl").name}` ({len(recs)} jobs). '
          'MS = killed / mutants (symbolic, re-executed, discriminating against the reference). '
          'Over-restrictive = the contract rejects the reference (symbolically or on an official-test input).', '',
          '| task | contract | reference | over-restrictive | killed / mutants | exc | non-discr. | proven-accepted | '
          'inconclusive | err | concrete kills | MS |', '|' + '---|' * 12]
    for r in rows:
        md.append(f"| {r['task']} | {r['contract']} | {r['reference_verdict']} | {'yes' if r['over_restrictive'] else ''} | "
                  f"{r['killed']} / {r['mutants']} | {r['killed_by_exception']} | {r['nondiscriminating']} | {r['accepted_proven']} | "
                  f"{r['inconclusive']} | {r['errors']} | {r['concrete_killed']} | {r['mutation_score']} |")
    human = [r for r in rows if r.get('human_vs_qwen_impls')]
    if human:
        md += ['', '## Human reference contract vs. Qwen implementations', '']
        md += [f"- {r['task']}: {r['human_vs_qwen_impls']}" for r in human]
    verdicts = defaultdict(int)
    for r in recs:
        verdicts[r['verdict']] += 1
    md += ['', '## Verdict counts', ''] + [f'- {k}: {v}' for k, v in sorted(verdicts.items())]
    # Proposal criterion: share of checks with a determinate CrossHair verdict
    # (a re-executed counterexample, or confirmation over all paths).
    md += ['', '## Determinate verdicts (counterexample or confirmed over all paths)', '']
    groups = {'all jobs': recs, 'contract x mutant': [r for r in recs if r['impl_kind'] == 'mutant'],
              'contract x reference': [r for r in recs if r['impl_kind'] == 'reference'],
              'contract x Qwen implementation': [r for r in recs if r['impl_kind'] == 'qwen']}
    for name, rs in groups.items():
        if rs:
            d = sum(r['verdict'] in DETERMINATE for r in rs)
            md.append(f'- {name}: {d}/{len(rs)} = {d / len(rs):.0%}')
    (out / 'summary.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print('\n'.join(md))


if __name__ == '__main__':
    summarize(Path(sys.argv[1]))
