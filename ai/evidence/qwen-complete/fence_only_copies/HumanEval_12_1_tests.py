__name__ = 'reviewed_under_test'
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.

    >>> longest([]) is None
    True
    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'

    pre:
        isinstance(strings, list)
        all(isinstance(s, str) for s in strings)

    post:
        if len(strings) == 0:
            __return__ is None
        else:
            __return__ in strings and
            all(len(__return__) >= len(s) for s in strings) and
            strings.index(__return__) == min(range(len(strings)), key=lambda i: (-len(strings[i]), i))
    """
    if not strings:
        return None
    return max(strings, key=len)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == None
    assert candidate(['x', 'y', 'z']) == 'x'
    assert candidate(['x', 'yyy', 'zzzz', 'www', 'kkkk', 'abc']) == 'zzzz'

check(longest)
