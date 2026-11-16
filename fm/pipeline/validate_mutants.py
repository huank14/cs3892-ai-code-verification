"""Check that every mutant in tasks/<T>/mutants/manifest.json is really wrong.

For each mutant: reference(*witness.args) == witness.expected, mutant(*witness.args)
== witness.actual, and expected != actual. Also records whether the mutant passes the
official HumanEval tests (a mutant that passes them is a test-suite gap, still valid).
Optional: --diffbehavior also asks CrossHair for a distinguishing input.
Usage (from fm/): .venv/Scripts/python -m pipeline.validate_mutants HumanEval/6 [--diffbehavior]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

FM = Path(__file__).resolve().parent.parent

PROBE = r'''
import copy, importlib.util, json, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m
ref_path, mut_path, entry, args, tests = sys.argv[1:6]
args = json.loads(args)
ref = getattr(load(ref_path, "_ref"), entry); mut = getattr(load(mut_path, "_mut"), entry)
out = {}
for k, f in (("reference", ref), ("mutant", mut)):
    try: out[k] = f(*copy.deepcopy(args))
    except Exception as e: out[k + "_raised"] = type(e).__name__ + ": " + str(e)
env = {}; exec(open(tests, encoding="utf-8").read(), env)
try: env["check"](mut); out["passes_official_tests"] = True
except Exception as e: out["passes_official_tests"] = False
print(json.dumps(out, default=repr))
'''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('tasks', nargs='+')
    ap.add_argument('--diffbehavior', action='store_true')
    ap.add_argument('--timeout', type=float, default=30)
    a = ap.parse_args(argv)
    ok_all = True
    for tid in a.tasks:
        d = FM / 'tasks' / tid.replace('/', '_')
        entry = json.loads((d / 'task.json').read_text(encoding='utf-8'))['entry_point']
        manifest = json.loads((d / 'mutants' / 'manifest.json').read_text(encoding='utf-8'))
        report = []
        for m in manifest:
            w = m.get('witness') or {}
            p = subprocess.run([sys.executable, '-I', '-c', PROBE, str(d / 'reference.py'), str(d / 'mutants' / m['file']),
                                entry, json.dumps(w.get('args', [])), str(d / 'tests.py')],
                               capture_output=True, text=True, timeout=60)
            res = json.loads(p.stdout) if p.stdout.strip() else {'error': p.stderr[-1000:]}
            checks = {
                'has_witness': bool(w),
                'reference_matches_expected': 'reference' in res and res['reference'] == w.get('expected'),
                'mutant_matches_actual': ('mutant' in res and res['mutant'] == w.get('actual'))
                                         or ('mutant_raised' in res and w.get('actual') == 'raises'),
                'expected_differs_from_actual': w.get('expected') != w.get('actual'),
            }
            valid = all(checks.values())
            ok_all &= valid
            row = {'id': m['id'], 'category': m.get('category'), 'valid': valid, **checks, 'observed': res}
            if a.diffbehavior:
                mod = lambda name: f'tasks.{d.name}.{name}'
                cmd = [sys.executable, '-m', 'crosshair', 'diffbehavior', f'{mod("reference")}.{entry}',
                       f'{mod("mutants." + Path(m["file"]).stem)}.{entry}', f'--per_condition_timeout={a.timeout}']
                db = subprocess.run(cmd, capture_output=True, text=True, cwd=FM, timeout=a.timeout * 20)
                row['diffbehavior'] = {'command': ' '.join(cmd), 'exit_code': db.returncode,
                                       'output': (db.stdout + db.stderr).strip()}
            report.append(row)
            print(f"{tid} {m['id']}: {'VALID' if valid else 'INVALID'} {checks} tests_pass={res.get('passes_official_tests')}")
        (d / 'mutants' / 'validation.json').write_text(json.dumps(report, indent=2, default=repr) + '\n', encoding='utf-8')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
