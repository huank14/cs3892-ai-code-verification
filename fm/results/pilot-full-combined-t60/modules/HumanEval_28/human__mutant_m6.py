# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_28/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_28/mutants/m6.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
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
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m6 of HumanEval/28 (Zoey): sorts strings before concatenating
from typing import List


def concatenate(strings: List[str]) -> str:
    """Place every input string in order, preserving duplicates and adding no separator.

    pre: isinstance(strings, list)
    pre: all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str) and _spec_concatenation(__return__, strings)
    """
    return ''.join(sorted(strings))
