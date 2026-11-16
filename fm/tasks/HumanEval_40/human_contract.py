# List[int] follows input_domain.md; the canonical implementation is unchanged.
from typing import List


def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def triples_sum_to_zero(l: List[int]) -> bool:
    """A zero-sum triple uses three positions; values at those positions may repeat.

    pre: isinstance(l, list)
    pre: all(_spec_int(x) for x in l)
    post: isinstance(__return__, bool)
    post: __return__ == any(l[i] + l[j] + l[k] == 0 for i in range(len(l)) for j in range(i + 1, len(l)) for k in range(j + 1, len(l)))
    """
    raise NotImplementedError
