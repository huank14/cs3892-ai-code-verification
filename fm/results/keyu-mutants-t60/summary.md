# Verification summary

Source: `results.jsonl` (36 jobs). MS = killed / mutants (symbolic, re-executed, discriminating against the reference). Over-restrictive = the contract rejects the reference (symbolically or on an official-test input).

| task | contract | reference | over-restrictive | killed / mutants | exc | non-discr. | proven-accepted | inconclusive | err | concrete kills | MS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HumanEval/0 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |
| HumanEval/12 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |
| HumanEval/28 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |
| HumanEval/40 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |
| HumanEval/6 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |
| HumanEval/8 | human |  |  | 6 / 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 |

## Verdict counts

- REJECTED: 36

## Determinate verdicts (counterexample or confirmed over all paths)

- all jobs: 36/36 = 100%
- contract x mutant: 36/36 = 100%
