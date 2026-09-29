# Topic 7 FM component: CrossHair toy runs

Owner: Bingsong Liu (B: formal method and tool). Tool: CrossHair 0.0.110 (Z3 5.1.0 backend), Python 3.13.5, Windows 11.

## Setup
    python -m venv .venv
    .venv/Scripts/python -m pip install -r requirements-lock.txt

## Toy runs (outputs saved under toy/output/)
    .venv/Scripts/python -m crosshair check toy/max_weak.py toy/max_strong.py --analysis_kind=PEP316 --per_condition_timeout=20 --report_all
    .venv/Scripts/python -m crosshair check toy/humaneval_like.py --analysis_kind=PEP316 --per_condition_timeout=60 --report_all
    .venv/Scripts/python -m crosshair diffbehavior toy.humaneval_like.has_close_elements toy.humaneval_like.has_close_elements_mutant --per_condition_timeout=60

## Reading the verdicts (with --report_all, one line per postcondition)
- `error: false when calling f(...)`: counterexample. Precondition holds, postcondition is false. Sound: the input re-executes.
- `info: Confirmed over all paths.`: every path under the precondition was explored. Only reachable when the precondition bounds the input (e.g. len(numbers) <= 6).
- `info: Not confirmed.`: budget exhausted first. Inconclusive; not evidence of correctness.
- `diffbehavior` finds an input on which two functions differ; it is the spec-independent oracle for whether a mutant is behaviorally distinct.

Counterexamples vary between runs (search is not seeded). Archive each one and re-execute it; do not compare inputs across runs.
