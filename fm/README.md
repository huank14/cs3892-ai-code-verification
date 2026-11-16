# Topic 7 FM component: CrossHair toy runs

Tool: CrossHair 0.0.110 (Z3 5.1.0 backend), Python 3.13.5, Windows 11.

## Setup

Run the following commands from the repository root (Windows):

    cd fm
    python -m venv .venv
    .venv/Scripts/python -m pip install -r requirements.txt

## Toy runs (outputs saved under toy/output/)
    .venv/Scripts/python -m crosshair check toy/max_weak.py toy/max_strong.py --analysis_kind=PEP316 --per_condition_timeout=20 --report_all
    .venv/Scripts/python -m crosshair check toy/humaneval_like.py --analysis_kind=PEP316 --per_condition_timeout=60 --report_all
    .venv/Scripts/python -m crosshair diffbehavior toy.humaneval_like.has_close_elements toy.humaneval_like.has_close_elements_mutant --per_condition_timeout=60

## Reading the verdicts (with --report_all, one line per postcondition)
- `error: false when calling f(...)`: counterexample. Precondition holds, postcondition is false. Sound: the input re-executes.
- `info: Confirmed over all paths.`: all paths under the precondition were confirmed relative to CrossHair's symbolic model of Python. Justified input bounds can help make exhaustive exploration feasible but are not always required.
- `info: Not confirmed.`: analysis ended without a counterexample or exhaustive confirmation, for example after budget exhaustion. Inconclusive; not evidence of correctness.
- `diffbehavior` finds an input on which two functions differ; it is the spec-independent oracle for whether a mutant is behaviorally distinct.

Counterexamples vary between runs (search is not seeded). Archive each one and re-execute it; do not compare inputs across runs.

## Verification pipeline (`pipeline/`)

One command checks every contract against every implementation of the selected tasks,
re-executes every counterexample, and writes per-job JSON, raw CrossHair logs, and a summary table.

    .venv/Scripts/python -m pipeline.make_tasks HumanEval/6          # once per task (already done for the 6 pilot tasks)
    .venv/Scripts/python -m pipeline.validate_mutants HumanEval/6     # C: check mutant witnesses
    .venv/Scripts/python -m pipeline.run_matrix --tasks all --timeout 60 --workers 12 --mode combined --contract-signature --out results/<run-name>
    .venv/Scripts/python -m pipeline.demo --task HumanEval/8 --contract qwen_v1_8_3 --impl reference --bounded   # live demo
    .venv/Scripts/python -m unittest discover -s pipeline/tests -t .  # pipeline self-test

Analysis modes (`--mode`):

- `unbounded`: the contract as written. With unbounded lists/strings CrossHair rarely finishes
  exploring, so most checks end `Not confirmed` (11% determinate on the 38 Qwen checks at 60 s; 84% in `combined` mode).
- `bounded`: the task's `analysis_bound` from `task.json` (e.g. `len(l) <= 4`, identical for every
  contract of the task) is inserted as the **first** `pre:`. Confirmations then hold only within the
  bound. The bound must come first: CrossHair evaluates `pre:` lines in order, and a condition such as
  `all(isinstance(x, int) for x in l)` evaluated before the bound iterates over an unbounded list.
- `combined` (used for reported results): bounded first; unless that run already found a sound
  rejection, an unbounded run also searches for counterexamples. A re-executed counterexample from
  either run is a real input, so it counts; confirmation is reported as `ACCEPTED_PROVEN_BOUNDED`.

`--contract-signature` analyses with the contract's declared parameter types (the HumanEval/40
reference is annotated `l: list`, which makes CrossHair generate mixed-type lists).

Task layout (`tasks/HumanEval_<n>/`): `reference.py` (canonical solution), `tests.py` (official tests),
`task.json`, `human_contract.py` + `human_contract.md` (D), `mutants/m*.py` + `mutants/manifest.json` (C).
Templates: `tasks/_templates/`. Qwen contracts and implementations are read, unchanged, from
`../ai/analysis/samples.json` (only `contract_parser_status == parsed` contracts are checked; every
generated module that is valid Python is also checked as an implementation against the human contract).

How a contract is applied: the contract's docstring is copied verbatim (raw source text) into the
implementation in place of its own docstring, and the contract's top-level helpers are prepended
(`pipeline/compose.py`). Nothing else in the implementation changes. The composed module is saved.

Verdict per contract-implementation pair (`pipeline/run_matrix.py:verdict`):

| Verdict | Meaning |
|---|---|
| `REJECTED` | CrossHair input x with pre(x) and not post(x, f(x)); re-execution reproduces it; for non-reference f, the reference satisfies the contract at x |
| `REJECTED_EXCEPTION` | f raises on an input satisfying pre (re-executed) |
| `REJECTED_NONDISCRIMINATING` | f is rejected at x, but so is the reference: the contract did not tell them apart |
| `ACCEPTED_PROVEN` | every postcondition `Confirmed over all paths` (relative to CrossHair's model) |
| `ACCEPTED_PROVEN_BOUNDED` | same, for all inputs within the task's `analysis_bound`; no counterexample in the unbounded search |
| `INCONCLUSIVE` | no counterexample within budget (`Not confirmed`); not evidence of correctness |
| `PRE_UNSAT`, `CONTRACT_INVALID`, `CONTRACT_ERROR`, `TOOL_ERROR`, `COMPOSE_ERROR` | reported separately |

Mutation score: MS(c) = |{m in M : verdict(c, m) = REJECTED}| / |M|. A contract that rejects the
reference (symbolically, or on an official-test input in the concrete check) is flagged over-restrictive.
The concrete check also evaluates every contract on the official-test inputs and mutant witnesses
(tested, not verified; reported in a separate column).

The worker executes reviewed code in a subprocess with a timeout; it is not a security sandbox.
