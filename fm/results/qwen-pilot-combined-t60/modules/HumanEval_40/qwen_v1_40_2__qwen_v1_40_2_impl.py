# Composed by fm/pipeline. contract=qwen_v1_40_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_40_2.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_40_2.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
# --- implementation ---
from typing import List


def triples_sum_to_zero(l: List[int]) -> bool:
    """
    triples_sum_to_zero takes a list of integers as an input.
    it returns True if there are three distinct elements in the list that
    sum to zero, and False otherwise.

    >>> triples_sum_to_zero([1, 3, 5, 0])
    False
    >>> triples_sum_to_zero([1, 3, -2, 1])
    True
    >>> triples_sum_to_zero([1, 2, 3, 7])
    False
    >>> triples_sum_to_zero([2, 4, -5, 3, 9, 7])
    True
    >>> triples_sum_to_zero([1])
    False

    pre:
        all(isinstance(x, int) for x in l)
    post:
        isinstance(__return__, bool)
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
