# HumanEval/0 input domain (`has_close_elements`)

Owner: Zoey (C). Decided 16 November 2026. Applies to the human reference contract,
mutant witnesses, and the interpretation of every contract verdict on this task.
Executable form: `input_domain.py` (`in_domain(numbers, threshold)`).

## Legal inputs

- `numbers`: a list of finite floats, of any length, including the empty list and a
  single element.
- `threshold`: a finite float with `threshold >= 0`, including `0.0`.

Expected result: `True` if and only if there are two **different positions** `i != j` with
`abs(numbers[i] - numbers[j]) < threshold`, computed in floating point as the canonical
solution does; otherwise `False`. Equal values at different positions count as close for
any positive threshold.

## Illegal inputs (outside the precondition; no behaviour required)

| Input kind | Example |
|---|---|
| Negative threshold | `([1.0, 2.0], -1.0)` |
| NaN or infinity anywhere | `([float('nan')], 1.0)`, `([1.0], float('inf'))` |
| Non-float elements or threshold | `([1, 2], 0.5)`, `([1.0], 1)` |

## Rationale (from the task text, not from model outputs)

1. **Empty and single-element lists are legal.** "Are any two numbers closer ... than the
   threshold" has the answer `False` when there are fewer than two numbers; the task does not
   exclude them, and the canonical solution returns `False`. Same cross-task rule as
   HumanEval/6: an input the task text does not exclude, on which the canonical solution
   behaves meaningfully, is legal.
2. **`threshold = 0` is legal.** "Closer than 0" is well-defined and never true, so the
   answer is `False`.
3. **Negative thresholds are illegal.** The threshold bounds a distance, and distances are
   non-negative; a negative value is not a meaningful distance threshold.
4. **"Any two numbers" means two positions.** The canonical solution compares indices
   (`idx != idx2`), and the official test `[1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1 -> True`
   relies on two equal values at different positions.
5. **Finite floats only.** The signature is `List[float]` / `float`; with NaN or infinity
   the distance comparison has no meaning under the task.

## Disclosure

Written after the AI and FM pilot reports. Under this domain, the pilot contract
`qwen_v2_0_3` (`pre: threshold > 0`) excludes the legal inputs with `threshold = 0`
(DOMAIN_EXCLUDING). It is OVER_RESTRICTIVE independently of this decision, because it
rejects the correct `True` on an official-test input.

## Suggested precondition (for the human contract; D may rewrite)

```
pre: all(_spec_finite_float(x) for x in numbers)
pre: _spec_finite_float(threshold) and threshold >= 0
```

with `_spec_finite_float` copied from `input_domain.py`.

## Consistency checks (16 November 2026)

- All seven official-test inputs are legal.
- All six mutant witnesses in `mutants/manifest.json` are legal.
