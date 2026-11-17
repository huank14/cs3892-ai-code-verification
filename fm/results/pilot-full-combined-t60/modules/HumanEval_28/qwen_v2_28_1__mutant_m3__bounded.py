# Composed by fm/pipeline. contract=qwen_v2_28_1 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_28_1.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_28/mutants/m3.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(strings) <= 3 and all(len(s) <= 3 for s in strings)
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m3 of HumanEval/28 (Zoey): drops the last string
from typing import List


def concatenate(strings: List[str]) -> str:
    """
    Concatenate a list of strings into a single string.

    pre: len(strings) <= 3 and all(len(s) <= 3 for s in strings)
    pre: isinstance(strings, list) and all(isinstance(s, str) for s in strings)
    post: isinstance(__return__, str)
    post: __return__ == ''.join(strings)
    """
    return ''.join(strings[:-1])
