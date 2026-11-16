# HumanEval/0: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | Finite float list; finite threshold >= 0; empty/singleton lists allowed | Exact domain helpers and preconditions | _spec_finite_float |
| Boolean result | reference.py: -> bool; input_domain.md: Expected result | Return a bool | Guard in postcondition | none |
| Existence in both directions | reference.py: any two numbers closer than threshold | True iff some i < j has abs(numbers[i]-numbers[j]) < threshold | Equality to an existential over index pairs | none |
| Positions, duplicates, order | input_domain.md: Rationale 4 | Compare distinct positions; equal values at different positions count; consider every pair | i < j enumeration | none |
| Boundary and empty behavior | input_domain.md: Rationale 1-2; strict closer-than wording | Fewer than 2 items or threshold 0 returns False; equality at threshold is False | Implied by empty existential and strict < | none |
| Numeric behavior | input_domain.md: Expected result | Python floating-point subtraction/abs; no tolerance or rational approximation | Use abs(x-y) < threshold unchanged | none |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** Finite floats and a nonnegative finite threshold match the frozen domain exactly. Equality to an existential over i < j covers both Boolean outcomes. Strict < preserves the threshold boundary, and different indices permit repeated values. Floating-point subtraction uses the same arithmetic as the task.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

([], 0.0) -> False; ([1.0], 1.0) -> False; ([0.0, 0.0], 0.0) -> False; ([0.0, 0.0], 0.5) -> True. NaN, infinity, integer elements and negative thresholds are outside the frozen domain.

## Validation

- Canonical reference: `INCONCLUSIVE`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
