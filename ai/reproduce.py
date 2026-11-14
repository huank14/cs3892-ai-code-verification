"""Reproduce the reviewed 36-sample pilot without model access or API keys."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main(args):
    repo = Path(__file__).resolve().parent.parent
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output/'analysis').mkdir(exist_ok=True)
    dataset = str(repo/'ai/data/eval-only-human-eval-pilot.jsonl.gz')
    evidence = {}
    runs = {'v1': repo/'ai/runs/qwen-pilot', 'v2': repo/'ai/runs/qwen-format-v2'}
    for version, run in runs.items():
        evidence[version] = output/version
        for command in [
            ['ai/audit_reviewed_pilot.py', '--run', str(run), '--output', str(evidence[version]), '--dataset', dataset],
            ['ai/probe_contracts.py', '--audit-directory', str(evidence[version]), '--dataset', dataset],
        ]:
            subprocess.run([sys.executable]+command, cwd=repo, check=True)
    subprocess.run([sys.executable, 'ai/compare_prompts.py', '--root', str(output),
                    '--v1-run', str(runs['v1']), '--v2-run', str(runs['v2']),
                    '--v1-evidence', str(evidence['v1']), '--v2-evidence', str(evidence['v2'])],
                   cwd=repo, check=True)
    expected = json.loads((repo/'ai/analysis/prompt_comparison.json').read_text())
    actual = json.loads((output/'analysis/prompt_comparison.json').read_text())
    for version in ['v1', 'v2']:
        for key in ['attempts', 'responses_received', 'strict_extracted_pairs',
                    'implementation_test_passes', 'readable_contracts',
                    'semantic_failure_contracts', 'semantic_probe_eligible']:
            if actual['versions'][version][key] != expected['versions'][version][key]:
                raise SystemExit(f'Reproduction mismatch: {version} {key}')
    print('All archived headline counts reproduced. Results:', output)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='ai/reproduced')
    main(p.parse_args())
