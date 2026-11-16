# Verification summary

Source: `results.jsonl` (6 jobs). MS = killed / mutants (symbolic, re-executed, discriminating against the reference). Over-restrictive = the contract rejects the reference (symbolically or on an official-test input).

| task | contract | reference | over-restrictive | killed / mutants | exc | non-discr. | proven-accepted | inconclusive | err | concrete kills | MS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HumanEval/0 | human | INCONCLUSIVE |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/12 | human | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | human | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/40 | human | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/6 | human | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/8 | human | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |

## Verdict counts

- ACCEPTED_PROVEN_BOUNDED: 5
- INCONCLUSIVE: 1

## Determinate verdicts (counterexample or confirmed over all paths)

- all jobs: 5/6 = 83%
- contract x reference: 5/6 = 83%
