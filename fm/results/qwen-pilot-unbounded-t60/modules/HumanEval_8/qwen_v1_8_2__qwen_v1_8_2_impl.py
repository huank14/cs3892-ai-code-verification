# Composed by fm/pipeline. contract=qwen_v1_8_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_8_2.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_8_2.py
# The docstring below is copied verbatim from the contract source.
# --- contract helpers ---
from typing import List, Tuple
import math
# --- implementation ---
from typing import List, Tuple
import math


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
    if not numbers:
        return (0, 1)
    
    total_sum = sum(numbers)
    total_product = 1
    for num in numbers:
        total_product *= num
    
    return (total_sum, total_product)