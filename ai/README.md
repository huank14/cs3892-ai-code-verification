# AI component — Jiahao

Completed two-prompt development pilot, separate from the final frozen 30-task evaluation.
See `MILESTONE_AI.md` for measured results and `FM_HANDOFF.md` for team integration.

## Use the saved results (no API or GPU required)

- [Pilot results and limitations](MILESTONE_AI.md)
- [Prompt comparison table](analysis/PROMPT_COMPARISON.md)
- [FM handoff and current responsibilities](FM_HANDOFF.md)
- [Sample index](analysis/samples.json), with repository and standalone-bundle paths
- [Standalone handoff ZIP](milestone-output/AI-FM-handoff.zip)

Raw outputs: `runs/qwen-pilot/` (V1) and `runs/qwen-format-v2/` (V2).
Fence-only diagnostic source copies: `evidence/qwen-complete/fence_only_copies/`
and `evidence/qwen-format-v2/fence_only_copies/`. These are exact generated
Python/contract content with only Markdown fences removed, not repaired specs.
Some archived outputs intentionally contain syntax errors and must remain unchanged.

To reproduce all headline counts from a fresh clone, use Python 3.14 to match the
archived diagnostic environment. From the repository root on macOS/Linux:

```
python3.14 -m venv .venv-ai
.venv-ai/bin/python -m pip install -r ai/requirements-diagnostic.txt
.venv-ai/bin/python ai/reproduce.py
```

On Windows, replace `.venv-ai/bin/python` with `.venv-ai/Scripts/python.exe`.
Outputs go to ignored `ai/reproduced/`; the archived evidence is preserved.
All 36 modules and six official test bodies were reviewed before this audit;
the scripts are not a sandbox for future unreviewed model outputs.

## Generate new responses (optional)

Python 3.10+ standard library only. Run from the repository root.

```
python3 ai/generate.py --config ai/configs/qwen.json --output ai/runs/qwen-pilot
python3 ai/summarize.py ai/runs/qwen-pilot
python3 ai/generate.py --config ai/configs/qwen.json --prompt ai/prompt-format-v2.txt --output ai/runs/qwen-format-v2
```

The Qwen URL is loopback on walla, port 18392. Run on walla alongside the
independently started service, or use an SSH tunnel and a separate run config.
No existing service is replaced. See the archived runtime metadata for actual
model revision, hardware, startup command, library versions, and defaults.

DeepSeek uses an environment variable (never paste the key into tracked files):

```
python3 ai/generate.py --config ai/configs/deepseek.json --output ai/runs/deepseek-pilot
```

This command requires `DEEPSEEK_API_KEY` already set. The key is now configured in the walla user-level file `~/.config/deepseek.env`.
Source that file only in the calling shell. No DeepSeek calls have been made;
the current decision is to evaluate Qwen first. `deepseek-flash` is a mutable provider alias:
on 2026-11-13 the provider documents DeepSeek-V4.1-Flash-1017, which differs
from the September proposal snapshot. Archive request date and response model;
the response model field may itself be an alias and is not a weight hash.

## Protocol

- Six task IDs and selection rationale are frozen in `tasks/pilot_manifest.json`
  before observing generations. These tasks probe different specification
  requirements; they are not a statistically representative difficulty sample.
- Each task has three independent, fresh conversations per model. No best-of-three
  selection, repair, verifier feedback, or human contract in the prompt.
- Preserve task prompt, full API response, extracted source, request parameters,
  usage, finish reason, elapsed time, errors, and model identifiers.
- HTTP errors and malformed outputs remain in the run. Resuming skips them as well
  as successful outputs; it never silently requests a replacement.
- Existing run directories reject config/task/prompt/runner changes. Use a new
  output directory for an intentionally different protocol.
- AST parsing does not execute generated code. `extracted` means source plus
  target function plus a postcondition were found; it is not a correctness or
  CrossHair-compatibility verdict. Empty `pre:` is permitted by the format.
- API credentials and authorization headers are never stored. Only the two reviewed pilot runs are published. New run directories remain
  ignored until separately reviewed.
- Unspecified API sampling values are recorded as provider-managed unknowns;
  they must not be reported as measured defaults. Qwen's local generation config
  is archived. Any server-enforced output cap must be recorded, including truncation.

## Handoff

Jiahao owns requests and unedited outputs. Bingsong checks contract compatibility,
verdicts and re-executes counterexamples. Zoey owns validated mutants, the shared evaluation domain and metric
aggregation. Keyu leads the human reference specifications (documenting any LLM
assistance), batch orchestration and artifact integration. Bingsong checks tool
compatibility and Zoey cross-checks the reference requirements and edge cases. A parser failure cannot be silently
corrected into a stronger contract.

## Validation

```
python3 -m unittest discover -s ai -p 'test_*.py' -v
```

Tests use a local fixture service, not a model. They check that failed/malformed
samples survive resume, raw output is retained, and changed prompts cannot mix
with old runs. Actual model results are separate from these fixture tests.
