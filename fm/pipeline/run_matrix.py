"""Batch verifier: every contract x every implementation for the selected tasks.

Run from fm/ with the pinned venv:
    .venv/Scripts/python -m pipeline.run_matrix --tasks HumanEval/6 --timeout 30 --out results/<name>

Contracts per task:   human  (tasks/<T>/human_contract.py, if present)
                      qwen_* (every sample with contract_parser_status == parsed in ai/analysis/samples.json)
Implementations:      reference (canonical solution), mutant_* (tasks/<T>/mutants/manifest.json),
                      qwen_*_impl (every generated module that parses as Python)
Jobs (default):       every contract x {reference, all mutants}
                      human x every qwen implementation   (FM4AI: AI code vs reference spec)
                      qwen contract x its own implementation
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

from .compose import ComposeError, compose, load_contract
from .crosshair_run import run_check

FM = Path(__file__).resolve().parent.parent
REPO = FM.parent
WORKER = Path(__file__).resolve().parent / 'worker.py'


def rel(p) -> str:
    p = Path(p).resolve()
    return p.relative_to(REPO).as_posix() if p.is_relative_to(REPO) else p.as_posix()


def task_dir(task_id: str) -> Path:
    return FM / 'tasks' / task_id.replace('/', '_')


def worker(*args, timeout=120) -> dict:
    try:
        p = subprocess.run([sys.executable, '-I', str(WORKER), *map(str, args)],
                           capture_output=True, text=True, timeout=timeout)
        return json.loads(p.stdout) if p.stdout.strip() else {'ok': False, 'error': p.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': f'worker timeout after {timeout}s'}


def short_id(sample_id: str) -> str:            # v2/HumanEval_6_1 -> v2_6_1
    version, rest = sample_id.split('/')
    return version + '_' + rest.replace('HumanEval_', '')


def discover(task_id: str, samples: list[dict]):
    td = task_dir(task_id)
    meta = json.loads((td / 'task.json').read_text(encoding='utf-8'))
    entry = meta['entry_point']
    contracts, impls = [], [{'impl_id': 'reference', 'kind': 'reference', 'path': td / 'reference.py'}]
    if (td / 'human_contract.py').exists():
        contracts.append(load_contract(td / 'human_contract.py', entry, 'human', task_id,
                                       {'author': 'human reference (see human_contract.md)'}))
    manifest = td / 'mutants' / 'manifest.json'
    if manifest.exists():
        for m in json.loads(manifest.read_text(encoding='utf-8')):
            impls.append({'impl_id': 'mutant_' + m['id'], 'kind': 'mutant',
                          'path': td / 'mutants' / m['file'], 'mutant': m})
    for s in samples:
        if s['task_id'] != task_id:
            continue
        src = REPO / s['repository_source']
        sid = short_id(s['sample_id'])
        if s['contract_parser_status'] == 'parsed':
            contracts.append(load_contract(src, entry, 'qwen_' + sid, task_id, {
                'sample_id': s['sample_id'], 'repository_source': s['repository_source'],
                'repository_raw_record': s['repository_raw_record'], 'normalization': s['normalization']}))
        if s['contract_parser_status'] != 'python_syntax_error':
            impls.append({'impl_id': 'qwen_' + sid + '_impl', 'kind': 'qwen', 'path': src,
                          'sample_id': s['sample_id'], 'contract_parser_status': s['contract_parser_status']})
    return entry, contracts, impls


def plan(contracts, impls, kinds: set[str]):
    jobs = []
    for c in contracts:
        for i in impls:
            own = c.contract_id != 'human' and i['impl_id'] == c.contract_id + '_impl'
            if (i['kind'] in ('reference', 'mutant') and i['kind'] in kinds) \
                    or (i['kind'] == 'qwen' and c.contract_id == 'human' and 'qwen' in kinds) \
                    or (own and 'self' in kinds):
                jobs.append((c, i))
    return jobs


def verdict(conds: dict, ch: dict, replays: list[dict]) -> tuple[str, dict]:
    """Aggregate per-postcondition CrossHair results into one contract-implementation verdict."""
    if not conds.get('ok'):
        return 'CONTRACT_LOAD_ERROR', {}
    if conds['syntax_errors'] or not conds['post']:
        return 'CONTRACT_INVALID', {}
    post_lines = {p['line'] for p in conds['post']}
    per_post = {p['line']: 'missing' for p in conds['post']}
    for r in ch['reports']:
        if r['line'] in post_lines:
            per_post[r['line']] = r['status']
    statuses = [r['status'] for r in ch['reports']]
    replayed = [r for r in replays if r['confirmed']]
    # A rejection only counts if the reference satisfies the contract on the same input
    # (otherwise the contract rejects everything there; it did not tell the two apart).
    disc = [r for r in replayed if r.get('discriminating') is not False]
    replayed_cex = [r for r in disc if r['report']['status'] == 'counterexample']
    replayed_exc = [r for r in disc if r['report']['status'] == 'exception']
    nondisc = [r for r in replayed if r.get('discriminating') is False]
    contract_err = [r for r in replays if r.get('contract_error')]
    unreplayed = [r for r in replays if not r['confirmed'] and not r.get('contract_error')]
    detail = {'per_postcondition': per_post, 'unreplayed_reports': len(unreplayed),
              'nondiscriminating_rejections': len(nondisc)}
    if 'pre_unsat' in statuses:
        return 'PRE_UNSAT', detail
    if replayed_cex:
        return 'REJECTED', detail            # concrete input: pre holds, some post false (re-executed)
    if replayed_exc:
        return 'REJECTED_EXCEPTION', detail  # implementation raises on an input satisfying pre
    if nondisc:
        return 'REJECTED_NONDISCRIMINATING', detail  # reference is rejected on that input too
    if contract_err:
        return 'CONTRACT_ERROR', detail      # evaluating the contract itself raises
    if ch['exit_code'] is None or 'other' in statuses:
        return 'TOOL_ERROR', detail
    if all(v == 'confirmed' for v in per_post.values()):
        return 'ACCEPTED_PROVEN', detail     # relative to CrossHair's model of Python
    return 'INCONCLUSIVE', detail            # no counterexample within budget; not a proof


def analyse(module: Path, c, impl, entry: str, timeout: float) -> dict:
    """crosshair check one composed module, re-execute every reported input, aggregate."""
    conds = worker('conditions', module, entry)
    ch = run_check(module, timeout) if conds.get('ok') and not conds.get('syntax_errors') else \
        {'reports': [], 'exit_code': 0, 'elapsed_seconds': 0, 'skipped': True, 'stdout': '', 'stderr': ''}
    replays = []
    for r in ch['reports']:
        if r['status'] in ('counterexample', 'exception') and r.get('call'):
            extra = [task_dir(c.task_id) / 'reference.py'] if impl['kind'] != 'reference' else []
            rp = worker('replay', module, entry, r['call'], *extra)
            item = {'report': r, 'replay': rp, 'confirmed': False}
            if rp.get('ok') and rp.get('pre_holds'):
                if r['status'] == 'counterexample':
                    item['confirmed'] = bool(rp.get('violated_lines'))
                    item['line_matches'] = r['line'] in rp.get('violated_lines', [])
                else:
                    item['confirmed'] = 'raised' in rp
                item['contract_error'] = bool(rp.get('contract_error_lines'))
                item['discriminating'] = rp.get('reference_satisfies_contract', None)
            replays.append(item)
    v, detail = verdict(conds, ch, replays)
    return {'module': rel(module), 'conditions': conds, 'replays': replays, 'verdict': v, 'verdict_detail': detail,
            'crosshair': {k: ch.get(k) for k in ('command', 'exit_code', 'elapsed_seconds', 'reports', 'stderr')},
            '_log': ' '.join(ch.get('command', [])) + '\n' + (ch.get('stdout') or '') + (ch.get('stderr') or '')}


SOUND_REJECTIONS = ('REJECTED', 'REJECTED_EXCEPTION')


def combine(bounded: dict, unbounded: dict | None) -> str:
    """Combined mode: a re-executed rejection from either run is sound; a confirmation only
    holds within the bound, and only if the unbounded search found no counterexample."""
    runs = [r for r in (bounded, unbounded) if r]
    for r in runs:
        if r['verdict'] in SOUND_REJECTIONS:
            return r['verdict']
    for r in runs:
        if r['verdict'] == 'REJECTED_NONDISCRIMINATING':
            return r['verdict']
    if bounded['verdict'] == 'ACCEPTED_PROVEN':
        return 'ACCEPTED_PROVEN_BOUNDED'
    return bounded['verdict']


def run_job(c, impl, entry, out: Path, timeout: float, opts: dict | None = None) -> dict:
    """mode 'unbounded' (default), 'bounded' (task bound as first pre:), or 'combined'
    (bounded first; if not soundly rejected, an unbounded run also searches for counterexamples)."""
    opts = opts or {}
    mode = opts.get('mode', 'unbounded')
    bound = (opts.get('bounds') or {}).get(c.task_id) if mode != 'unbounded' else None
    sig = bool(opts.get('contract_signature'))
    task = c.task_id.replace('/', '_')
    name = f'{c.contract_id}__{impl["impl_id"]}'
    mod_dir = out / 'modules' / task
    mod_dir.mkdir(parents=True, exist_ok=True)
    rec = {'task_id': c.task_id, 'contract_id': c.contract_id, 'impl_id': impl['impl_id'],
           'impl_kind': impl['kind'], 'impl_source': rel(impl['path']),
           'contract_source': rel(c.source_path), 'contract_provenance': c.provenance,
           'mode': mode, 'analysis_bound': bound, 'contract_signature': sig}
    try:
        plain = mod_dir / f'{name}.py'
        plain.write_text(compose(impl['path'], c, use_contract_signature=sig), encoding='utf-8')
        if bound:
            bmod = mod_dir / f'{name}__bounded.py'
            bmod.write_text(compose(impl['path'], c, use_contract_signature=sig, extra_pre=bound), encoding='utf-8')
    except (ComposeError, SyntaxError) as e:
        rec.update(verdict='COMPOSE_ERROR', error=str(e))
        return rec
    logs = out / 'logs' / task
    logs.mkdir(parents=True, exist_ok=True)
    runs = {}
    if bound:
        runs['bounded'] = analyse(bmod, c, impl, entry, timeout)
    if mode == 'unbounded' or (mode == 'combined' and runs['bounded']['verdict'] not in SOUND_REJECTIONS):
        runs['unbounded'] = analyse(plain, c, impl, entry, timeout)
    for k, r in runs.items():
        (logs / f'{name}.{k}.crosshair.txt').write_text(r.pop('_log'), encoding='utf-8')
    primary = runs.get('bounded') or runs['unbounded']
    # Top-level fields describe the primary analysis; `runs` keeps every analysis.
    rec.update({k: primary[k] for k in ('module', 'conditions', 'replays', 'verdict_detail')})
    rec['crosshair'] = dict(primary['crosshair'])
    rec['runs'] = {k: {kk: vv for kk, vv in r.items() if kk != 'conditions'} for k, r in runs.items()}
    if mode == 'combined':
        rec['verdict'] = combine(runs['bounded'], runs.get('unbounded'))
    elif mode == 'bounded':
        rec['verdict'] = 'ACCEPTED_PROVEN_BOUNDED' if primary['verdict'] == 'ACCEPTED_PROVEN' else primary['verdict']
    else:
        rec['verdict'] = primary['verdict']
    rec['crosshair']['elapsed_seconds'] = round(sum(r['crosshair']['elapsed_seconds'] or 0 for r in runs.values()), 2)
    # The concrete (test-input) check always uses the unbounded contract.
    rec['concrete'] = worker('concrete', plain, entry, task_dir(c.task_id), timeout=300)
    if rec['concrete'].get('ok'):
        rec['concrete'].pop('ok')
        rows = rec['concrete'].pop('rows')
        rec['concrete']['violating_inputs'] = [r for r in rows if r.get('violated_lines') or 'raised' in r]
        rec['concrete']['excluded_inputs'] = [r['input_repr'] for r in rows if not r['pre_holds']]
    return rec


def versions() -> dict:
    import crosshair, z3
    try:
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(['git', 'status', '--porcelain'], cwd=REPO, capture_output=True, text=True).stdout)
    except OSError:
        commit, dirty = None, None
    return {'python': sys.version, 'crosshair': crosshair.__version__, 'z3': z3.get_version_string(),
            'platform': platform.platform(), 'cpu_count': os.cpu_count(), 'git_commit': commit, 'git_dirty': dirty}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--tasks', nargs='+', required=True, help='e.g. HumanEval/6 HumanEval/8, or "all"')
    ap.add_argument('--timeout', type=float, default=30, help='CrossHair --per_condition_timeout (s)')
    ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--kinds', default='reference,mutant,qwen,self',
                    help='subset of reference,mutant,qwen,self')
    ap.add_argument('--contracts', default='*', help='glob on contract id, e.g. "human" or "qwen_v2_*"')
    ap.add_argument('--samples', default=str(REPO / 'ai/analysis/samples.json'))
    ap.add_argument('--out', required=True)
    ap.add_argument('--mode', choices=['unbounded', 'bounded', 'combined'], default='unbounded',
                    help='bounded: task analysis_bound (task.json) as the first pre:; '
                         'combined: bounded, then an unbounded counterexample search if not rejected')
    ap.add_argument('--contract-signature', action='store_true',
                    help="analyse with the contract's declared parameter types instead of the implementation's")
    a = ap.parse_args(argv)

    samples = json.loads(Path(a.samples).read_text(encoding='utf-8'))
    tasks = sorted(p.name.replace('_', '/') for p in (FM / 'tasks').glob('HumanEval_*')) \
        if a.tasks == ['all'] else a.tasks
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    opts = {'contract_signature': a.contract_signature, 'bounds': {}, 'mode': a.mode}
    if a.mode != 'unbounded':
        for t in tasks:
            b = json.loads((task_dir(t) / 'task.json').read_text(encoding='utf-8')).get('analysis_bound')
            if not b:
                sys.exit(f'--mode {a.mode}: no analysis_bound in {task_dir(t) / "task.json"}')
            opts['bounds'][t] = b if isinstance(b, list) else [b]
    all_jobs, inventory = [], {}
    for t in tasks:
        entry, contracts, impls = discover(t, samples)
        contracts = [c for c in contracts if fnmatch.fnmatch(c.contract_id, a.contracts)]
        inventory[t] = {'contracts': [c.contract_id for c in contracts], 'implementations': [i['impl_id'] for i in impls]}
        all_jobs += [(c, i, entry) for c, i in plan(contracts, impls, set(a.kinds.split(',')))]
    meta = {'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'argv': sys.argv,
            'per_condition_timeout': a.timeout, 'workers': a.workers, 'jobs': len(all_jobs),
            'mode': a.mode, 'analysis_bounds': opts['bounds'], 'contract_signature': a.contract_signature,
            'inventory': inventory, 'versions': versions()}
    (out / 'run_meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print(f'{len(all_jobs)} jobs across {len(tasks)} task(s); timeout {a.timeout}s/condition; {a.workers} workers',
          flush=True)
    results = []
    with ThreadPoolExecutor(a.workers) as ex, open(out / 'results.jsonl', 'w', encoding='utf-8') as fh:
        futs = {ex.submit(run_job, c, i, e, out, a.timeout, opts): (c, i) for c, i, e in all_jobs}
        for n, f in enumerate(as_completed(futs), 1):
            c, i = futs[f]
            try:
                rec = f.result()
            except Exception as e:  # keep the batch going; record the failure
                rec = {'task_id': c.task_id, 'contract_id': c.contract_id, 'impl_id': i['impl_id'],
                       'impl_kind': i['kind'], 'verdict': 'HARNESS_ERROR', 'error': repr(e)}
            results.append(rec)
            fh.write(json.dumps(rec, default=str) + '\n')
            fh.flush()
            print(f'[{n}/{len(all_jobs)}] {rec["task_id"]} {rec["contract_id"]} x {rec["impl_id"]}: '
                  f'{rec["verdict"]} ({rec.get("crosshair", {}).get("elapsed_seconds", 0)}s)', flush=True)
    meta['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    (out / 'run_meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    from .summarize import summarize
    summarize(out)


if __name__ == '__main__':
    main()
