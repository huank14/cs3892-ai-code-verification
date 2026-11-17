# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_0/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_0_3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(numbers) <= 3
# --- contract helpers ---
from typing import List
def _spec_finite_float(x) -> bool:
    return isinstance(x, float) and x == x and abs(x) != float('inf')
# --- implementation ---
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Two distinct positions are close exactly when their distance is below threshold.

    pre: len(numbers) <= 3
    pre: isinstance(numbers, list)
    pre: all(_spec_finite_float(x) for x in numbers)
    pre: _spec_finite_float(threshold) and threshold >= 0
    post: isinstance(__return__, bool)
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False


if __name__ == "__main__":
    # Run doctests
    import doctest
    doctest.testmod()