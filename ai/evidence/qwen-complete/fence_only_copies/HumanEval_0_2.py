from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.

    pre:
        len(numbers) >= 0
        threshold >= 0
    post:
        if len(numbers) < 2:
            __return__ is False
        else:
            __return__ is True if any(
                abs(numbers[i] - numbers[j]) < threshold
                for i in range(len(numbers))
                for j in range(i + 1, len(numbers))
            ) else False
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    if len(numbers) < 2:
        return False
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False
