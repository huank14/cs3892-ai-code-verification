# Human Reference Contract Provenance

This file records the provenance and review status of the six pilot reference contracts owned by Keyu Huang for the CS 3892 Topic 7 milestone.

## Baseline Label

For the six-task milestone pilot, these specifications are described as **human-reviewed reference contracts**.

ChatGPT assisted with translating manually determined requirements into PEP 316 syntax, checking contract syntax, and improving documentation. Keyu determined and reviewed the task semantics, input domains, final contract conditions, and interpretation of CrossHair results. AI was not used to alter experimental outputs or determine conclusions.

Keyu Huang subsequently reviewed the substantive specification conditions against:

- the original HumanEval task statement;
- the frozen task-specific `input_domain.md`;
- the canonical HumanEval implementation;
- relevant boundary, empty-input, duplicate, ordering, and tie-breaking behavior.

The final six contracts below required no substantive semantic changes after this review.

The final project report will disclose AI assistance in the required AI-use disclosure.

---

## Semantic Review Status

| Task | Review result | Key semantic point |
|---|---|---|
| HumanEval/0 | Reviewed; no semantic change required | The result is true iff two different positions have distance strictly less than `threshold`. `threshold = 0` remains legal. |
| HumanEval/6 | Reviewed; no semantic change required | The result contains the maximum nesting depth of each balanced parenthesis group, preserving group order. |
| HumanEval/8 | Reviewed; no semantic change required | The result is `(sum, product)`; the empty-list case is `(0, 1)`. Zero, negative integers, and duplicates remain legal. |
| HumanEval/12 | Reviewed; no semantic change required | Empty input returns `None`; otherwise the result has maximum length and must be the first maximum-length string. |
| HumanEval/28 | Reviewed; no semantic change required | The result is the exact concatenation of all strings in input order, with no separator; empty and repeated strings remain legal. |
| HumanEval/40 | Reviewed; no semantic change required | The result is true iff three distinct positions `i < j < k` sum to zero; the values themselves need not be distinct. |

Semantic review completed: **November 16, 2026**.

---

## Review Criteria

Each contract was checked for the following specification defects:

### Too strong

The contract must not reject behavior allowed by the task or the frozen legal input domain.

### Too weak

The contract must encode the task's important semantic requirements rather than only easily checked output properties.

### Overly restrictive precondition

The precondition must not exclude inputs that the frozen `input_domain.md` classifies as legal.

### Edge-case coverage

Where applicable, the review checked:

- empty inputs;
- boundary values;
- duplicate values;
- ordering;
- tie-breaking;
- short inputs;
- task-specific special cases.

No substantive defect requiring a contract change was identified in the six reviewed pilot contracts.

---

## Validation Relationship

Semantic review and tool validation are separate checks.

Semantic review asks whether the specification expresses the intended task behavior.

CrossHair validation asks whether the canonical implementation or a mutant satisfies that specification under the project's analysis settings.

Current validation evidence is recorded separately in:

- `fm/keyu/VALIDATION.md`
- the corresponding result directories under `fm/results/`

The current pilot results should not be interpreted as proving that the reference contracts are complete specifications for every possible implementation error. They are evaluated against the six purpose-selected pilot tasks and the current validated mutant set.

---

## Ownership

**Keyu Huang**
- human reference specification review;
- contract-to-task semantic checking;
- integration of reference contracts with the shared verification pipeline;
- reproducibility documentation for this portion of the milestone.

The frozen input domains and mutant construction are owned by the corresponding team members and are not redefined in this file.
