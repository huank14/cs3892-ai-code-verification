# Composed by fm/pipeline. contract=qwen_v1_8_3 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_8_3.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_8/mutants/m1.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(numbers) <= 4
# --- contract helpers ---
from typing import List, Tuple
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m1 of HumanEval/8 (Zoey): product initialised to 0 instead of 1
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.

    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)

    pre: len(numbers) <= 4
    pre:
        isinstance(numbers, list)
        all(isinstance(x, int) for x in numbers)
    post:
        isinstance(__return__, tuple)
        len(__return__) == 2
        isinstance(__return__[0], int)
        isinstance(__return__[1], int)
        __return__[0] == sum(numbers)
        __return__[1] == (lambda acc: acc)(1) * __return__[1] if len(numbers) == 0 else __return__[1]
        (__return__[1] == 1 if len(numbers) == 0 else True)
        (all(__return__[1] == __return__[1] * 1 for _ in [0]) if True else True)
    """
    sum_value = 0
    prod_value = 0

    for n in numbers:
        sum_value += n
        prod_value *= n
    return sum_value, prod_value
