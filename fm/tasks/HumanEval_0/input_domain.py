"""Legal input domain of HumanEval/0 (rules and rationale: input_domain.md)."""


def _spec_finite_float(x) -> bool:
    return isinstance(x, float) and x == x and abs(x) != float('inf')


def in_domain(numbers, threshold) -> bool:
    return (isinstance(numbers, list)
            and all(_spec_finite_float(x) for x in numbers)
            and _spec_finite_float(threshold) and threshold >= 0)
