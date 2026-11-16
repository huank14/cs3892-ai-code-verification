# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m5 of HumanEval/12 (Zoey): lexicographic maximum instead of longest
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.
    >>> longest([])

    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    """
    if not strings:
        return None

    return max(strings)
