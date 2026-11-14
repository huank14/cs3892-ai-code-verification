# AI → FM handoff

FM can start with the already available V1 samples while AI generation continues.
Completion of every AI sample is not a dependency for implementing the verifier,
reviewing human contracts, constructing mutants, or rehearsing the demo.

## Repository quick start

The generation runs are complete and available in this repository:

- V1 raw records: `ai/runs/qwen-pilot/`
- V2 raw records: `ai/runs/qwen-format-v2/`
- Stable sample index: `ai/analysis/samples.json`
- V2 fence-only source: `ai/evidence/qwen-format-v2/fence_only_copies/`
- Full reproduction: see `ai/README.md`; it needs no model access or API key.

From the repository root, an already prepared diagnostic environment can run:

```
python -m crosshair check ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_6_1.py --analysis_kind=PEP316 --report_all --per_condition_timeout=60
```

The `raw/`, `source/` and `samples.json` paths below describe the standalone ZIP.
Use each index entry's `repository_source` and `repository_raw_record` in a clone.

## What this handoff contains

Two separately versioned Qwen development runs, 18 attempted responses each.
`samples.json` maps stable IDs to raw request/response records and source copies.
`raw/v1` and `raw/v2` preserve full API responses, prompts and finish reasons.
`source/v1` and `source/v2` contain only fence removal, including clearly marked
recovery of missing closing fences. No PEP 316 condition was strengthened or
rewritten. `*.contract.txt` is an AST docstring extract, not a new contract.

The initial code-block extraction metric and fence-only diagnostic metric differ.
Never report a recovered sample as a perfect-format raw generation. The original
task prompts were the only task content in model requests. Evaluation-only
canonical solutions and official tests are in `data/`, clearly separated.

## Bingsong: immediate work

1. Select records with `contract_parser_status = parsed` for executable analysis.
   Keep malformed/missing contracts in the generation-failure denominator.
2. Reproduce parsing in the team environment; the AI diagnostic used Python 3.14,
   CrossHair 0.0.110 and Z3 5.4.1 on macOS, so record environment differences.
3. Run the selected implementation with the unchanged generated docstring:

```
python -m crosshair check source/v2/HumanEval_6_1.py --analysis_kind=PEP316 --report_all --per_condition_timeout=60
```

4. Put generated and human contracts onto the SAME independently validated mutant
   implementations with matching function names/signatures and required helpers.
   Keep contract helpers with the contract, and do not silently substitute model
   implementation helpers as trusted human specification logic.
5. Save every postcondition's verdict. An incorrect mutant may be admitted by a
   weak contract, but a timeout/Not confirmed is not an exhaustive confirmation.
6. Re-execute every reported counterexample. The concrete probes here are small
   behavioral witnesses, not CrossHair's full benchmark mutation score.

## Zoey: evaluation decisions

- Freeze the final 30-task eligibility and input domains independently of outputs.
- Cross-check Keyu's human reference requirements and edge cases. A contract
  rejecting every output should not score as strong.
- Build a shared per-task mutant pool validated against the TASK/reference, not
  merely against model-generated code. The AI pilot has not completed this pool.
- Agree how per-postcondition verdicts become a contract–mutant verdict, how
  malformed samples enter denominators, and how three samples aggregate per task.
- The six pilot tasks were purpose-selected during development, not a random
  representative sample. The V2 prompt was designed after V1 format inspection.

## Keyu: human reference specifications and integration

- Lead the six pilot reference contracts: write the task requirements checklist,
  then encode and review PEP 316 conditions. If an LLM assists, record its role
  and label the baseline accurately. Keep these references separate from the
  Qwen contracts being evaluated. Bingsong checks tool compatibility and Zoey
  checks boundary coverage. Expand to 30 tasks for the final evaluation.


- Integrate raw records, source mapping and reproducibility commands into the team
  repository with reviewed artifacts. The AI materials are provided in this commit.
- Use the exact saved generations for the milestone demo. Live API resampling is
  unnecessary and would produce a new observation.
- The pilot used walla loopback port 18392. The independently started service
  was stopped after both runs to release GPU memory. Credentials are outside
  this handoff. DeepSeek remains unused for this milestone contribution.

## AI milestone contribution versus the full project

This completes the AI pilot, prompt comparison, reproducible generation artifacts,
concrete specification-quality diagnostics, speaker notes and presentation section.
The full 30-task/two-model evaluation, shared-mutant mutation scores and human–LLM
score gap are still team work. They are not claimed as completed here.
