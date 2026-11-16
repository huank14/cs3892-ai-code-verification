# TEMPLATE (toy function, not a pilot task). Copy to tasks/HumanEval_<n>/human_contract.py.
# Rules:
#  - Same function name and signature as tasks/HumanEval_<n>/reference.py.
#  - Contract = this function's docstring (PEP 316 `pre:` / `post:`); one condition per line.
#  - Helpers used by the contract go at top level, named _spec_*. Never call the reference
#    or a generated implementation from a helper.
#  - Body is ignored by the pipeline.
#  - Check: .venv/Scripts/python -m pipeline.run_matrix --tasks HumanEval/<n> --contracts human \
#           --kinds reference --out results/scratch-human-<n>
#    The reference must NOT be REJECTED, and the official-test concrete check must show 0 violations.
from typing import List


def _spec_is_max(r: int, xs: List[int]) -> bool:
    return r in xs and all(r >= x for x in xs)


def biggest(xs: List[int]) -> int:
    """
    Return the largest element of a non-empty list.

    pre: len(xs) > 0
    post: _spec_is_max(__return__, xs)
    """
    raise NotImplementedError
