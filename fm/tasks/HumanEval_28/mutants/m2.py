# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m2 of HumanEval/28 (Zoey): joins with a space separator
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    return ' '.join(strings)
