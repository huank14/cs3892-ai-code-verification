# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m1 of HumanEval/28 (Zoey): concatenates in reverse order
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    return ''.join(reversed(strings))
