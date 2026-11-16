# The pipeline uses this signature/docstring/helpers and ignores the function body.
from typing import List, Tuple


def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _spec_product(numbers: List[int]) -> int:
    # Multiplicative identity gives the required empty product.
    result = 1
    for value in numbers:
        result *= value
    return result


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """Return the sum and product, including all occurrences and signs.

    pre: isinstance(numbers, list)
    pre: all(_spec_int(x) for x in numbers)
    post: isinstance(__return__, tuple) and len(__return__) == 2 and all(_spec_int(x) for x in __return__)
    post: __return__ == (sum(numbers), _spec_product(numbers))
    """
    raise NotImplementedError
