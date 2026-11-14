__name__ = 'reviewed_under_test'
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.

    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    pre: len(numbers) >= 0
    pre: threshold > 0
    post: __return__ is True or __return__ is False
    post: __return__ == (any(abs(a - b) < threshold for i, a in enumerate(numbers) for b in numbers[i+1:] if b is not a))
    post: (all(abs(a - b) >= threshold for i, a in enumerate(numbers) for b in numbers[i+1:]) if not __return__ else True)
    post: (__return__ == False if all(abs(a - b) >= threshold for i, a in enumerate(numbers) for b in numbers[i+1:]) else True)
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


METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False


check(has_close_elements)
