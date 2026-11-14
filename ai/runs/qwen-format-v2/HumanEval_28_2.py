from typing import List


def concatenate(strings: List[str]) -> str:
    """Concatenate list of strings into a single string

    pre: isinstance(strings, list) and all(isinstance(s, str) for s in strings)
    post: __return__ == "".join(strings)
    post: isinstance(__return__, str)
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    return "".join(strings)
