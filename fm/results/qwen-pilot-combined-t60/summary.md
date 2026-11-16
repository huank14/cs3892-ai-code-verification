# Verification summary

Source: `results.jsonl` (38 jobs). MS = killed / mutants (symbolic, re-executed, discriminating against the reference). Over-restrictive = the contract rejects the reference (symbolically or on an official-test input).

| task | contract | reference | over-restrictive | killed / mutants | exc | non-discr. | proven-accepted | inconclusive | err | concrete kills | MS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HumanEval/0 | qwen_v2_0_2 | INCONCLUSIVE |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/0 | qwen_v2_0_3 | INCONCLUSIVE | yes | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/12 | qwen_v2_12_2 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/12 | qwen_v2_12_3 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v1_28_1 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v1_28_2 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v1_28_3 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v2_28_1 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v2_28_2 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/28 | qwen_v2_28_3 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/40 | qwen_v1_40_2 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/40 | qwen_v2_40_1 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/40 | qwen_v2_40_2 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/40 | qwen_v2_40_3 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/6 | qwen_v2_6_1 | REJECTED | yes | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/8 | qwen_v1_8_2 | INCONCLUSIVE |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/8 | qwen_v1_8_3 | REJECTED | yes | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/8 | qwen_v2_8_2 | INCONCLUSIVE |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| HumanEval/8 | qwen_v2_8_3 | ACCEPTED_PROVEN_BOUNDED |  | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |

## Verdict counts

- ACCEPTED_PROVEN_BOUNDED: 28
- INCONCLUSIVE: 6
- REJECTED: 2
- REJECTED_NONDISCRIMINATING: 2

## Determinate verdicts (counterexample or confirmed over all paths)

- all jobs: 32/38 = 84%
- contract x reference: 15/19 = 79%
- contract x Qwen implementation: 17/19 = 89%
