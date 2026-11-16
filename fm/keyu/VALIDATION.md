# Human reference validation — six-task milestone pilot

**Date:** November 16, 2026  
**Archived source base:** `80429feb9e2114280323ff9f53eb3f622c0c26af`

This document summarizes the recorded CrossHair validation of Keyu Huang's six
human-reviewed reference contracts. Detailed provenance and semantic-review status are in
[`PROVENANCE.md`](PROVENANCE.md).

## Observed results

Six reference contracts were evaluated against the canonical HumanEval implementations
and the six validated mutants for each pilot task.

| Task | Canonical implementation | Recorded seconds | Concrete official/witness checks | Mutants caught | Mutant inconclusive | Errors |
|---|---|---:|---:|---:|---:|---:|
| HumanEval/0 | `INCONCLUSIVE` | 250.08 | 13, all pass | 6/6 | 0 | 0 |
| HumanEval/6 | `ACCEPTED_PROVEN_BOUNDED` | 127.23 | 9, all pass | 6/6 | 0 | 0 |
| HumanEval/8 | `ACCEPTED_PROVEN_BOUNDED` | 120.97 | 11, all pass | 6/6 | 0 | 0 |
| HumanEval/12 | `ACCEPTED_PROVEN_BOUNDED` | 61.90 | 9, all pass | 6/6 | 0 | 0 |
| HumanEval/28 | `ACCEPTED_PROVEN_BOUNDED` | 67.00 | 9, all pass | 6/6 | 0 | 0 |
| HumanEval/40 | `ACCEPTED_PROVEN_BOUNDED` | 121.92 | 15, all pass | 6/6 | 0 | 0 |

Summary:

- 5/6 canonical implementations: `ACCEPTED_PROVEN_BOUNDED`;
- HumanEval/0 canonical implementation: `INCONCLUSIVE`;
- canonical-reference rejections: 0;
- shared mutants evaluated: 36;
- mutants rejected by replayed, discriminating CrossHair counterexamples: 36/36;
- mutant inconclusive/error outcomes: 0.

The recorded seconds are whole job durations. The configured 60 s value is a
**per-condition search budget**, not a total wall-clock limit for an entire job.

The 66 concrete cases in `result_audit.json` are official-test and mutant-witness calls
used as additional checks. They are tested cases, not a formal proof and not necessarily
66 distinct inputs.

## Recorded commands

The archived runs were produced from `fm/` with:

```bash
.venv/bin/python -m pipeline.run_matrix   --tasks all --contracts human --kinds reference   --timeout 60 --workers 6 --mode combined --contract-signature   --out results/keyu-reference-t60

.venv/bin/python -m pipeline.run_matrix   --tasks all --contracts human --kinds mutant   --timeout 60 --workers 12 --mode combined --contract-signature   --out results/keyu-mutants-t60
```

The archived `run_meta.json` files record Python 3.12.14, CrossHair 0.0.110,
Z3 5.1.0, Linux, analysis bounds, timestamps, and the source-base commit.

## What counts as a caught mutant

For legal input domain \(D\), contract \(c\), mutant \(m\), and canonical reference
`ref`, this pilot counts a mutant as caught only when CrossHair supplies a witness \(x\)
such that:

```text
x is in D
pre_c(x) holds
post_c(x, m(x)) is false
post_c(x, ref(x)) is true
```

and concrete replay reproduces the distinction.

For one contract \(c\):

```text
MS(c) = caught validated mutants / all validated mutants for the task
```

Each pilot task has six validated mutants. The descriptive caught fraction for each
human-reviewed contract is therefore 6/6, and the pooled descriptive count is 36/36.

This pilot result is mutant-set dependent and must not be interpreted as complete
specification coverage.

## Canonical-reference interpretation

A human reference contract is not treated as valid merely because it catches mutants.
It must also avoid rejecting the correct implementation on the frozen legal input domain.

No canonical-reference rejection was observed in this pilot.

Five tasks reached `ACCEPTED_PROVEN_BOUNDED`. This means CrossHair confirmed the
conditions inside the declared small-scope analysis bound; it is not an unrestricted
correctness proof.

HumanEval/0 remained `INCONCLUSIVE` in both bounded and unbounded search. The result is
reported as inconclusive rather than upgraded to correctness.

## Semantic review

The six final contracts were reviewed against:

- the original HumanEval task statement;
- the frozen task-specific input domain;
- the canonical implementation;
- applicable empty-input, boundary, duplicate, ordering, and tie-breaking behavior.

No substantive semantic change was required after this review. The task-specific
semantic points are recorded in `PROVENANCE.md` and each task's `human_contract.md`.

## Archived evidence

The compact evidence retained in the repository is:

```text
results/keyu-reference-t60/
    results.jsonl
    run_meta.json
    summary.csv
    summary.md

results/keyu-mutants-t60/
    results.jsonl
    run_meta.json
    summary.csv
    summary.md
```

Supporting audit files in `keyu/` are:

- `mutant_results.csv`;
- `result_audit.json`;
- `source_manifest.json`;
- `revision_manifest.json`;
- `revision_replay.json`;
- `replay_evidence.py`.

Raw CrossHair text logs are intentionally omitted. The structured JSONL records preserve
the verdict and counterexample information used for the summaries.

## Revision integrity and replay

The archived symbolic runs were made before a comment-only cleanup of the six contract
files. `revision_manifest.json` records both hashes and confirms identical executable ASTs,
including the PEP 316 contract docstrings.

The current reviewed contracts can replay the archived witnesses with:

```bash
.venv/bin/python -m keyu.replay_evidence   --out results/keyu-replay/replay.json
```

`revision_replay.json` records the completed revision check:

```text
checks: 36
passed: 36
```

This is concrete replay of previously archived symbolic counterexamples, not a new
CrossHair search, and it does not upgrade any original verdict.

## Worked example: HumanEval/12 tie-breaking

One archived counterexample for the mutant that returns the **last** longest string is:

```text
longest(['\x00', '\x01'])
mutant -> '\x01'
reference -> '\x00'
```

Both strings have length one. The task requires the first maximum-length string, so the
mutant violates the reference contract while the canonical implementation satisfies it.

A readable classroom example such as `['aa', 'bb'] -> 'aa'` illustrates the same
requirement, but it should not be presented as the recorded symbolic witness.

## Current limitations and remaining team work

- The six pilot tasks were purpose-selected; these results are descriptive, not a
  population estimate for HumanEval.
- The mutation score depends on the frozen mutant set; 36/36 does not imply that every
  possible implementation error would be detected.
- HumanEval/0 remains inconclusive and must stay reported that way.
- The aligned human-vs-LLM mutation-score comparison is pending the shared-mutant,
  shared-domain pipeline run under the agreed evaluation protocol.
- The project-level evaluation protocol is maintained separately in
  `../EVALUATION_PROTOCOL.md`; this document does not independently redefine its
  aggregation rules.

## Milestone evidence supported by this package

This package provides:

- six human-reviewed PEP 316 reference contracts;
- real CrossHair output summarized in machine-readable records;
- replayed, discriminating counterexamples for the 36 observed mutant rejections;
- explicit bounded/inconclusive distinctions;
- run metadata and reproduction commands;
- source/revision manifests connecting the archived run to the reviewed contract files.

These artifacts support the milestone's verifier, technical-depth, and
repository/reproducibility requirements. They do not by themselves constitute the full
team milestone presentation or final 30-task evaluation.
