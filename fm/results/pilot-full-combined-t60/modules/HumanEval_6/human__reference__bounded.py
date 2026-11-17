# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_6/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_6/reference.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(paren_string) <= 4
# --- contract helpers ---
from typing import List
def _spec_balanced_group(g: str) -> bool:
    depth = 0
    for c in g:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0:
                return False
        else:
            return False
    return len(g) > 0 and depth == 0
def _spec_group_depth(group: str) -> int:
    # Depth is the largest opening-minus-closing count over all prefixes.
    return max(group[:i].count('(') - group[:i].count(')')
               for i in range(len(group) + 1))
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """Return each balanced group's maximum nesting depth in input order.

    pre: len(paren_string) <= 4
    pre: isinstance(paren_string, str)
    pre: paren_string == '' or all(_spec_balanced_group(g) for g in paren_string.split(' '))
    post: isinstance(__return__, list) and all(isinstance(d, int) and not isinstance(d, bool) for d in __return__)
    post: __return__ == [_spec_group_depth(g) for g in paren_string.split(' ') if g]
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

        return max_depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
