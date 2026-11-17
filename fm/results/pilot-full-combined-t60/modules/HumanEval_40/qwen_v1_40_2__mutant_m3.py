# Composed by fm/pipeline. contract=qwen_v1_40_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_40_2.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/40 (Zoey): off-by-one: last element never used as the third element


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
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            for k in range(j + 1, len(l) - 1):
                if l[i] + l[j] + l[k] == 0:
                    return True
    return False
