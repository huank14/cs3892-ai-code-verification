# Qwen prompt comparison

Same six tasks and deployment. Three fresh samples per task per prompt. No seed matching.

| Metric | V1 | V2 |
|---|---:|---:|
| Returned responses | 18/18 | 18/18 |
| Strict extracted code–contract pairs | 11/18 | 12/18 |
| Implementation official-test passes after fence-only extraction | 18/18 | 17/18 |
| Readable explicit contracts after fence-only extraction | 6/18 | 13/18 |
| Contracts with an observed semantic failure, among readable contracts | 3/6 | 2/13 |

Observed failures are lower bounds from finite probes, not estimates of all semantic errors. Syntax-invalid samples were not silently repaired.

| Task | V1 readable | V2 readable |
|---|---:|---:|
| HumanEval/0 | 0/3 | 2/3 |
| HumanEval/6 | 0/3 | 1/3 |
| HumanEval/8 | 2/3 | 2/3 |
| HumanEval/12 | 0/3 | 2/3 |
| HumanEval/28 | 3/3 | 3/3 |
| HumanEval/40 | 1/3 | 3/3 |

Implementation test passes are not proofs. Output perturbations are not a shared-mutant benchmark. The small development sample does not establish a causal prompt effect or a general model ranking.
