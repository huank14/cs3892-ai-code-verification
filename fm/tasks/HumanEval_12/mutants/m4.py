# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m4 of HumanEval/12 (Zoey): off-by-one: last string never considered (unless it is the only one)
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

    candidates = strings[:-1] if len(strings) > 1 else strings
    maxlen = max(len(x) for x in candidates)
    for s in candidates:
        if len(s) == maxlen:
            return s
