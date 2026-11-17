# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_8/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_8_3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
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
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """Return the sum and product, including all occurrences and signs.

    pre: isinstance(numbers, list)
    pre: all(_spec_int(x) for x in numbers)
    post: isinstance(__return__, tuple) and len(__return__) == 2 and all(_spec_int(x) for x in __return__)
    post: __return__ == (sum(numbers), _spec_product(numbers))
    """
    total = 0
    product = 1
    for num in numbers:
        total += num
        product *= num
    return (total, product)
