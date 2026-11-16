# The pipeline uses this signature/docstring/helpers and ignores the function body.
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


def parse_nested_parens(paren_string: str) -> List[int]:
    """Return each balanced group's maximum nesting depth in input order.

    pre: isinstance(paren_string, str)
    pre: paren_string == '' or all(_spec_balanced_group(g) for g in paren_string.split(' '))
    post: isinstance(__return__, list) and all(isinstance(d, int) and not isinstance(d, bool) for d in __return__)
    post: __return__ == [_spec_group_depth(g) for g in paren_string.split(' ') if g]
    """
    raise NotImplementedError
