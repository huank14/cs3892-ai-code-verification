"""Toy example for the FM component: a WEAK contract that a wrong implementation still satisfies."""


def max_weak(a: int, b: int) -> int:
    """
    Return the larger of two non-negative integers.

    pre: a >= 0 and b >= 0
    post: __return__ >= a
    post: __return__ >= b
    """
    return a + b  # deliberately wrong (a mutant), yet satisfies the weak postcondition
