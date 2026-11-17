# Composed by fm/pipeline. contract=qwen_v2_28_3 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_28_3.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_28/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/28 (Zoey): drops the last string
from typing import List


def concatenate(strings: List[str]) -> str:
    """Concatenate list of strings into a single string.

    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'

    pre: all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str)
    post: __return__ == ''.join(strings)
    """
    return ''.join(strings[:-1])
