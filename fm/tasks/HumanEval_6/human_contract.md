# HumanEval/6: requirements and semantic check

## Requirements and contract mapping

| Requirement | Source | Required behavior | PEP 316 encoding | Helper |
|---|---|---|---|---|
| Input domain | input_domain.md: Legal inputs / Suggested precondition | Empty string or balanced nonempty groups separated by single spaces; ()() is legal | Copy balance helper and suggested precondition | _spec_balanced_group |
| Result type | reference.py: -> List[int]; task: deepest level | List of integers | List/type guard | none |
| One depth per group in order | reference.py task text: for each group; input_domain.md: Expected result | Preserve group order and cardinality | Equality to ordered depth list | _spec_group_depth |
| Maximum depth | reference.py task text: deepest level; examples | For each group, maximum prefix balance, not final balance or total opens | max over prefix opening count minus closing count | _spec_group_depth |
| Empty and boundaries | input_domain.md: Rationale 1-2 | Empty string -> []; () and ()() -> [1]; nesting counts all levels | Empty group list and prefix definition | _spec_group_depth |


All listed properties are expressible in PEP 316 using the shown helpers.
Input-domain authority: `input_domain.md` and `input_domain.py` at base
`80429feb9e2114280323ff9f53eb3f622c0c26af`. Search-size bounds stay in `task.json`.

## Semantic check

**No semantic change required.** The precondition accepts the empty string or exactly the frozen balanced-group grammar. Maximum prefix balance is the nesting depth. Equality to the ordered depth list fixes values, order and number of outputs. A group may contain several outer pairs, so ()() remains legal. Single-space separation is a frozen domain assumption, not a claim about every possible reading of the original task.

Classification: appropriate on the frozen domain. No too-strong condition,
missing task requirement, or additional precondition restriction was identified.
This is a condition-by-condition semantic argument, not a universal verifier proof.

## Boundary examples

'' -> []; '()() ((()))' -> [1, 3]; '(()()) ()' -> [2, 1]. Unbalanced groups, foreign characters, and leading, trailing or repeated spaces are outside the frozen domain.

## Validation

- Canonical reference: `ACCEPTED_PROVEN_BOUNDED`; no reference rejection observed.
- Shared mutants: 6/6 caught by replayed, discriminating, in-domain counterexamples.
- Original experiment records are unchanged. Details and limits:
  [`../../keyu/VALIDATION.md`](../../keyu/VALIDATION.md).
