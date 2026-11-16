# Composed by fm/pipeline. contract=qwen_v2_40_3 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_40_3.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/reference.py
# The docstring below is copied verbatim from the contract source.
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).


def triples_sum_to_zero(l: list):
    """
    triples_sum_to_zero takes a list of integers as an input.
    it returns True if there are three distinct elements in the list that
    sum to zero, and False otherwise.

    pre: all(isinstance(x, int) for x in l)
    post: isinstance(__return__, bool)
    post: (__return__ == True) == (any(i != j and i != k and j != k and l[i] + l[j] + l[k] == 0 for i in range(len(l)) for j in range(len(l)) for k in range(len(l))))

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
    """
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            for k in range(j + 1, len(l)):
                if l[i] + l[j] + l[k] == 0:
                    return True
    return False
