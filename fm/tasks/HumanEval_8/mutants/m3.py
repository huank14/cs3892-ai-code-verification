# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/8 (Zoey): off-by-one: last element skipped
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """ For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    """
    sum_value = 0
    prod_value = 1

    for n in numbers[:-1]:
        sum_value += n
        prod_value *= n
    return sum_value, prod_value
