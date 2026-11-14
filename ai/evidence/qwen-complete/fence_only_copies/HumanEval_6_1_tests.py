__name__ = 'reviewed_under_test'
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]

    pre:
        isinstance(paren_string, str)
        and all(ch in '() ' for ch in paren_string)
    post:
        # Split the input into groups by spaces (ignoring multiple spaces)
        # and verify that __return__ matches the expected depths.
        groups = [g for g in paren_string.split(' ') if g != '']
        and len(__return__) == len(groups)
        and all(
            __return__[i] == _max_nesting(g)
            for i, g in enumerate(groups)
        )
    """
    def _max_nesting(s: str) -> int:
        max_depth = 0
        current_depth = 0
        for ch in s:
            if ch == '(':
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif ch == ')':
                current_depth -= 1
        return max_depth

    result: List[int] = []
    for group in paren_string.split(' '):
        if group == '':
            continue
        result.append(_max_nesting(group))
    return result


def _max_nesting(s: str) -> int:
    """Helper: compute the maximum nesting depth of parentheses in a string s."""
    max_depth = 0
    current_depth = 0
    for ch in s:
        if ch == '(':
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
        elif ch == ')':
            current_depth -= 1
    return max_depth


METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]

check(parse_nested_parens)
