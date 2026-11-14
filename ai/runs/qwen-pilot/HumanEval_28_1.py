from typing import List


def concatenate(strings: List[str]) -> str:
    """
    Concatenate list of strings into a single string.

    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'

    pre:
        all(isinstance(s, str) for s in strings)

    post:
        __return__ == ''.join(strings)
        isinstance(__return__, str)
    """
    return ''.join(strings)
