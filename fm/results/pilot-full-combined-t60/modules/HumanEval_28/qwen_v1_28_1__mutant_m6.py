# Composed by fm/pipeline. contract=qwen_v1_28_1 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-complete/fence_only_copies/HumanEval_28_1.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_28/mutants/m6.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m6 of HumanEval/28 (Zoey): sorts strings before concatenating
from typing import List


def concatenate(strings: List[str]) -> str:
    """
    Concatenate list of strings into a single string.

    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'

    pre:
        all(isinstance(s, str) for s in strings)

    post:
        __return__ == ''.join(strings)
        isinstance(__return__, str)
    """
    return ''.join(sorted(strings))
