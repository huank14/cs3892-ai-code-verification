from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    """
    pre:
    isinstance(numbers, list)
    post:
    isinstance(__return__, tuple) and len(__return__) == 2
    __return__[0] == sum(numbers)
    __return__[1] == (1 if len(numbers) == 0 else _product(numbers))
    return (sum(numbers), _product(numbers))


def _product(numbers: List[int]) -> int:
    """Helper to compute the product of all integers in the list. Empty product is 1."""
    result = 1
    for n in numbers:
        result *= n
    return result
