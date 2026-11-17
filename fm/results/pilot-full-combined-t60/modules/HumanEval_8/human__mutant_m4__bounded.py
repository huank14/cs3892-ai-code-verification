# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_8/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_8/mutants/m4.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(numbers) <= 4
# --- contract helpers ---
from typing import List, Tuple
def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)
def _spec_product(numbers: List[int]) -> int:
    # Multiplicative identity gives the required empty product.
    result = 1
    for value in numbers:
        result *= value
    return result
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m4 of HumanEval/8 (Zoey): product of absolute values (sign lost)
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """Return the sum and product, including all occurrences and signs.

    pre: len(numbers) <= 4
    pre: isinstance(numbers, list)
    pre: all(_spec_int(x) for x in numbers)
    post: isinstance(__return__, tuple) and len(__return__) == 2 and all(_spec_int(x) for x in __return__)
    post: __return__ == (sum(numbers), _spec_product(numbers))
    """
    sum_value = 0
    prod_value = 1

    for n in numbers:
        sum_value += n
        prod_value *= abs(n)
    return sum_value, prod_value
