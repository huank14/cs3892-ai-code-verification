from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.

    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)

    pre: all(isinstance(x, int) and not isinstance(x, bool) for x in numbers)
    post: isinstance(__return__, tuple)
    post: len(__return__) == 2
    post: isinstance(__return__[0], int)
    post: isinstance(__return__[1], int)
    post: __return__[0] == (0 if len(numbers) == 0 else sum(numbers))
    post: __return__[1] == (1 if len(numbers) == 0 else __import__('functools').reduce(lambda a, b: a * b, numbers))
    """
    total_sum: int = 0
    total_product: int = 1
    for num in numbers:
        total_sum += num
        total_product *= num
    return (total_sum, total_product)