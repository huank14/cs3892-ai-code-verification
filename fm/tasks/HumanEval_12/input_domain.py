"""Legal input domain of HumanEval/12 (rules and rationale: input_domain.md)."""


def in_domain(strings) -> bool:
    return isinstance(strings, list) and all(isinstance(s, str) for s in strings)
