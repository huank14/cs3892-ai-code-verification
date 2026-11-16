"""Legal input domain of HumanEval/6 (rules and rationale: input_domain.md)."""


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


def in_domain(paren_string) -> bool:
    return isinstance(paren_string, str) and (
        paren_string == '' or all(_spec_balanced_group(g) for g in paren_string.split(' ')))
