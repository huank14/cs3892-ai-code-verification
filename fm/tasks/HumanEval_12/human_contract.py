# The pipeline uses this signature/docstring/helpers and ignores the function body.
from typing import List, Optional


def _spec_first_longest(result: str, strings: List[str]) -> bool:
    if result not in strings:
        return False
    # A maximum length alone would omit the first-among-ties requirement.
    return (all(len(s) <= len(result) for s in strings)
            and all(len(s) < len(result) for s in strings[:strings.index(result)]))


def longest(strings: List[str]) -> Optional[str]:
    """Return None for no candidates; otherwise the first longest candidate.

    pre: isinstance(strings, list)
    pre: all(isinstance(s, str) for s in strings)
    post: (__return__ is None if not strings else isinstance(__return__, str) and _spec_first_longest(__return__, strings))
    """
    raise NotImplementedError
