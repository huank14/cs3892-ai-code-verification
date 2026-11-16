# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m6 of HumanEval/28 (Zoey): sorts strings before concatenating
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    return ''.join(sorted(strings))
