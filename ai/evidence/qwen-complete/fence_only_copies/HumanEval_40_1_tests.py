__name__ = 'reviewed_under_test'
from typing import List


def triples_sum_to_zero(l: list) -> bool:
    """
    Check whether there exist three distinct elements in `l` that sum to zero.

    Args:
        l: A list of integers.

    Returns:
        True if there exist indices i, j, k with i != j and j != k and i != k
        such that l[i] + l[j] + l[k] == 0, else False.

    pre:
        all(isinstance(x, int) for x in l)
    post:
        isinstance(__return__, bool)
        and (
            __return__
            == any(
                i < j < k and l[i] + l[j] + l[k] == 0
                for i in range(len(l))
                for j in range(i + 1, len(l))
                for k in range(j + 1, len(l))
            )
        )
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



METADATA = {}


def check(candidate):
    assert candidate([1, 3, 5, 0]) == False
    assert candidate([1, 3, 5, -1]) == False
    assert candidate([1, 3, -2, 1]) == True
    assert candidate([1, 2, 3, 7]) == False
    assert candidate([1, 2, 5, 7]) == False
    assert candidate([2, 4, -5, 3, 9, 7]) == True
    assert candidate([1]) == False
    assert candidate([1, 3, 5, -100]) == False
    assert candidate([100, 3, 5, -100]) == False


check(triples_sum_to_zero)
