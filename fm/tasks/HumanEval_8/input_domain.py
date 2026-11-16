"""Legal input domain of HumanEval/8 (rules and rationale: input_domain.md)."""


def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def in_domain(numbers) -> bool:
    return isinstance(numbers, list) and all(_spec_int(x) for x in numbers)
