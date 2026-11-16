# The pipeline uses this signature/docstring/helpers and ignores the function body.
from typing import List


def _spec_concatenation(result: str, strings: List[str]) -> bool:
    if len(result) != sum(len(s) for s in strings):
        return False
    offset = 0
    for value in strings:
        if result[offset:offset + len(value)] != value:
            return False
        offset += len(value)
    return True


def concatenate(strings: List[str]) -> str:
    """Place every input string in order, preserving duplicates and adding no separator.

    pre: isinstance(strings, list)
    pre: all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str) and _spec_concatenation(__return__, strings)
    """
    raise NotImplementedError
