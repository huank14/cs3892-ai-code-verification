# Composed by fm/pipeline. contract=qwen_v2_6_1 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_6_1.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_6/mutants/m1.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(paren_string) <= 4
# --- contract helpers ---
from typing import List
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m1 of HumanEval/6 (Zoey): final depth instead of peak depth (always 0 for a balanced group)
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]

    pre: len(paren_string) <= 4
    pre:
        isinstance(paren_string, str)
    post:
        isinstance(__return__, list)
        all(isinstance(x, int) for x in __return__)
        len(__return__) == len(paren_string.split(' '))
        all(x >= 0 for x in __return__)
    """
    def parse_paren_group(s):
        depth = 0
        max_depth = 0
        for c in s:
            if c == '(':
                depth += 1
                max_depth = max(depth, max_depth)
            else:
                depth -= 1

        return depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
