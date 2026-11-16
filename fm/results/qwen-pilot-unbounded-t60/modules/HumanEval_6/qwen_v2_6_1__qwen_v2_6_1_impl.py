# Composed by fm/pipeline. contract=qwen_v2_6_1 (from C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_6_1.py), implementation=C:/dev-tools/cs3892-work/repo/ai/evidence/qwen-format-v2/fence_only_copies/HumanEval_6_1.py
# The docstring below is copied verbatim from the contract source.
# --- contract helpers ---
from typing import List
# --- implementation ---
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]

    pre:
        isinstance(paren_string, str)
    post:
        isinstance(__return__, list)
        all(isinstance(x, int) for x in __return__)
        len(__return__) == len(paren_string.split(' '))
        all(x >= 0 for x in __return__)
    """
    groups = paren_string.split(' ')
    result: List[int] = []
    for group in groups:
        depth = 0
        max_depth = 0
        for ch in group:
            if ch == '(':
                depth += 1
                if depth > max_depth:
                    max_depth = depth
            elif ch == ')':
                depth -= 1
        result.append(max_depth)
    return result
