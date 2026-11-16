# How to add mutants (C)

1. Copy `tasks/HumanEval_<n>/reference.py` to `tasks/HumanEval_<n>/mutants/m<k>.py`; change only the function body.
2. Add an entry to `tasks/HumanEval_<n>/mutants/manifest.json` (see `mutants_manifest.json`):
   `witness.args` is the argument list (JSON), `expected` the reference output, `actual` the mutant output
   (or the string "raises"). The witness must be a legal input for the task.
3. Run `.venv/Scripts/python -m pipeline.validate_mutants HumanEval/<n>` (add `--diffbehavior` for a CrossHair check).
   Every mutant must print VALID. Results go to `mutants/validation.json`.
