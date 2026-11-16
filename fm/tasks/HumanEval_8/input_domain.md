# HumanEval/8 input domain (`sum_product`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.
Executable form: `input_domain.py` (`in_domain(numbers)`).

## Legal inputs

`numbers`: a list of integers of any length, including the empty list, zero and negative
values. `bool` values are not integers for this task.

Expected result: the tuple `(sum(numbers), product of numbers)`, with `(0, 1)` for the
empty list.

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Non-integer elements | `[1.5]`, `['a']` |
| Booleans | `[True, 2]` |

## Rationale (from the task text, not from model outputs)

1. **Empty list is legal.** The task text states "Empty sum should be equal to 0 and empty
   product should be equal to 1", and the first official test is `[] -> (0, 1)`.
2. **Zero and negative integers are legal.** The task says "a given list of integers"
   without restriction; the official test `[100, 0] -> (100, 0)` uses zero.
3. **Booleans are excluded.** `bool` is a subclass of `int` in Python, but a list of truth
   values is not "a list of integers" in the task's sense; excluding it avoids crediting or
   penalising contracts for Python-specific type behaviour.

## Suggested precondition (for the human contract; D may rewrite)

```
pre: all(_spec_int(x) for x in numbers)
```

with `_spec_int` copied from `input_domain.py`.

## Consistency checks (16 November 2026)

- All five official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
