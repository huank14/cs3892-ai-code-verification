__name__ = 'reviewed_under_test'
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """
    pre:
        all(c in '() ' for c in paren_string)
        all(group.count('(') == group.count(')') for group in paren_string.split() if group)
        # For each group, at no point while scanning left-to-right does the number of ')' exceed the number of '('.
        # This is encoded via a helper below.
        all(_is_balanced(g) for g in paren_string.split() if g)

    post:
        len(__return__) == len([g for g in paren_string.split() if g])
        all(v >= 1 for v in __return__)
        # For each group, the returned value equals the maximum nesting depth.
        all(
            v == _max_depth(g)
            for v, g in zip(__return__, [g for g in paren_string.split() if g])
        )
    """
    results: List[int] = []
    for group in paren_string.split():
        if not group:
            continue
        depth = 0
        max_depth = 0
        for ch in group:
            if ch == '(':
                depth += 1
                if depth > max_depth:
                    max_depth = depth
            elif ch == ')':
                depth -= 1
        results.append(max_depth)
    return results


def _is_balanced(s: str) -> bool:
    """Helper for the contract: check that s is a valid balanced paren string."""
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                return False
        else:
            return False
    return depth == 0


def _max_depth(s: str) -> int:
    """Helper for the contract: compute the maximum nesting depth of a balanced paren string."""
    depth = 0
    max_depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
            if depth > max_depth:
                max_depth = depth
        elif ch == ')':
            depth -= 1
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
