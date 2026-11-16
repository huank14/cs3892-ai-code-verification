# Evaluation protocol: from CrossHair verdicts to reported numbers

**Status: DRAFT for sign-off**, Zoey (C), 16 November 2026.
Owner: C (evaluation, input domains, mutants). Needs agreement from Bingsong (B,
verdicts/pipeline) and Keyu (D, human contracts) before any mutation score is reported.

| Sign-off | Name | Date |
|---|---|---|
| C, evaluation | Zoey | |
| B, pipeline | Bingsong | |
| D, human contracts | Keyu | |

This document fixes how per-check verdicts become the numbers on the slides. It builds on the
verdict definitions in `fm/README.md` and `fm/MILESTONE_FM.md` (B) and on the success
criterion in the proposal (Section 5). Where it changes the current pipeline, the change is
listed in Section 9.

## 1. Objects

| Symbol | Meaning | Where |
|---|---|---|
| T | a HumanEval task | `fm/tasks/HumanEval_<n>/` |
| D_T | legal input domain of T (fixed by C from the task text) | `input_domain.md`; executable `input_domain.py:in_domain` |
| ref_T | canonical HumanEval solution | `reference.py` |
| M_T | validated mutants of T (VALID in `validation.json`) | `mutants/` |
| c | a contract: PEP 316 `pre:` / `post:` in a docstring | Qwen samples, `human_contract.py` |
| B_T | analysis bound, inserted as the first `pre:` in bounded runs | `task.json` |

Every D_T must contain all official-test inputs of T, and every mutant witness must lie in
D_T (checked when D_T is written; done for all six pilot tasks).

A **sample** is one attempted model response (one model, one prompt version, one task, one
of three conversations). Every sample is evaluated, whether or not its contract parses.

## 2. Frozen before results

The following are fixed before the run whose numbers are reported, and are not changed
afterwards to improve or worsen any contract's score:

- task list; D_T for every task; M_T for every task (mutants are added, never removed after
  results, unless found INVALID by `validate_mutants`);
- B_T, `--mode combined`, `--contract-signature`, 60 s per-condition timeout, CrossHair and
  Z3 versions (recorded in `run_meta.json`);
- this protocol.

Pilot disclosure: for the six pilot tasks, the mutants and the input domains were
written after the AI and FM pilot reports were available (no contract was run against the
mutants before they were frozen). For the final 30 tasks, D_T and M_T are written before
any contract is run on those tasks.

## 3. Contract-level status (before any mutant)

Each sample's contract gets exactly one status, taken from `ai/analysis/samples.json`
(`contract_parser_status`) and the pipeline:

| Status | Rule | Enters MS? |
|---|---|---|
| `GENERATION_FAILURE` | `contract_parser_status != parsed` (PEP 316 syntax error, missing postcondition, invalid Python), or pipeline `CONTRACT_INVALID` / `CONTRACT_LOAD_ERROR` | yes, with MS = 0 (end-to-end view, Section 6) |
| `VACUOUS_PRE` | `PRE_UNSAT` on the reference: no input satisfies the precondition | yes, MS = 0 |
| `OVER_RESTRICTIVE` | the contract rejects ref_T on a **legal** input: a re-executed symbolic counterexample x with x in D_T, or a post violation or contract error in the concrete check (official-test and witness inputs are legal by construction) | raw MS reported; effective MS = 0 (Section 5) |
| `DOMAIN_EXCLUDING` | the precondition is false on a legal input (concrete `pre_excluded > 0`) | MS as computed; fails the proposal's "useful" test |
| `ANALYSABLE` | none of the above | MS as computed |

A contract can be both `OVER_RESTRICTIVE` and `DOMAIN_EXCLUDING`; both flags are reported.

A symbolic rejection of ref_T at an input **outside** D_T is not a defect (the task requires
nothing there). It is recorded as `constrains_illegal_inputs` and does not make the contract
over-restrictive.

Examples (pilot, from `fm/MILESTONE_FM.md`):
- `qwen_v2_6_1` rejects ref on `''`. `''` is legal (`HumanEval_6/input_domain.md`), so
  `OVER_RESTRICTIVE`.
- `qwen_v2_0_3` rejects the correct `True` on an official-test input: `OVER_RESTRICTIVE`.
  Its `threshold > 0` precondition also excludes the legal `threshold = 0`
  (`HumanEval_0/input_domain.md`): `DOMAIN_EXCLUDING`.
- `qwen_v1_8_3` rejects the correct `(0, 0)` for `[0]`: `OVER_RESTRICTIVE`.

## 4. Contract-mutant verdict to killed / not killed

One check = one contract c against one mutant m in M_T, verdict from
`pipeline/run_matrix.py:verdict` (combined mode).

| Verdict | killed(c, m)? | Notes |
|---|---|---|
| `REJECTED` | **yes** | re-executed counterexample; ref satisfies c at the same input |
| `REJECTED_EXCEPTION` | no | m raises on an input satisfying pre_c; detection does not depend on post_c. Count reported separately |
| `REJECTED_NONDISCRIMINATING` | no | ref is rejected at the same input |
| `ACCEPTED_PROVEN` / `ACCEPTED_PROVEN_BOUNDED` | no | **a verified wrong implementation**: the proposal's vacuity evidence. Every such (c, m) pair is listed in the report |
| `INCONCLUSIVE` | no | budget ran out; not evidence either way |
| `PRE_UNSAT` | no | contract is `VACUOUS_PRE` |
| `CONTRACT_ERROR`, `TOOL_ERROR`, `COMPOSE_ERROR` | no | rerun once with identical settings; if it persists, keep as not killed, stay in the denominator, list it |

Domain check on kills (sensitivity, not primary): every `REJECTED` input x is also tested for
x in D_T. The primary score counts the kill either way, because m is independently known to
be wrong on a legal input (its witness) and the contract separated m from ref at x. The report
gives the MS restricted to in-domain kills next to it and lists any difference.

## 5. Mutation score of one contract

    MS(c)     = |{m in M_T : killed(c, m)}| / |M_T|
    MS_eff(c) = MS(c)  if status is ANALYSABLE or DOMAIN_EXCLUDING
              = 0      if GENERATION_FAILURE, VACUOUS_PRE or OVER_RESTRICTIVE

The denominator is all of M_T, including mutants whose check ended INCONCLUSIVE or in a tool
error. MS_eff is the headline number; MS is always reported next to it.

Why over-restrictive contracts get MS_eff = 0: a contract that rejects correct code cannot be
used to verify anything, and crediting its kills would reward over-restriction (FM handoff:
"a contract rejecting every output should not score as strong"). B's discriminating rule
already removes kills where ref fails at the same input; MS_eff additionally covers kills at
other inputs.

**Useful contract** (proposal Section 5): parsed, not `VACUOUS_PRE`, not `OVER_RESTRICTIVE`,
not `DOMAIN_EXCLUDING`, and MS(c) >= 0.60. The report gives the number of useful contracts
out of all samples.

## 6. Denominators

Two views, always both reported, never mixed in one number:

| View | Population | Question it answers |
|---|---|---|
| **End-to-end** (primary) | every attempted sample: 3 per task per model per prompt version | how strong is what the model actually produces? |
| **Conditional** | samples with `contract_parser_status = parsed` | how strong are the contracts that can be checked at all? |

Generation-failure rate = `GENERATION_FAILURE` samples / attempted samples, reported by model
and prompt version, with the failure categories.

Pilot (Qwen, 6 tasks, 36 samples): 19 parsed, 17 generation failures (15 PEP 316 syntax
errors, 1 missing postcondition, 1 invalid Python). Parsed per task: /0 2, /6 1, /8 4,
/12 2, /28 6, /40 4.

## 7. Aggregation

Prompt versions and models are never pooled. V1 and V2 are separate rows; in the final
evaluation each model is reported under the frozen prompt only.

**Primary comparison (as in the proposal):**

    median_LLM   = median of MS_eff(c) over all samples of the model (end-to-end view)
    median_human = median of MS_eff over the human contracts (one per task)
    gap          = median_human - median_LLM, in percentage points

Comparable strength: gap <= 15 points. Also reported for MS (raw) and for the conditional view.

**Paired per-task view (secondary, more informative on the same tasks):**

    task score  S_LLM(T) = mean of MS_eff over the 3 samples of T
    difference  d(T)     = MS_eff(human_T) - S_LLM(T)

Reported: d(T) for every task, mean and median of d, number of tasks with d > 0.15.

Also reported per model and prompt version: mean MS_eff, the number of samples with
MS_eff = 0 and = 1, the useful-contract count, and the over-restrictive count.

The human contract is evaluated with exactly the same rules (it can also be
`OVER_RESTRICTIVE` or `DOMAIN_EXCLUDING`; D checks this before the run, as required by
`tasks/_templates/human_contract.py`).

## 8. Determinate-verdict rate (proposal success criterion)

    determinacy = (contract-mutant checks with REJECTED, REJECTED_EXCEPTION,
                   REJECTED_NONDISCRIMINATING, ACCEPTED_PROVEN or ACCEPTED_PROVEN_BOUNDED)
                  / (all contract-mutant checks run)

Only parsed contracts produce checks, so generation failures are outside this denominator
(they are already counted in Section 6). Target: >= 80% at the 60 s per-condition timeout.
Reported for combined and unbounded mode. `ACCEPTED_PROVEN_BOUNDED` holds only within B_T;
the proposal's "confirmation over all paths" is met in full only by `ACCEPTED_PROVEN`, and
the report says so.

Also reported on contract x reference and contract x own-implementation checks, as in B's
milestone, but the success criterion is the contract-mutant rate.

## 9. Required pipeline changes

| # | Change | Who |
|---|---|---|
| 1 | Machine-readable D_T predicate per task, and `in_domain` recorded for every replayed input | C: done (`tasks/HumanEval_<n>/input_domain.py`, function `in_domain` with the task's parameters); B: call it in replay |
| 2 | `over_restrictive` only from in-domain reference rejections (now: any `REJECTED` on ref) | B |
| 3 | Summary includes generation-failure samples (MS = 0) and reports `MS_eff`, `useful`, `domain_excluding` per contract | C (aggregation script on `results.jsonl` + `samples.json`) |
| 4 | Per model/prompt table: medians, means, gap to human, paired d(T) | C |
| 5 | Listing of every `ACCEPTED_PROVEN*` contract-mutant pair (verified wrong implementations) | C |

## 10. Open questions for sign-off

1. **MS_eff = 0 for over-restrictive contracts.** Alternative: report raw MS only, with a flag.
   Proposed: MS_eff headline, raw MS beside it.
2. **`REJECTED_EXCEPTION` not counted as a kill.** None of the 36 pilot mutants raises on its
   witness; revisit if the final mutants include crashing ones.
3. **Persistent `TOOL_ERROR`** stays in the denominator as not killed (conservative).
   Alternative: exclude and report.
4. **Bounded acceptance in the 80% criterion.** Proposed: counted as determinate, disclosed,
   and the unbounded rate reported beside it.
5. **Final prompt version** for both models (V2 was designed after inspecting V1).

Resolved: input domains for the six pilot tasks are fixed by C in each task's
`input_domain.md` (16 November 2026).

## 11. Limits that the report must state

- The six pilot tasks were purpose-selected; pilot numbers are descriptive, not estimates.
- V2 was designed after V1's format errors were inspected.
- MS depends on the mutant set; with |M_T| = 6, one mutant is about 17 points on one contract.
- Combined-mode acceptance is bounded by B_T. INCONCLUSIVE is never read as correct.
- Known tool limits (B): nonlinear products on HumanEval/8 and float lists on HumanEval/0 stay
  Not confirmed; these lower determinacy and can lower MS without any contract defect.
- Kills count only symbolic, re-executed, discriminating counterexamples. The concrete check
  on official-test and witness inputs is tested, not verified, and is reported separately.
