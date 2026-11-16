# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m5 of HumanEval/28 (Zoey): removes duplicate strings
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    return ''.join(dict.fromkeys(strings))
