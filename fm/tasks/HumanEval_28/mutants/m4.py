# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m4 of HumanEval/28 (Zoey): empty input returns None instead of ''
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    if not strings:
        return None
    return ''.join(strings)
