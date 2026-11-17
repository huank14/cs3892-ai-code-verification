# Composed by fm/pipeline. contract=human (from C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/human_contract.py), implementation=C:/dev-tools/cs3892-work/repo/fm/tasks/HumanEval_40/mutants/m4.py
# The docstring below is copied verbatim from the contract source.
# Signature annotations taken from the contract.
# Harness analysis bound (extra pre:): len(l) <= 4
# --- contract helpers ---
from typing import List
def _spec_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)
# --- implementation ---
# HumanEval canonical solution (MIT licence, openai/human-eval).
# Mutant m4 of HumanEval/40 (Zoey): checks pairs summing to zero instead of triples


def triples_sum_to_zero(l: List[int]) -> bool:
    """A zero-sum triple uses three positions; values at those positions may repeat.

    pre: len(l) <= 4
    pre: isinstance(l, list)
    pre: all(_spec_int(x) for x in l)
    post: isinstance(__return__, bool)
    post: __return__ == any(l[i] + l[j] + l[k] == 0 for i in range(len(l)) for j in range(i + 1, len(l)) for k in range(j + 1, len(l)))
    """
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[i] + l[j] == 0:
                return True
    return False
