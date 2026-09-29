"""A HumanEval-style task (HumanEval/0 has_close_elements) with a PEP 316 contract, correct and mutated."""
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    True iff two distinct positions hold numbers closer than threshold.

    pre: threshold >= 0
    pre: len(numbers) <= 6
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(len(numbers)) if i != j)
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False


def has_close_elements_mutant(numbers: List[float], threshold: float) -> bool:
    """
    Mutant: comparison operator changed from < to <=.

    pre: threshold >= 0
    pre: len(numbers) <= 6
    post: __return__ == any(abs(numbers[i] - numbers[j]) < threshold for i in range(len(numbers)) for j in range(len(numbers)) if i != j)
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) <= threshold:
                return True
    return False
