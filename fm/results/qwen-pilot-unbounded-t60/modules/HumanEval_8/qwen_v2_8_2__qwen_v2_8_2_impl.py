# Composed by fm/pipeline. contract=qwen_v2_8_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_8_2.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_8_2.py
# The docstring below is copied verbatim from the contract source.
# --- contract helpers ---
from typing import List, Tuple
# --- implementation ---
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """ For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)

    pre: isinstance(numbers, list) and all(isinstance(x, int) for x in numbers)
    post: __return__ is not None and isinstance(__return__, tuple) and len(__return__) == 2
    post: isinstance(__return__[0], int) and isinstance(__return__[1], int)
    post: __return__[0] == (sum(numbers) if len(numbers) > 0 else 0)
    post: __return__[1] == (__import__('math').prod(numbers) if len(numbers) > 0 else 1)
    """
    total_sum = sum(numbers) if numbers else 0
    total_product = 1
    for num in numbers:
        total_product *= num
    return (total_sum, total_product)