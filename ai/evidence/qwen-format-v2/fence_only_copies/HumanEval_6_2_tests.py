__name__ = 'reviewed_under_test'
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """
    Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]

    pre: isinstance(paren_string, str)
    pre: all(c in '() ' for c in paren_string)
    pre: all(group.count('(') == group.count(')') for group in paren_string.split() if group)
    pre: all(
        sum(1 for c in group[: i + 1] if c == '(' ) >= sum(1 for c in group[: i + 1] if c == ')')
        for group in paren_string.split() if group
        for i in range(len(group))
    )
    post: isinstance(__return__, list)
    post: all(isinstance(x, int) for x in __return__)
    post: len(__return__) == len([g for g in paren_string.split() if g])
    post: __return__ == [
        max(
            (
                sum(1 for c in group[: i + 1] if c == '(') - sum(1 for c in group[: i + 1] if c == ')')
                for i in range(len(group))
            ),
            default=0,
        )
        for group in paren_string.split()
        if group
    ]
    """
    groups = [g for g in paren_string.split() if g]
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



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]

check(parse_nested_parens)
