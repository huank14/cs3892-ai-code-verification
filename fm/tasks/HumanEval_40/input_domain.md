# HumanEval/40 input domain (`triples_sum_to_zero`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.
Executable form: `input_domain.py` (`in_domain(l)`).

## Legal inputs

`l`: a list of integers of any length, including the empty list and lists with fewer than
three elements. `bool` values are not integers for this task.

Expected result: `True` if and only if there are three **different positions**
`i < j < k` with `l[i] + l[j] + l[k] == 0`; otherwise `False` (always `False` for fewer
than three elements).

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Non-integer or mixed-type elements | `['', 0, '']`, `[1.5, -1.5, 0]` |
| Booleans | `[True, False, -1]` |

## Rationale (from the task text, not from model outputs)

1. **Short lists, including the empty list, are legal.** The task says it "takes a list of
   integers" without a length requirement; with fewer than three elements no triple exists,
   so the answer is `False`. The official test `[1] -> False` uses a short list.
2. **"Three distinct elements" means three positions, not three values.** The official test
   `[1, 3, -2, 1] -> True` is true only through `1 + 1 + (-2)`, which uses the value 1 twice
   at different positions; the canonical solution compares indices.
3. **Integers only.** The reference is annotated `l: list`, but the task text says "a list of
   integers". Mixed-type lists (for example the `['', 0, '']` input CrossHair produced in the
   FM pilot) are outside the task.
4. **Booleans are excluded**, as for HumanEval/8.

## Suggested precondition (for the human contract; D may rewrite)

```
pre: all(_spec_int(x) for x in l)
```

with `_spec_int` copied from `input_domain.py`. The human contract should declare
`l: List[int]` so that CrossHair generates integer lists (`--contract-signature`).

## Consistency checks (16 November 2026)

- All nine official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
