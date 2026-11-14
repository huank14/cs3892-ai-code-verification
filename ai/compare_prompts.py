"""Build descriptive comparison tables from archived evidence, with denominators."""
import argparse
from collections import Counter
import json
from pathlib import Path


def load_version(run, evidence):
    records = [json.loads(p.read_text()) for p in run.glob('HumanEval_*.json')
               if not p.name.endswith('.response.json')]
    audit = json.loads((evidence / 'reviewed_pilot_audit.json').read_text())
    probes = json.loads((evidence / 'semantic_probes.json').read_text())
    n = len(records)
    return {'attempts': n, 'task_count': len({r['task_id'] for r in records}),
            'responses_received': sum(r['status'] == 'response_received' for r in records),
            'strict_extracted_pairs': sum(r.get('extraction', {}).get('status') == 'extracted' for r in records),
            'strict_code_blocks': sum(r.get('extraction', {}).get('status') not in (None, 'format_error') for r in records),
            'implementation_test_passes': audit['implementation_test_passes_after_fence_only_extraction'],
            'readable_contracts': audit['contract_syntax_passes_after_fence_only_extraction'],
            'parser_status_counts': dict(Counter(r.get('contract_parser_status', r.get('status')) for r in audit['rows'])),
            'semantic_failure_contracts': probes['contracts_with_observed_semantic_failure'],
            'semantic_probe_eligible': probes['eligible_contracts'],
            'semantic_runtime_error_contracts': probes['contracts_with_runtime_errors'],
            'samples_with_observed_semantic_failure': [r['sample'] for r in probes['rows'] if r['observed_semantic_failure']],
            'audit_rows': audit['rows']}


def main(args):
    root = Path(args.root)
    versions = {
        'v1': load_version(Path(args.v1_run) if args.v1_run else root / 'runs/qwen-pilot',
                           Path(args.v1_evidence) if args.v1_evidence else root / 'evidence/qwen-complete'),
        'v2': load_version(Path(args.v2_run) if args.v2_run else root / 'runs/qwen-format-v2',
                           Path(args.v2_evidence) if args.v2_evidence else root / 'evidence/qwen-format-v2'),
    }
    # Never label a partial run as the requested completed comparison.
    assert all(v['attempts'] == 18 and v['task_count'] == 6 and len(v['audit_rows']) == 18 for v in versions.values())
    result = {'scope': 'completed development pilot, descriptive comparison only', 'versions': versions}
    target = root / 'analysis/prompt_comparison.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Qwen prompt comparison', '', 'Same six tasks and deployment. Three fresh samples per task per prompt. No seed matching.', '',
             '| Metric | V1 | V2 |', '|---|---:|---:|']
    metrics = [('Returned responses', 'responses_received'), ('Strict extracted code–contract pairs', 'strict_extracted_pairs'),
               ('Implementation official-test passes after fence-only extraction', 'implementation_test_passes'),
               ('Readable explicit contracts after fence-only extraction', 'readable_contracts')]
    for label, key in metrics:
        lines.append(f"| {label} | {versions['v1'][key]}/18 | {versions['v2'][key]}/18 |")
    lines.append('| Contracts with an observed semantic failure, among readable contracts | ' +
                 ' | '.join(f"{v['semantic_failure_contracts']}/{v['semantic_probe_eligible']}" for v in versions.values()) + ' |')
    lines += ['', 'Observed failures are lower bounds from finite probes, not estimates of all semantic errors. Syntax-invalid samples were not silently repaired.', '',
              '| Task | V1 readable | V2 readable |', '|---|---:|---:|']
    for i in [0, 6, 8, 12, 28, 40]:
        task = f'HumanEval/{i}'
        vals = [sum(r.get('contract_parser_status') == 'parsed' for r in v['audit_rows'] if r.get('task_id') == task) for v in versions.values()]
        lines.append(f'| {task} | {vals[0]}/3 | {vals[1]}/3 |')
    lines += ['', 'Implementation test passes are not proofs. Output perturbations are not a shared-mutant benchmark. The small development sample does not establish a causal prompt effect or a general model ranking.', '']
    (root / 'analysis/PROMPT_COMPARISON.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='ai')
    p.add_argument('--v1-run')
    p.add_argument('--v2-run')
    p.add_argument('--v1-evidence')
    p.add_argument('--v2-evidence')
    main(p.parse_args())
