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
