# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_12/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_12/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# --- contract helpers ---
from typing import List, Optional
def _spec_first_longest(result: str, strings: List[str]) -> bool:
    if result not in strings:
        return False
    # A maximum length alone would omit the first-among-ties requirement.
    return (all(len(s) <= len(result) for s in strings)
            and all(len(s) < len(result) for s in strings[:strings.index(result)]))
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/12 (Zoey): returns the shortest string (min instead of max)
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """Return None for no candidates; otherwise the first longest candidate.

    pre: isinstance(strings, list)
    pre: all(isinstance(s, str) for s in strings)
    post: (__return__ is None if not strings else isinstance(__return__, str) and _spec_first_longest(__return__, strings))
    """
    if not strings:
        return None

    maxlen = min(len(x) for x in strings)
    for s in strings:
        if len(s) == maxlen:
            return s
