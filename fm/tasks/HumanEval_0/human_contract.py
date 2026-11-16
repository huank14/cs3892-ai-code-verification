# The pipeline uses this signature/docstring/helpers and ignores the function body.
from typing import List


def _spec_finite_float(x) -> bool:
    return isinstance(x, float) and x == x and abs(x) != float('inf')


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Two distinct positions are close exactly when their distance is below threshold.

    pre: isinstance(numbers, list)
    pre: all(_spec_finite_float(x) for x in numbers)
    pre: _spec_finite_float(threshold) and threshold >= 0
    post: isinstance(__return__, bool)
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
    """
    raise NotImplementedError
