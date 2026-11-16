# HumanEval/6 input domain (`parse_nested_parens`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.

## Legal inputs

`paren_string` is either

- the empty string `''` (zero groups; expected result `[]`), or
- one or more **groups** joined by **single spaces**, where each group is a non-empty
  string of `(` and `)` that is balanced: reading left to right the nesting depth never
  drops below 0 and ends at 0.

A group does not need a single outermost pair: `()()` is a legal group with depth 1.

Expected result: one integer per group, in order, equal to the maximum nesting depth of
that group (the canonical solution's behaviour on these inputs).

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Unbalanced group | `'(()'`, `')('` |
| Characters other than `(`, `)` and space | `'(a)'` |
| Leading, trailing or repeated spaces | `' ()'`, `'() '`, `'()  ()'` |

## Rationale (from the task text, not from model outputs)

1. **Empty string is legal.** The task describes "multiple groups ... separated by spaces"
   and does not exclude zero groups; the canonical solution returns `[]` for `''`.
   HumanEval/8, /12 and /28 explicitly treat empty input as legal, so this keeps one rule
   across the pilot tasks: an input the task text does not exclude, and on which the
   canonical solution behaves meaningfully, is legal.
2. **Groups need not have a single outer pair.** The text asks for "the deepest level of
   nesting" of each group, which is well-defined for any balanced string; all official
   examples happen to have one outer pair, but the text does not require it.
3. **Unbalanced groups and foreign characters are illegal.** The text speaks of groups of
   nested parentheses; the canonical solution's output on unbalanced strings has no
   meaning under the task.
4. **Only single spaces separate groups.** The text says "separated by spaces"; the strict
   reading avoids crediting or penalising contracts for whitespace handling the task never
   specifies.

## Disclosure

This decision was written after the FM pilot run (`fm/MILESTONE_FM.md`, 15 November 2026)
had reported that `qwen_v2_6_1` rejects the reference on `''`. The rules above are derived
from the task text and the cross-task consistency rule only. Under this domain that
rejection is a contract defect (false rejection of a correct output on a legal input).

## Suggested precondition (for the human contract; D may rewrite)

```
pre: paren_string == '' or all(_spec_balanced_group(g) for g in paren_string.split(' '))
```

```python
def _spec_balanced_group(g: str) -> bool:
    depth = 0
    for c in g:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0:
                return False
        else:
            return False
    return len(g) > 0 and depth == 0
```

`paren_string.split(' ')` yields an empty group for leading, trailing or repeated spaces,
which `_spec_balanced_group` rejects.

## Consistency checks (16 November 2026)

- All three official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
- The canonical solution returns `[]` on `''`.
