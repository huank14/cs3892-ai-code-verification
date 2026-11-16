# HumanEval/8: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | List of integers, including zero and negatives; exclude bool; no length bound | Copy _spec_int and suggested precondition | _spec_int |
| Return shape and order | reference.py task text and -> Tuple[int,int] | Tuple of exactly two integers: sum then product | Tuple/length/type guard and ordered equality | _spec_int |
| Sum | reference.py task text: sum of all integers | Include every occurrence with its sign | sum(numbers) | none |
| Product | reference.py task text: product of all integers | Multiply every occurrence with its sign; a zero makes product zero | Multiplicative fold from identity 1 | _spec_product |
| Empty input | reference.py explicitly specifies empty sum/product | [] -> (0,1) | Additive and multiplicative identities | _spec_product |
| Numeric edge cases | input_domain.md: Legal inputs | Unbounded Python integers; duplicates retained; no positivity or magnitude constraint | Full list reductions without bounds in the contract | _spec_product |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** The precondition preserves arbitrary signed integers and zeros while excluding bool as the frozen domain requires. The ordered tuple and integer type checks match the stated return type. Full sum/product equality counts every occurrence, with product identity 1 for the empty list. No magnitude restriction is added.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

[] -> (0, 1); [0] -> (0, 0); [-2, 3] -> (1, -6); [2, 2] -> (4, 4). Booleans and non-integer elements are outside the domain.

## Validation

- Canonical reference: `ACCEPTED_PROVEN_BOUNDED`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
