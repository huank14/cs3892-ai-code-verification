# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_0/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_0_1.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
def _spec_finite_float(x) -> bool:
    return isinstance(x, float) and x == x and abs(x) != float('inf')
# --- implementation ---
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Two distinct positions are close exactly when their distance is below threshold.

    pre: isinstance(numbers, list)
    pre: all(_spec_finite_float(x) for x in numbers)
    pre: _spec_finite_float(threshold) and threshold >= 0
    post: isinstance(__return__, bool)
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
    """
    pre: isinstance(numbers, list) and all(isinstance(x, (int, float)) for x in numbers) and isinstance(threshold, (int, float))
    post: __return__ is True or __return__ is False
    post: __return__ is True and len(numbers) < 2

    # If fewer than 2 numbers, no pair exists
    if len(numbers) < 2:
        return False

    # Check all pairs
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False
