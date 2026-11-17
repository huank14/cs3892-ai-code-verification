# Milestone 1 — FM component (verification pipeline)

Bingsong Liu, Group E, CS 3892 / 5892. Status as of 16 November 2026.

## What the verifier checks

A contract c for a function f is a pair (pre_c, post_c) written as PEP 316 conditions in the
docstring; post_c is the conjunction of postconditions phi_1 ... phi_k. The verification target is
the Hoare triple

    {pre_c} f {post_c}   i.e.   for all x:  pre_c(x)  =>  post_c(x, f(x))     (terminating runs)

CrossHair (0.0.110, Z3 5.1.0) executes f on symbolic inputs, turns each branch into a path
condition, and asks Z3 for an input that satisfies pre_c and the path but falsifies phi_i.
For every postcondition phi_i it reports one of:

| CrossHair output | Meaning |
|---|---|
| `false when calling f(x)` | counterexample: pre_c(x) and not phi_i(x, f(x)) |
| `Confirmed over all paths` | every path under pre_c was explored and phi_i held (proof relative to CrossHair's model of Python) |
| `Not confirmed` | budget ended without either: inconclusive, not evidence of correctness |

**Bounded verification.** For each task T we fix one size bound B_T, the same for every contract,
and check {B_T and pre_c} f {post_c}. A confirmation then means "for all inputs within B_T".
B_T is inserted as the *first* precondition, and the analysis uses the contract's declared types.

| Task | B_T |
|---|---|
| HumanEval/0 | `len(numbers) <= 3` |
| HumanEval/6 | `len(paren_string) <= 4` |
| HumanEval/8 | `len(numbers) <= 4` |
| HumanEval/12, /28 | `len(strings) <= 3 and all(len(s) <= 3 for s in strings)` |
| HumanEval/40 | `len(l) <= 4` |

**Combined mode (reported results).** Each check runs bounded first. Unless that already produced a
re-executed rejection, an unbounded run also searches for counterexamples. A re-executed
counterexample from either run is a real input, so it counts as a rejection; an acceptance is
reported as `ACCEPTED_PROVEN_BOUNDED` (proof within B_T, no counterexample found beyond it).
Small bounds therefore do not hide mutants whose errors need longer inputs.

## From per-condition results to one verdict

For contract c and implementation g (reference, mutant, or Qwen implementation):

| Verdict | Rule |
|---|---|
| `REJECTED` | some phi_i has a counterexample x; re-running g(x) in a fresh process reproduces the violation; and (if g is not the reference) the reference satisfies c at x |
| `REJECTED_NONDISCRIMINATING` | g is rejected at x, but so is the reference: c did not tell g apart from the reference |
| `REJECTED_EXCEPTION` | g raises on an input satisfying pre_c (re-executed) |
| `ACCEPTED_PROVEN_BOUNDED` | every phi_i confirmed over all paths within B_T, and no counterexample in the unbounded search |
| `INCONCLUSIVE` | no counterexample, at least one phi_i not confirmed |

Mutation score over the validated mutant set M of a task:

    killed(c, m)  <=>  verdict(c, m) = REJECTED
    MS(c) = |{m in M : killed(c, m)}| / |M|

A contract that rejects the reference (symbolically or on an official-test input) is flagged
over-restrictive. Determinacy rate = (checks with REJECTED*, or ACCEPTED_PROVEN[_BOUNDED]) / all checks.

## Changes since the proposal

1. **Bounded verification (new).** Unbounded, with the proposal's 60 s per-condition budget,
   only 4 of the 38 Qwen checks (11%) were determinate: CrossHair never finishes exploring
   unbounded lists/strings. With one fixed size bound per task (combined mode, contract types):
   32 of 38 (84%), above the proposal's 80% criterion. Cause found in the
   process: CrossHair evaluates `pre:` lines in order, so the bound must precede any condition that
   iterates over the input (`all(isinstance(x, int) for x in l)`), or exploration never terminates.
2. **Declared types.** HumanEval/40's reference is annotated `l: list`; CrossHair then generates
   mixed-type lists (`['', 0, '']` raised `TypeError`). The analysis uses the contract's signature.
3. **Discriminating kills.** A mutant only counts as killed if the reference satisfies the
   contract on the same input; otherwise an over-restrictive contract would get credit.
4. **Concrete check** alongside the symbolic one: every contract is also evaluated on the official
   HumanEval test inputs and mutant witnesses (tested, not verified; reported separately).

## Preliminary results (Qwen contracts only; human contracts and mutants in progress)

The 19 Qwen contracts that parse, each checked against the HumanEval reference and against the
implementation Qwen generated in the same response ("own impl"). 38 checks, 60 s per postcondition.
Run on 15 November 2026 at commit `0032441` (CrossHair 0.0.110, Z3 5.1.0, Python 3.13.5, 28 cores):
`results/qwen-pilot-unbounded-t60/` and `results/qwen-pilot-combined-t60/`.

| Determinate checks | unbounded | combined |
|---|---|---|
| all 38 checks | 4 / 38 = 11% | **32 / 38 = 84%** |
| contract x reference | 2 / 19 = 11% | 15 / 19 = 79% |
| contract x own Qwen impl | 2 / 19 = 11% | 17 / 19 = 89% |

| Verdict (combined) | count |
|---|---|
| `ACCEPTED_PROVEN_BOUNDED` | 28 |
| `REJECTED` (reference rejected: contract defect) | 2 |
| `REJECTED_NONDISCRIMINATING` (own impl rejected, but so is the reference) | 2 |
| `INCONCLUSIVE` | 6 |

Per contract (U = unbounded, C = combined; P = `ACCEPTED_PROVEN_BOUNDED`, R = `REJECTED`,
N = `REJECTED_NONDISCRIMINATING`, I = `INCONCLUSIVE`):

| Task | Contract | reference U / C | own impl U / C | Note |
|---|---|---|---|---|
| HumanEval/0 | v2_0_2 | I / I | I / P | float lists: reference not confirmed even within B_T |
| HumanEval/0 | v2_0_3 | I / I | N / N | over-restrictive (`is not`), fails an official-test input |
| HumanEval/6 | v2_6_1 | R / R | I / P | rejects the reference on `''` |
| HumanEval/8 | v1_8_2 | I / I | I / I | `math.prod` (nonlinear) |
| HumanEval/8 | v1_8_3 | R / R | N / N | operator-precedence defect |
| HumanEval/8 | v2_8_2 | I / I | I / I | `math.prod` (nonlinear) |
| HumanEval/8 | v2_8_3 | I / P | I / P | |
| HumanEval/12 | v2_12_2, v2_12_3 | I / P | I / P | |
| HumanEval/28 | v1_28_1..3, v2_28_1..3 | I / P | I / P | all six |
| HumanEval/40 | v1_40_2, v2_40_1..3 | I / P | I / P | all four |

All six remaining inconclusive checks are the two known tool limits below (floats on /0,
nonlinear products on /8). Every rejection in both runs was re-executed in a fresh process; the
unbounded and combined runs found the same four rejections. No mutants or human contracts were
part of this run; mutation scores are in the full pilot run below.

Concrete contract defects found by CrossHair (each counterexample re-executed):

- `v1/HumanEval_8_3`: rejects the correct `(0, 0)` for `sum_product([0])`. The condition
  `r[1] == 1*r[1] if len(numbers) == 0 else r[1]` parses as `(...) if ... else r[1]`, so any
  correct product 0 is rejected (operator precedence).
- `v2/HumanEval_6_1`: rejects the reference on `''` (`len(r) == len(s.split(' '))` counts empty
  groups). Whether `''` is a legal input is an input-domain decision (C/D).
- `v2/HumanEval_0_3`: uses `b is not a` (object identity) for "different positions"; rejects the
  correct `True` on an official test input where equal floats are the same object.

## Full pilot run: human and Qwen contracts against the validated mutants

After Zoey's 36 validated mutants and Keyu's six human reference contracts were merged, one run
covered every job (16 November 2026, commit `57b315d`, same host and versions as above, combined
mode, 60 s): every contract (human + 19 parsed Qwen) x {reference, its task's 6 mutants}, the human
contract x every Qwen implementation, and every Qwen contract x its own implementation. 229 checks,
25 minutes: `results/pilot-full-combined-t60/`. Scoring follows `EVALUATION_PROTOCOL.md`
(MS_eff = 0 for a contract that rejects the reference on a legal input).

| Task | Human MS_eff | Qwen MS_eff, median (n) |
|---|---|---|
| HumanEval/0 | 1.00 | 0.50 (2) |
| HumanEval/6 | 1.00 | 0.00 (1) |
| HumanEval/8 | 1.00 | 0.75 (4) |
| HumanEval/12 | 1.00 | 1.00 (2) |
| HumanEval/28 | 1.00 | 1.00 (6) |
| HumanEval/40 | 1.00 | 1.00 (4) |
| all (mean) | 1.00 | 0.76 (19) |

- The human contracts kill all 36 mutants (re-executed, discriminating, all inputs in D_T) and
  never reject the reference (5 proven within B_T, HumanEval/0 inconclusive: floats).
- Four Qwen contracts score MS_eff = 0: three are over-restrictive (`v1_8_3`, `v2_6_1`,
  `v2_0_3`, above), and `v1_40_2` is too weak: its only postcondition is
  `isinstance(__return__, bool)`, so all six HumanEval/40 mutants are ACCEPTED_PROVEN_BOUNDED
  (verified wrong implementations).
- `v2_6_1`'s three raw kills are all at inputs outside D_T (e.g. `'\x00'`); in-domain kills: 0.
- Human contract x Qwen implementations (35): 27 proven within B_T, 6 inconclusive (all
  HumanEval/0), 2 rejected: `v1_6_2` and `v2_6_1` return `[0]` for the legal input `''`
  (reference: `[]`).
- Determinacy: 212/229 = 93% of all checks, 147/150 = 98% of contract x mutant checks.
- End-to-end view (17 Qwen samples that do not parse count as MS = 0) and per-prompt
  aggregation: Zoey (protocol items 3-4).

## Demo

    cd fm
    .venv/Scripts/python -m pipeline.demo --task HumanEval/40 --contract qwen_v1_40_2,human --impl mutant_m4 --bounded

One implementation (mutant m4: checks pairs instead of triples), two contracts, ~3 s. Shows each
contract's pre/post verbatim, the live CrossHair output, the counterexample re-executed in a fresh
process (with its D_T membership and the reference's output at the same input), and one verdict
line per contract: `qwen_v1_40_2  ACCEPTED_PROVEN_BOUNDED`, `human  REJECTED`. CrossHair is not
seeded, so the counterexample values differ between runs. Single-contract form:
`--contract qwen_v1_8_3 --impl reference` (the precedence defect).

## Reproduce

    cd fm
    .venv/Scripts/python -m pip install -r requirements.txt
    .venv/Scripts/python -m pipeline.run_matrix --tasks all --kinds reference,self --timeout 60 --mode unbounded --out results/qwen-pilot-unbounded-t60
    .venv/Scripts/python -m pipeline.run_matrix --tasks all --kinds reference,self --timeout 60 --mode combined --contract-signature --out results/qwen-pilot-combined-t60

Each run writes `run_meta.json` (versions, git commit, bounds), `results.jsonl` (every
per-condition report and replay), raw CrossHair logs, composed modules, and `summary.md`.
CrossHair's search is not seeded: counterexample inputs can differ between runs; verdicts are
computed from re-execution, not from CrossHair's text.

## Remaining work

- Done for the pilot (above). Replay now records `in_domain` for every counterexample, and
  over-restrictive is decided from legal-input rejections only (protocol items 1-2).
- Report both unbounded and combined results; bounded confirmations hold only within B_T.
- Known tool limits to report, not work around by editing contracts: nonlinear integer products
  (`math.prod` contracts on HumanEval/8 stay Not confirmed even at length <= 2) and float lists on
  HumanEval/0 (Not confirmed even at length <= 2).
- Scale to 30 tasks and the second model for the final.
