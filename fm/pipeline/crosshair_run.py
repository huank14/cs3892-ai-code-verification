"""Run `crosshair check` on one composed module and interpret its output.

Per-condition statuses parsed from `--report_all` output:
  confirmed       "Confirmed over all paths."   all paths under pre explored, post held
  not_confirmed   "Not confirmed."              budget ended; inconclusive, NOT evidence of correctness
  counterexample  "false when calling f(..)"    pre holds and post is false on that input
  exception       "XError: .. when calling f(..)" the call (or a condition) raised
  pre_unsat       "Unable to meet precondition" no input satisfying pre was found
  other           anything else (tool error)
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

LINE_RE = re.compile(r'^(?P<path>.*?):(?P<line>\d+): (?P<level>error|info|warning): (?P<msg>.*)$')
CALL_RE = re.compile(r'^(?:(?P<false>false)|(?P<exc>[A-Za-z_][\w.]*)(?::(?P<excmsg>.*?))?) when calling '
                     r'(?P<call>.*?)(?: \(which returns (?P<ret>.*)\))?$')


def classify(msg: str) -> dict:
    m = msg.strip()
    if m.startswith('Confirmed over all paths'):
        return {'status': 'confirmed'}
    if m.startswith('Not confirmed'):
        return {'status': 'not_confirmed'}
    if 'Unable to meet precondition' in m:
        return {'status': 'pre_unsat'}
    c = CALL_RE.match(m)
    if c:
        out = {'status': 'counterexample' if c['false'] else 'exception', 'call': c['call'],
               'crosshair_return': c['ret']}
        if c['exc']:
            out['exception'] = c['exc'] + (':' + c['excmsg'] if c['excmsg'] else '')
        return out
    return {'status': 'other'}


def run_check(module: Path, per_condition_timeout: float, python: str = sys.executable) -> dict:
    cmd = [python, '-m', 'crosshair', 'check', str(module), '--analysis_kind=PEP316',
           '--report_all', f'--per_condition_timeout={per_condition_timeout}']
    t0 = time.perf_counter()
    # Hard wall-clock cap so a hung analysis cannot block the batch.
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=max(600, per_condition_timeout * 40))
        stdout, stderr, code = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        stdout, stderr, code = (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), \
            'WALL TIMEOUT', None
    elapsed = time.perf_counter() - t0
    lines = []
    for raw in stdout.splitlines():
        m = LINE_RE.match(raw)
        if m:
            lines.append({'line': int(m['line']), 'level': m['level'], 'message': m['msg'], **classify(m['msg'])})
        elif raw.strip():
            lines.append({'line': None, 'level': None, 'message': raw, 'status': 'other'})
    return {'command': cmd, 'exit_code': code, 'elapsed_seconds': round(elapsed, 2),
            'stdout': stdout, 'stderr': stderr, 'reports': lines}
