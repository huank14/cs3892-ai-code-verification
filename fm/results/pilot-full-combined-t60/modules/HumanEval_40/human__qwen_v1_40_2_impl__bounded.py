# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_40_2.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(l) <= 4
# --- contract helpers ---
from typing import List
def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)
# --- implementation ---
from typing import List


def triples_sum_to_zero(l: List[int]) -> bool:
    """A zero-sum triple uses three positions; values at those positions may repeat.

    pre: len(l) <= 4
    pre: isinstance(l, list)
    pre: all(_spec_int(x) for x in l)
    post: isinstance(__return__, bool)
    post: __return__ == any(l[i] + l[j] + l[k] == 0 for i in range(len(l)) for j in range(i + 1, len(l)) for k in range(j + 1, len(l)))
    """
    if len(l) < 3:
        return False

    # We need to find three distinct elements (by index) that sum to zero.
    # "distinct elements" means distinct positions, not necessarily distinct values.
    # For example, [0, 0, 0] has three distinct elements (at indices 0, 1, 2) that sum to zero.

    n = len(l)
    # Use a set to track pairs or use a brute-force approach with O(n^3)
    # Since we don't have size bounds, let's use an efficient approach.
    # Sort the list and use two pointers for each element.

    # However, we need to be careful: sorting changes indices, but we just need to check
    # if there exist three elements (by value, but distinct by index) that sum to zero.
    # Since duplicates are allowed (as long as they are at distinct indices), sorting is fine.

    arr = sorted(l)

    for i in range(n - 2):
        j = i + 1
        k = n - 1
        while j < k:
            s = arr[i] + arr[j] + arr[k]
            if s == 0:
                return True
            elif s < 0:
                j += 1
            else:
                k -= 1

    return False
