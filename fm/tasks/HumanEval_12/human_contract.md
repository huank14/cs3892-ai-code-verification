# HumanEval/12: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | List of strings; [] and empty/repeated strings allowed | Suggested precondition plus list check | none |
| Empty behavior | reference.py: Return None in case input list is empty | None exactly for empty input | Explicit empty branch | none |
| Membership / result type | reference.py: Out of list of strings, return the longest one | Nonempty input returns a string occurring in the input | Membership and type predicate | _spec_first_longest |
| Maximum length | reference.py: return the longest one | Result length >= every candidate length | Universal length comparison | _spec_first_longest |
| First among ties | reference.py: Return the first one in case of multiple strings of same length | Every string preceding the first occurrence of the returned value is shorter | Strict length comparison over preceding prefix | _spec_first_longest |
| Duplicates and empty strings | input_domain.md: Rationale 2 | Repeated identical strings are indistinguishable by value; a nonempty all-empty list returns empty string | Membership, maximum and earliest-value semantics | _spec_first_longest |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** The empty branch requires None exactly. For nonempty input, membership and the maximum-length test prevent invented or shorter results. Every entry before the first occurrence of the returned value must be strictly shorter, which enforces the first-among-ties rule. Repeated equal strings are indistinguishable by value; the task does not require object identity.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

[] -> None; [''] -> ''; ['aa', 'bb'] -> 'aa'; ['a', 'bbb', 'bbb'] -> 'bbb'. Non-string elements and non-list containers are outside the domain.

## Validation

- Canonical reference: `ACCEPTED_PROVEN_BOUNDED`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
