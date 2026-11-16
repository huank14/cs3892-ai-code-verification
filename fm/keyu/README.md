# Keyu: human-reviewed reference contracts and pilot reproduction

This directory documents Keyu Huang's six-task milestone contribution: human-reviewed
PEP 316 reference contracts, their CrossHair validation, and the evidence needed to
reproduce the reported pilot results.

AI-assistance and semantic-review provenance are recorded once in
[`PROVENANCE.md`](PROVENANCE.md).

## Pilot tasks

| HumanEval task | Entry point | Reference contract |
|---|---|---|
| /0 | `has_close_elements` | `../tasks/HumanEval_0/human_contract.py` |
| /6 | `parse_nested_parens` | `../tasks/HumanEval_6/human_contract.py` |
| /8 | `sum_product` | `../tasks/HumanEval_8/human_contract.py` |
| /12 | `longest` | `../tasks/HumanEval_12/human_contract.py` |
| /28 | `concatenate` | `../tasks/HumanEval_28/human_contract.py` |
| /40 | `triples_sum_to_zero` | `../tasks/HumanEval_40/human_contract.py` |

Each task also has a concise requirement note in `human_contract.md`. The task
directories already contain the team-owned canonical implementation, frozen input
domain, analysis bound, and validated mutants. Those files are not redefined here.

## Environment

From the repository root:

```bash
python3 -m venv fm/.venv
fm/.venv/bin/python -m pip install -r fm/requirements.txt
cd fm
```

On Windows, use `.venv/Scripts/python` instead of `.venv/bin/python`.

The archived runs used:

- Python 3.12.14
- CrossHair 0.0.110
- Z3 5.1.0
- Linux
- 60 s per-condition timeout
- combined mode with `--contract-signature`

Exact commands, versions, analysis bounds, timestamps, and the source-base commit are
stored in each run's `run_meta.json`.

## Reproduce the pilot checks

Run from `fm/`. Use fresh output directories so the archived records remain unchanged.

```bash
# Six reference-implementation checks
.venv/bin/python -m pipeline.run_matrix   --tasks all --contracts human --kinds reference   --timeout 60 --workers 6 --mode combined --contract-signature   --out results/keyu-reference-reproduction

# Thirty-six shared-mutant checks
.venv/bin/python -m pipeline.run_matrix   --tasks all --contracts human --kinds mutant   --timeout 60 --workers 12 --mode combined --contract-signature   --out results/keyu-mutants-reproduction
```

At the recorded milestone source base, `--tasks all` referred to the six pilot tasks
listed above.

Expected recorded pilot outcome:

- reference checks: 5 `ACCEPTED_PROVEN_BOUNDED`, 1 `INCONCLUSIVE` (HumanEval/0);
- reference rejections: 0;
- mutant checks: 36 `REJECTED`;
- replayed, discriminating, in-domain mutant counterexamples: 36/36.

`ACCEPTED_PROVEN_BOUNDED` is a bounded CrossHair result, not an unrestricted
correctness claim. `INCONCLUSIVE` is retained as inconclusive.

## Archived evidence

The compact archived result sets are:

```text
../results/keyu-reference-t60/
    results.jsonl
    run_meta.json
    summary.csv
    summary.md

../results/keyu-mutants-t60/
    results.jsonl
    run_meta.json
    summary.csv
    summary.md
```

Raw CrossHair text logs are intentionally not retained in this contribution. The
machine-readable `results.jsonl` records contain the structured verdicts, reported
counterexamples, replay information, pre/post evaluations, and canonical-reference
returns used by the summaries.

Additional audit files:

- `mutant_results.csv` — concise 36-row mutant result table;
- `result_audit.json` — sidecar audit of verdicts, concrete checks, legal-domain status,
  and discriminating replays;
- `source_manifest.json` — hashes of the original source inputs used for the archived run;
- `revision_manifest.json` — maps the archived contract hashes to the reviewed files and
  records identical executable ASTs after comment-only cleanup;
- `revision_replay.json` — concrete replay of all 36 archived symbolic counterexamples
  against the reviewed files.

## Replay archived counterexamples

To replay the saved mutant witnesses without running a new symbolic search:

```bash
.venv/bin/python -m keyu.replay_evidence   --out results/keyu-replay/replay.json
```

Expected result:

```text
36 checks, 36 passed
```

`replay_evidence.py` regenerates temporary composed modules using the existing pipeline,
checks that each witness lies in the frozen legal domain, reruns the mutant and canonical
reference, and compares the returns with the archived record.

## Verdict interpretation

| Verdict | Meaning in this pilot |
|---|---|
| `REJECTED` on a mutant | CrossHair found a counterexample; the saved witness was replayed and discriminates the mutant from the canonical reference. |
| `REJECTED` on the reference | Would indicate a specification/domain/helper/tool/reference mismatch and must not be counted as successful mutation detection. None occurred in this pilot. |
| `ACCEPTED_PROVEN_BOUNDED` | Conditions were confirmed inside the declared analysis bound. This is not an unrestricted proof. |
| `INCONCLUSIVE` | No decisive result was obtained within the search budget. HumanEval/0 has this reference verdict. |

The project-level evaluation protocol in `../EVALUATION_PROTOCOL.md` defines how these
verdicts enter mutation-score reporting.

## Revision integrity

The six reviewed contracts required no substantive semantic changes. A non-executable
provenance comment was removed from each contract after the archived run. The resulting
file hashes therefore differ from the original run hashes.

`revision_manifest.json` records the before/after hashes and confirms that the executable
ASTs, including the PEP 316 contract docstrings, are identical. `revision_replay.json`
records 36/36 successful concrete replays of the archived symbolic counterexamples against
the reviewed files.

No new symbolic run was substituted for an unfavorable archived result.

## Pilot scope and limitations

The six tasks were purpose-selected for the milestone, and the current mutant set does not
cover every possible implementation error. The observed 36/36 caught-mutant result is
therefore descriptive of this pilot only.

An aligned human-vs-LLM mutation-score comparison requires the LLM contracts to be run
against the same frozen input domains and shared mutant pool under the agreed team
evaluation protocol. That comparison is separate team work and is not fabricated here.
