# Does HumanEval create a ceiling effect?

The concern is plausible, not established. Easy implementation does not establish
complete contracts. A model may write correct code while omitting tie-breaking,
order, duplicates, empty cases, or the reverse direction of a Boolean property.
Conversely, a complete executable reference inside a contract can make these
tasks genuinely easy while being expensive for CrossHair to analyze.

## Pilot, fixed before generation

Use HumanEval/0, /6, /8, /12, /28, /40; 3 outputs each/model. This is a purposive
development sample, not the final random/representative evaluation and not a
license to discard high-scoring tasks. Preserve the existing 30-task scope.

For each sample distinguish:

1. Generation/format compatibility.
2. Implementation behavior (tests; do not call this formal proof).
3. Contract validity on task-correct behavior and valid inputs.
4. Contract sensitivity to the same independently validated incorrect mutants.
5. CrossHair counterexample / confirmed / inconclusive / tool-error outcomes.

Predeclared mutant categories for C/B to instantiate and validate:

| Task | Examples of errors to probe |
|---|---|
| /0 close elements | `<` vs `<=`; self-pair; adjacent-only; missing a pair |
| /6 nested parentheses | final depth vs peak depth; group order; one missing group |
| /8 sum/product | product initialized to 0; omitted element; empty identity |
| /12 longest | last tied maximum; return length; wrong empty result |
| /28 concatenate | reversed order; removed duplicates; separator inserted |
| /40 triples | repeated index; only adjacent triples; exactly-zero vs nonpositive |

These are categories, not yet an implemented or validated mutant benchmark.
Reference behavior is judged against the task, not merely against generated code.

## Decide before the main evaluation

Flag a possible measurement ceiling if, on this pilot, both models' per-task
median mutation scores are >=90% on at least 5/6 tasks, human baselines show a
similar ceiling, and >=80% of checks have determinate verdicts. These thresholds
are a proposed development rule, not an observed outcome or a significance test.
With five mutants/task scores are quantized in 20-point increments; >=90% means
5/5 and makes a 15-point gap hard to resolve. Prefer a richer, shared mutant pool
before replacing the benchmark. Use paired task-level comparisons with 3 outputs
aggregated per model/task; do not treat correlated mutants as independent tasks.

High rates of invalid contracts or CrossHair timeouts are compatibility/budget
problems, not evidence the model has solved the task. A contract that rejects
correct reference behavior or valid inputs must not receive a strength claim
merely because it rejects all mutants (e.g. `post: False`).

If a ceiling persists, predeclare an additional specification-quality analysis
(redundant vs essential clauses, false rejection, contract evaluation cost) or
seek team/instructor agreement on an extension. Report saturated results honestly.
Do not weaken prompts/models until they fail, select only failures, add arbitrary
input restrictions, or change the 60%/15-point proposal targets after results.

HumanEval is public and may be familiar to models. No pilot here establishes lack
of training contamination. Do not claim novel algorithm generalization.
