# HumanEval/28: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | List of arbitrary strings; empty and duplicate entries allowed | Suggested precondition plus list check | none |
| Result type | reference.py: -> str | Return a string | Type guard | none |
| Length / no separator | reference.py: concatenate; input_domain.md: Expected result | Output length equals sum of lengths; no extra separator characters | Total length equality | _spec_concatenation |
| Content and order | reference.py: concatenate; input_domain.md: joined in order | Each input string occupies its cumulative-offset output segment | Segment equality for each position | _spec_concatenation |
| Duplicates / empty strings | input_domain.md: Rationale 2 | Every occurrence retained; empty strings contribute zero length | Iterate all positions, no deduplication or sorting | _spec_concatenation |
| Empty list | reference.py example concatenate([]) -> empty string | [] -> empty string | String type plus length zero | _spec_concatenation |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** The output is a string of exactly the sum of all input lengths. Cumulative-offset segment equalities then cover the whole output in input order. This rules out insertion, omission, sorting and deduplication. Empty segments add no length, and the empty input forces the empty string.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

[] -> ''; ['b', '', 'a', 'b'] -> 'bab'; ['x', 'x'] -> 'xx'. Arbitrary string characters are legal; non-string elements are not.

## Validation

- Canonical reference: `ACCEPTED_PROVEN_BOUNDED`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
