# HumanEval/28 input domain (`concatenate`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.
Executable form: `input_domain.py` (`in_domain(strings)`).

## Legal inputs

`strings`: a list of strings of any length, including the empty list, empty strings and
repeated strings.

Expected result: the strings joined in order with no separator (`''` for the empty list).

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Non-string elements | `['a', 1]`, `[None]` |

## Rationale (from the task text, not from model outputs)

1. **Empty list is legal.** The task's own example is `concatenate([]) -> ''`, and the first
   official test is `[] -> ''`.
2. **Empty and repeated strings are legal.** "Concatenate list of strings into a single
   string" places no restriction on the strings.

## Suggested precondition (for the human contract; D may rewrite)

```
pre: all(isinstance(s, str) for s in strings)
```

## Consistency checks (16 November 2026)

- All three official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
