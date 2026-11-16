"""Create fm/tasks/HumanEval_<n>/ from the evaluation-only HumanEval file.

Writes reference.py (prompt + canonical solution), tests.py (official check()),
task.json, and an empty mutants/manifest.json. Never overwrites existing files.
Usage (from fm/): .venv/Scripts/python -m pipeline.make_tasks HumanEval/0 HumanEval/6 ...
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

FM = Path(__file__).resolve().parent.parent
DATA = FM.parent / 'ai/data/eval-only-human-eval-pilot.jsonl.gz'


def write_new(path: Path, text: str) -> None:
    if path.exists():
        print(f'keep   {path.relative_to(FM)}')
        return
    path.write_text(text, encoding='utf-8')
    print(f'create {path.relative_to(FM)}')


def main(task_ids: list[str], data: Path = DATA) -> None:
    rows = {r['task_id']: r for r in map(json.loads, gzip.open(data, 'rt', encoding='utf-8'))}
    for tid in task_ids:
        r = rows[tid]
        d = FM / 'tasks' / tid.replace('/', '_')
        (d / 'mutants').mkdir(parents=True, exist_ok=True)
        write_new(d / 'reference.py', '# HumanEval canonical solution (MIT licence, openai/human-eval).\n'
                  + r['prompt'] + r['canonical_solution'])
        write_new(d / 'tests.py', '# Official HumanEval tests (evaluation only).\n' + r['test'])
        write_new(d / 'task.json', json.dumps({'task_id': tid, 'entry_point': r['entry_point'],
                                               'source': 'openai/human-eval',
                                               'dataset_file': DATA.relative_to(FM.parent).as_posix()}, indent=2) + '\n')
        write_new(d / 'mutants' / 'manifest.json', '[]\n')


if __name__ == '__main__':
    main(sys.argv[1:])
