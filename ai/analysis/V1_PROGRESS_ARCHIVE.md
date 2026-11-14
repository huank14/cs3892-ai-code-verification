# Milestone AI progress — Qwen pilot, 2026-11-13

Owner: Jiahao Zhang. This is a completed development pilot, not the final frozen
30-task experiment. DeepSeek has NOT been called; its key configuration was
verified without displaying or archiving the key. Per the user's direction,
assess Qwen first before deciding whether a stronger model adds useful evidence.

## Implemented and executed

- API runner, exact prompt/config manifest, raw response and error retention,
  resume protection, and tests for failed-output preservation are implemented.
- Six tasks fixed before generation: HumanEval/0, /6, /8, /12, /28, /40.
- Qwen3.8-27B-FP8, walla GPU 0, vLLM 0.19.0, thinking off, 3 independent
  responses/task. All 18 requests completed with finish_reason=stop.
- Checkpoint revision: c3a462cc3d38cf351f3b26cbd763469eeb74ef81.
- Actual deployment defaults: temperature=1.0, top_p=0.95, top_k=20; context cap
  8192 tokens. No defaults were silently changed to match recommended parameters.
- A6000 uses weight-only FP8 Marlin fallback rather than native FP8 computation.
  Startup command, hardware, model config and version metadata are archived.
- No model saw human contracts, canonical solutions, hidden tests or verifier
  feedback during generation. Raw outputs are unchanged.

## Complete pilot results

| Task | Independent samples | Implementation passes official tests | CrossHair contract syntax passes after fence-only extraction |
|---|---:|---:|---:|
| /0 close elements | 3 | 3 | 0 |
| /6 nested parentheses | 3 | 3 | 0 |
| /8 sum and product | 3 | 3 | 2 |
| /12 longest string | 3 | 3 | 0 |
| /28 concatenate | 3 | 3 | 3 |
| /40 three-sum | 3 | 3 | 1 |
| Total | 18 | 18 | 6 |

Strict one-closed-code-block extraction initially accepted 11/18. Seven responses
lack a closing fence despite finish_reason=stop. For the separate implementation
and syntax audit only, copies with the opening fence removed were saved; no
Python or contract content was repaired. Five of the 11 strictly extracted
contracts parse, plus one of the seven recovered copies = six total. Preserve
both denominators rather than reporting a single ambiguous success rate.

Passing the finite official tests is not a formal correctness proof. A contract
syntax pass is not semantic correctness, CrossHair confirmation, or mutation score.

## Reproduced semantic witnesses (original contract expressions unchanged)

| Sample | Input | Candidate output | Expected output | Contract result |
|---|---|---|---|---|
| /40 response 2 | [0,0,0] | False | True | accepts wrong result |
| /8 response 3 | [2,3] | (5,1) | (5,6) | accepts wrong result |
| /8 response 3 | [0,2] | (2,0) | (2,0) | rejects correct result |
| /8 response 2 | [] | (0,999) | (0,1) | accepts wrong result |

Each witness satisfies the generated preconditions. They were replayed through
CrossHair's actual condition parser/evaluator, not an invented replacement spec.
Response /40_2 requires only `isinstance(__return__, bool)` and omits the intended
three-sum property. Response /8_3 contains tautological/product-truthiness
conditions. Response /8_2's conditional expression evaluates to numeric 1 on
empty input regardless of the product field, due to Python operator precedence.
Its missing closing fence is separately recorded as a format failure.

Thus three of the six syntactically readable contracts have concrete semantic
failures. The other three are all the concatenate task and compare the return
value with `''.join(strings)`. They look exact for this task but have NOT been
exhaustively verified or scored on a shared mutant pool.

CrossHair check of a constant-False mutant under /40_2's unchanged contract
returned Not confirmed at the fixed 60-second per-condition budget. This must
NOT be relabeled Confirmed. The concrete [0,0,0] witness independently establishes
that the contract permits that wrong return value. These are different claims.

All three /0 samples also add threshold restrictions absent from the task,
including threshold > 0 in one sample. That excludes the well-defined zero
threshold case; C/B should agree the input domain independently of model output.

## Interpretation and next step

The user's hypothesis is supported for this pilot: implementations pass the
available tests while contracts suffer compatibility and semantic problems.
This does not establish a population error rate or that all implementations
are correct. There is no evidence yet of a semantic ceiling across the benchmark.

Keep the current benchmark for now. First separate formatting from semantics:
`prompt-format-v2.txt` only adds one-line/expression-format instructions and has
NOT been run or substituted into the completed baseline. A new run must get its
own fingerprint/output directory and be reported separately. Then C/B should
validate shared mutants and correct-reference behavior to measure false rejection
and mutation sensitivity. Add DeepSeek only after that comparison protocol is
usable; its API remains uncalled.

## Milestone-ready English text

**AI pipeline and pilot**
- Qwen3.8-27B-FP8, thinking off; six fixed HumanEval tasks, three samples each.
- All prompts, settings and raw responses retained; no best-of-three selection.
- All 18 implementations passed the available official tests after fence-only
  extraction; this is testing, not proof.

**Contracts remain a challenge**
- Only 6/18 contracts parsed after fence-only extraction.
- Three of those six had reproduced semantic failures, including accepting
  incorrect outputs and rejecting correct outputs.
- Example: a three-sum contract checks only that the output is Boolean.
- Next: isolate formatting effects and evaluate shared, human-validated mutants.

## Artifacts and reproducibility

- `ai/runs/qwen-pilot/`: all 18 unedited response texts, full API responses,
  extracted code where available, request records and exact run manifest.
- `ai/evidence/qwen-complete/reviewed_pilot_audit.json`: per-sample finite-test
  and parser results, including mechanically recovered fence-only copies.
- `ai/evidence/qwen-complete/concrete_contract_witnesses.json`: exact expressions,
  values, valid-input checks and the four concrete witnesses.
- `ai/audit_reviewed_pilot.py`: rerun using the official HumanEval gzip and the
  diagnostic environment; all 18 modules and the six test bodies were manually
  reviewed before execution. Not a general-purpose sandbox for future outputs.
- `ai/check_contract_witnesses.py`: replay the semantic witnesses.
- `ai/evidence/qwen-complete/constant_false_crosshair*`: actual Not confirmed log
  and budget, not a claim of exhaustive confirmation.
- `ai/evidence/qwen-pilot/`: startup metadata, initial diagnostics and local
  diagnostic dependency freeze. macOS/Python 3.14/CrossHair 0.0.110/Z3 5.4.1;
  differs from the September Windows toy environment.
- Remote run root: /home/jiahao/cs3892-ai-pilot on walla. Generation completed;
  the independent loopback-only model service remains available for follow-up.
- Changes are local and have not been pushed to the team repository.
