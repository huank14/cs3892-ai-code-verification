# Milestone 1 — AI contribution

Jiahao Zhang, Group E, CS 3892 / 5892. Completed development pilot, 13 November 2026.

## Question

Can a model that writes implementations passing available tests still generate
contracts that are unusable, too weak, or overly restrictive? Does a format-only
prompt change improve the practical usability of its contracts?

## What I built

A resumable OpenAI-compatible generation runner, versioned prompts, exact run
manifests, raw-output archives, and diagnostic scripts. All responses are retained,
including malformed code and contracts. No best-of-three selection or contract
strengthening is used. The pipeline generates a Python implementation with a
PEP 316 docstring contract. AI4FM generates specifications; FM4AI analyzes the
resulting programs. Human reference contracts and hidden evaluation material
were not supplied in prompts.

## Experimental setup

- Qwen/Qwen3.8-27B-FP8, thinking disabled, vLLM 0.19.0 on walla GPU 0.
- Checkpoint c3a462cc3d38cf351f3b26cbd763469eeb74ef81.
- Actual deployment defaults: temperature 1.0, top-p 0.95, top-k 20. Context cap 8192.
- Six fixed HumanEval tasks: /0, /6, /8, /12, /28, /40. Three fresh conversations
  per task per prompt. Two prompts, 36 total responses, no seed matching.
- V1 asks for executable PEP 316 conditions. V2 additionally requests each complete
  condition on one physical line and expressions instead of if/else statements.
  Model, task prompts, ordering and generation settings remain the same.
- The six tasks were selected for development before V1 generation. V2 was designed
  after inspecting V1 format errors. Semantic probes were developed during pilot
  inspection and applied in their final identical form to both versions.
- No DeepSeek requests were made. Its credentials are configured outside artifacts.

## Results

| Metric | V1 | V2 |
|---|---:|---:|
| Returned responses | 18/18 | 18/18 |
| Strict extracted code–contract pairs | 11/18 | 12/18 |
| Implementation passes official tests after fence removal | 18/18 | 17/18 |
| Explicit contracts parse after fence removal | 6/18 | 13/18 |
| Readable contracts with observed semantic failures | 3/6 | 2/13 |

Seven V1 and four V2 responses lack a closing code fence. Diagnostic copies remove
only fences, preserving all Python and contract text. They are distinct from raw
perfect-format outputs. V2's five non-readable results comprise three PEP 316
syntax failures, one missing docstring postcondition, and one invalid Python
module. The single V2 implementation failure is a syntax failure caused by contract
text placed in the function body. V1's twelve non-readable contracts have syntax
errors. The final finite probe suite produced no runtime errors on these cases.

Metric definitions:

- Parser compatibility = readable explicit contracts / 18 attempted responses.
- Implementation pass = passing the task's finite official tests; not a proof.
- An observed semantic failure is a concrete witness of unwanted valid-input
  exclusion, false rejection of a reference output, or acceptance of a wrong output.
- False acceptance: for valid x, pre(x) and post(x,r) hold while r != f*(x), where
  f* is the canonical reference behavior. False rejection: pre(x) holds but
  post(x,f*(x)) is false. No observed witness does not prove correctness.

The counts are descriptive and are not statistical evidence of a general prompt
ranking. In particular, 3/6 versus 2/13 has different eligible denominators and
must not be advertised as a measured improvement in population semantic accuracy.
No benchmark mutation score or LLM–human 15-point comparison has been completed.

## Main V2 semantic case

Sample v2/HumanEval_6_1 returns a list of maximum parentheses nesting depths.
Its generated contract only requires a list of integers, matching group count,
and nonnegative entries. For input '(())', the reference result is [2], but [0]
satisfies all unchanged generated pre/postconditions. The contract omits the
actual depth requirement. This is a concrete reproducible false-acceptance case.

Sample v2/HumanEval_0_3 imposes threshold > 0, excluding well-defined zero-threshold
inputs. It also uses `b is not a` inside the pair comparison, confusing Python
object identity with distinct positions. With the same floating object repeated
in the input, a correct True result can be rejected. Input alias groups are
recorded because ordinary JSON values do not preserve object identity.

The V1 examples remain archived: a three-sum contract requiring only Boolean
output; a product contract allowing a wrong nonzero product and rejecting a
correct zero product; and an empty-product condition with incorrect precedence.

A symbolic CrossHair diagnostic for a zero-depth mutant with the unchanged V2
contract returned Not confirmed at all four postconditions under the fixed
60-second per-condition budget. That is inconclusive, not a proof the mutant
passes. The concrete witness independently shows the missing constraint.

## Interpretation and next work

Format instructions were associated with more readable contracts in this run,
but did not ensure valid syntax or complete semantics. This pilot supplies real
specification-quality failures without changing to harder programming tasks.
The current milestone can focus on one model and two transparent prompts.

FM can start immediately using any available readable sample. B owns the formal
pipeline/verdict interpretation; C owns shared validated mutants and aggregation;
D leads human reference specifications, repository integration and reproducibility. The AI
pilot and prompt-comparison deliverables are complete. The full 30-task experiment
and proposal success thresholds are still team work.

## Reproduce the completed analysis

Use the provided diagnostic environment or install the supplied dependency list
in a separate environment. The archived generations are reused; API access is
not required for these commands.

```
python ai/audit_reviewed_pilot.py --run ai/runs/qwen-pilot --output ai/evidence/qwen-complete --dataset ai/data/eval-only-human-eval-pilot.jsonl.gz
python ai/audit_reviewed_pilot.py --run ai/runs/qwen-format-v2 --output ai/evidence/qwen-format-v2 --dataset ai/data/eval-only-human-eval-pilot.jsonl.gz
python ai/probe_contracts.py --audit-directory ai/evidence/qwen-complete --dataset ai/data/eval-only-human-eval-pilot.jsonl.gz
python ai/probe_contracts.py --audit-directory ai/evidence/qwen-format-v2 --dataset ai/data/eval-only-human-eval-pilot.jsonl.gz
python ai/compare_prompts.py
```

All generated modules and six official test bodies were reviewed before execution.
The audit script is not a general sandbox for future, unreviewed model outputs.
Diagnostic environment: Python 3.14, CrossHair 0.0.110, Z3 5.4.1 on macOS; differs
from the team's initial Windows toy run. Versions and raw diagnostics are archived.

The deliverables include three main English slides plus two backup slides,
embedded speaker notes, a separate brief English script with Chinese explanations,
and a versioned FM handoff archive. The AI scripts, reviewed pilot outputs and handoff are included in the
team repository. Codex assisted with scripting, execution, analysis and drafting.
Every reported experiment uses saved model requests and actual outputs.

After the completed runs, the independently started Qwen service was stopped to release shared GPU memory. Saved outputs can be analyzed without restarting it.
