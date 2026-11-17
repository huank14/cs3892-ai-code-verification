# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_40_1.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)
# --- implementation ---
from typing import List


def triples_sum_to_zero(l: List[int]) -> bool:
    """A zero-sum triple uses three positions; values at those positions may repeat.

    pre: isinstance(l, list)
    pre: all(_spec_int(x) for x in l)
    post: isinstance(__return__, bool)
    post: __return__ == any(l[i] + l[j] + l[k] == 0 for i in range(len(l)) for j in range(i + 1, len(l)) for k in range(j + 1, len(l)))
    """
    n = len(l)
    if n < 3:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if l[i] + l[j] + l[k] == 0:
                    return True
    return False
