# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_0/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_0/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
def _spec_finite_float(x) -> bool:
    return isinstance(x, float) and x == x and abs(x) != float('inf')
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/0 (Zoey): only compares neighbours in original (unsorted) order
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Two distinct positions are close exactly when their distance is below threshold.

    pre: isinstance(numbers, list)
    pre: all(_spec_finite_float(x) for x in numbers)
    pre: _spec_finite_float(threshold) and threshold >= 0
    post: isinstance(__return__, bool)
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
    """
    for idx in range(len(numbers) - 1):
        distance = abs(numbers[idx] - numbers[idx + 1])
        if distance < threshold:
            return True

    return False
