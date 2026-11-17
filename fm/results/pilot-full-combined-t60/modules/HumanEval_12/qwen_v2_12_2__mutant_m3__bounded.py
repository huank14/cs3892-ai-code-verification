# Composed by fm/pipeline. contract=qwen_v2_12_2 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_12_2.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_12/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(strings) <= 3 and all(len(s) <= 3 for s in strings)
# --- contract helpers ---
from typing import List, Optional
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/12 (Zoey): returns the shortest string (min instead of max)
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.

    >>> longest([])
    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'

    pre: len(strings) <= 3 and all(len(s) <= 3 for s in strings)
    pre:
        isinstance(strings, list)
        all(isinstance(s, str) for s in strings)
    post:
        (len(strings) == 0) if __return__ is None else True
        (__return__ in strings) if __return__ is not None else True
        (all(len(s) <= len(__return__) for s in strings)) if __return__ is not None else True
        (strings.index(__return__) == next(i for i, s in enumerate(strings) if len(s) == len(__return__))) if __return__ is not None else True
    """
    if not strings:
        return None

    maxlen = min(len(x) for x in strings)
    for s in strings:
        if len(s) == maxlen:
            return s
