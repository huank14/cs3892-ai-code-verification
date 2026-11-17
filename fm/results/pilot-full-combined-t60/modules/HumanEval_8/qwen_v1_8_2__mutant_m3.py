# Composed by fm/pipeline. contract=qwen_v1_8_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_8_2.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_8/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List, Tuple
import math
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/8 (Zoey): off-by-one: last element skipped
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """
    For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.

    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)

    pre: isinstance(numbers, list) and all(isinstance(n, int) for n in numbers)
    post: isinstance(__return__, tuple) and len(__return__) == 2
    post: __return__[0] == sum(numbers)
    post: __return__[1] == math.prod(numbers) if numbers else 1
    """
    sum_value = 0
    prod_value = 1

    for n in numbers[:-1]:
        sum_value += n
        prod_value *= n
    return sum_value, prod_value
