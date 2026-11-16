# HumanEval/12 input domain (`longest`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.
Executable form: `input_domain.py` (`in_domain(strings)`).

## Legal inputs

`strings`: a list of strings of any length, including the empty list, empty strings and
repeated strings.

Expected result: `None` for the empty list; otherwise the first string (lowest index) whose
length equals the maximum length in the list.

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Non-string elements | `['a', 1]`, `[None]` |

## Rationale (from the task text, not from model outputs)

1. **Empty list is legal.** The task text says "Return None in case the input list is
   empty", and the first official test is `[] -> None`.
2. **Empty and repeated strings are legal.** The task does not restrict the strings; ties
   are resolved by the stated rule "Return the first one in case of multiple strings of the
   same length".

## Suggested precondition (for the human contract; D may rewrite)

```
pre: all(isinstance(s, str) for s in strings)
```

## Consistency checks (16 November 2026)

- All three official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
