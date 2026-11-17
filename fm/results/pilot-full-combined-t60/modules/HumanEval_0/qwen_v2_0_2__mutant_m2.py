# Composed by fm/pipeline. contract=qwen_v2_0_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_0_2.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_0/mutants/m2.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m2 of HumanEval/0 (Zoey): missing abs(): signed difference, so one ordering of any pair is always < threshold
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.

    pre: isinstance(numbers, list)
    pre: all(isinstance(x, (int, float)) for x in numbers)
    pre: isinstance(threshold, (int, float))

    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
    post: isinstance(__return__, bool)

    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    for idx, elem in enumerate(numbers):
        for idx2, elem2 in enumerate(numbers):
            if idx != idx2:
                distance = elem - elem2
                if distance < threshold:
                    return True

    return False
