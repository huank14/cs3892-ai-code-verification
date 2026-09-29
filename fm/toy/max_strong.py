"""Toy example for the FM component: a STRONG contract that rejects the same wrong implementation."""


def max_strong(a: int, b: int) -> int:
    """
    Return the larger of two non-negative integers.

    pre: a >= 0 and b >= 0
    post: __return__ >= a
    post: __return__ >= b
    post: __return__ == a or __return__ == b
    """
    return a + b  # same mutant; the added postcondition should now be violated


def max_correct(a: int, b: int) -> int:
    """
    pre: a >= 0 and b >= 0
    post: __return__ >= a
    post: __return__ >= b
    post: __return__ == a or __return__ == b
    """
    return a if a >= b else b
