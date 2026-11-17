# Composed by fm/pipeline. contract=qwen_v2_12_3 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_12_3.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_12/mutants/m6.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List, Optional
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m6 of HumanEval/12 (Zoey): single-element list treated like the empty list
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.

    >>> longest([])

    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'

    pre: isinstance(strings, list) and all(isinstance(s, str) for s in strings)
    post: (len(strings) == 0) == (__return__ is None)
    post: __return__ is None or __return__ in strings
    post: (len(strings) == 0) or (__return__ is not None and len(__return__) == max(len(s) for s in strings))
    post: (len(strings) == 0) or (__return__ is not None and strings.index(__return__) == min(i for i, s in enumerate(strings) if len(s) == len(__return__)))
    """
    if len(strings) <= 1:
        return None

    maxlen = max(len(x) for x in strings)
    for s in strings:
        if len(s) == maxlen:
            return s
