"""Summarize generation compatibility, never semantic correctness."""
import argparse
from collections import Counter
import json
from pathlib import Path


def summarize(directory):
    records = []
    for path in Path(directory).glob('HumanEval_*.json'):
        if path.name.endswith('.response.json'):
            continue
        records.append(json.loads(path.read_text()))
    return {'attempts': len(records),
            'tasks_attempted': len({r['task_id'] for r in records}),
            'transport_status': dict(Counter(r['status'] for r in records)),
            'extraction_status': dict(Counter(r.get('extraction', {}).get('status', 'no_response') for r in records)),
            'finish_reasons': dict(Counter(str(r.get('finish_reason')) for r in records)),
            'semantic_correctness': 'not measured',
            'crosshair_verdicts': 'not measured',
            'mutation_score': 'not measured'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('directory')
    args = p.parse_args()
    print(json.dumps(summarize(args.directory), indent=2))
