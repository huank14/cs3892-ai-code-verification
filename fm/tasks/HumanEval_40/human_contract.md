# HumanEval/40: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | List of integers, excluding bool; no minimum length | Copy _spec_int; List[int] signature as explicitly requested by domain | _spec_int |
| Result type | reference.py task text: returns True / False | Return a bool | Boolean type guard | none |
| Existence in both directions | reference.py: three distinct elements sum to zero | True iff there exist i < j < k with l[i]+l[j]+l[k] == 0 | Equality to existential over index triples | none |
| Distinct positions, duplicate values | reference.py official example [1,3,-2,1]; input_domain.md: Rationale 2 | An index cannot be reused; duplicate values at different indices may participate | Strictly increasing indices; no set conversion | none |
| Empty and short lists | input_domain.md: Rationale 1 | Length < 3 -> False | Empty existential | none |
| Numeric / ordering behavior | input_domain.md: Legal inputs | Arbitrary signed integers and zeros; all triples, including nonconsecutive positions | Exact Python integer sum over all triples | none |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** List[int] and the copied integer predicate follow the frozen domain. Equality to existence over i < j < k specifies True and False, including short lists. It requires distinct positions without excluding repeated values. This interpretation is supported by the task example [1, 3, -2, 1], which needs two occurrences of 1.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

[] -> False; [0] -> False; [0, 0, 0] -> True; [1, 3, -2, 1] -> True. Booleans, floats and mixed element types are outside the domain.

## Validation

- Canonical reference: `ACCEPTED_PROVEN_BOUNDED`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
