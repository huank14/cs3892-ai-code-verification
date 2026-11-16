"""Legal input domain of HumanEval/40 (rules and rationale: input_domain.md)."""


def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def in_domain(l) -> bool:
    return isinstance(l, list) and all(_spec_int(x) for x in l)
