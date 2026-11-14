from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.

    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
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
