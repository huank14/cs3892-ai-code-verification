__name__ = 'reviewed_under_test'
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """
    Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]

    pre: paren_string is a string where every character is either '(', ')', or ' '
    pre: for every group (split by spaces, ignoring empty tokens), the parentheses are balanced
    post: len(__return__) == len([g for g in paren_string.split(' ') if g != ''])
    post: all(x >= 1 for x in __return__)
    post: all(x == max_level(g) for x, g in zip(__return__, [g for g in paren_string.split(' ') if g != '']))
    """
    groups = [g for g in paren_string.split(' ') if g != '']
    result = []
    for group in groups:
        current_depth = 0
        max_depth = 0
        for ch in group:
            if ch == '(':
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif ch == ')':
                current_depth -= 1
        result.append(max_depth)
    return result


def max_level(group: str) -> int:
    """Helper function to compute the maximum nesting depth of a single group."""
    current_depth = 0
    max_depth = 0
    for ch in group:
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
