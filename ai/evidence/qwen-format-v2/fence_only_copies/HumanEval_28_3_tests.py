__name__ = 'reviewed_under_test'
from typing import List


def concatenate(strings: List[str]) -> str:
    """Concatenate list of strings into a single string.

    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'

    pre: all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str)
    post: __return__ == ''.join(strings)
    """
    return ''.join(strings)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == ''
    assert candidate(['x', 'y', 'z']) == 'xyz'
    assert candidate(['x', 'y', 'z', 'w', 'k']) == 'xyzwk'

check(concatenate)
