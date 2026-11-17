# Verification summary

Source: `results.jsonl` (229 jobs). MS = killed / mutants (symbolic, re-executed, discriminating against the reference). Over-restrictive = the contract rejects the reference on a legal input (symbolic x in D_T, or an official-test / witness input). Dom-excl = the precondition excludes an official-test input. MS_eff = 0 if over-restrictive, else MS. In-D kills = kills whose input is in D_T.

| task | contract | reference | over-restrictive | dom-excl | killed / mutants | in-D kills | exc | non-discr. | proven-accepted | inconclusive | err | concrete kills | MS | MS_eff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HumanEval/0 | human | INCONCLUSIVE |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/0 | qwen_v2_0_2 | INCONCLUSIVE |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/0 | qwen_v2_0_3 | INCONCLUSIVE | yes |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 0.00 |
| HumanEval/12 | human | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/12 | qwen_v2_12_2 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/12 | qwen_v2_12_3 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | human | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v1_28_1 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v1_28_2 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v1_28_3 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v2_28_1 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v2_28_2 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/28 | qwen_v2_28_3 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/40 | human | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/40 | qwen_v1_40_2 | ACCEPTED_PROVEN_BOUNDED |  |  | 0 / 6 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0.00 | 0.00 |
| HumanEval/40 | qwen_v2_40_1 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/40 | qwen_v2_40_2 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/40 | qwen_v2_40_3 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/6 | human | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/6 | qwen_v2_6_1 | REJECTED | yes |  | 3 / 6 | 0 | 0 | 3 | 0 | 0 | 0 | 2 | 0.50 | 0.00 |
| HumanEval/8 | human | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |
| HumanEval/8 | qwen_v1_8_2 | INCONCLUSIVE |  |  | 4 / 6 | 4 | 0 | 0 | 0 | 2 | 0 | 5 | 0.67 | 0.67 |
| HumanEval/8 | qwen_v1_8_3 | REJECTED | yes |  | 5 / 6 | 5 | 0 | 1 | 0 | 0 | 0 | 6 | 0.83 | 0.00 |
| HumanEval/8 | qwen_v2_8_2 | INCONCLUSIVE |  |  | 5 / 6 | 5 | 0 | 0 | 0 | 1 | 0 | 6 | 0.83 | 0.83 |
| HumanEval/8 | qwen_v2_8_3 | ACCEPTED_PROVEN_BOUNDED |  |  | 6 / 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 1.00 | 1.00 |

## Human reference contract vs. Qwen implementations

- HumanEval/0: v1_0_1=INCONCLUSIVE v1_0_2=INCONCLUSIVE v1_0_3=INCONCLUSIVE v2_0_1=INCONCLUSIVE v2_0_2=INCONCLUSIVE v2_0_3=INCONCLUSIVE
- HumanEval/12: v1_12_1=ACCEPTED_PROVEN_BOUNDED v1_12_2=ACCEPTED_PROVEN_BOUNDED v1_12_3=ACCEPTED_PROVEN_BOUNDED v2_12_1=ACCEPTED_PROVEN_BOUNDED v2_12_2=ACCEPTED_PROVEN_BOUNDED v2_12_3=ACCEPTED_PROVEN_BOUNDED
- HumanEval/28: v1_28_1=ACCEPTED_PROVEN_BOUNDED v1_28_2=ACCEPTED_PROVEN_BOUNDED v1_28_3=ACCEPTED_PROVEN_BOUNDED v2_28_1=ACCEPTED_PROVEN_BOUNDED v2_28_2=ACCEPTED_PROVEN_BOUNDED v2_28_3=ACCEPTED_PROVEN_BOUNDED
- HumanEval/40: v1_40_1=ACCEPTED_PROVEN_BOUNDED v1_40_2=ACCEPTED_PROVEN_BOUNDED v1_40_3=ACCEPTED_PROVEN_BOUNDED v2_40_1=ACCEPTED_PROVEN_BOUNDED v2_40_2=ACCEPTED_PROVEN_BOUNDED v2_40_3=ACCEPTED_PROVEN_BOUNDED
- HumanEval/6: v1_6_1=ACCEPTED_PROVEN_BOUNDED v1_6_2=REJECTED v1_6_3=ACCEPTED_PROVEN_BOUNDED v2_6_1=REJECTED v2_6_2=ACCEPTED_PROVEN_BOUNDED v2_6_3=ACCEPTED_PROVEN_BOUNDED
- HumanEval/8: v1_8_1=ACCEPTED_PROVEN_BOUNDED v1_8_2=ACCEPTED_PROVEN_BOUNDED v1_8_3=ACCEPTED_PROVEN_BOUNDED v2_8_2=ACCEPTED_PROVEN_BOUNDED v2_8_3=ACCEPTED_PROVEN_BOUNDED

## Verdict counts

- ACCEPTED_PROVEN_BOUNDED: 65
- INCONCLUSIVE: 17
- REJECTED: 141
- REJECTED_NONDISCRIMINATING: 6

## Determinate verdicts (counterexample or confirmed over all paths)

- all jobs: 212/229 = 93%
- contract x mutant: 147/150 = 98%
- contract x reference: 20/25 = 80%
- contract x Qwen implementation: 45/54 = 83%
