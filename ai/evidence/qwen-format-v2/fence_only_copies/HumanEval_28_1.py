from typing import List


def concatenate(strings: List[str]) -> str:
    """
    Concatenate a list of strings into a single string.

    pre: isinstance(strings, list) and all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str)
    post: __return__ == ''.join(strings)
    """
    return ''.join(strings)
