# HumanEval/<n> human reference contract

| Requirement (from the task text) | Condition (line in human_contract.py) | Example input -> expected |
|---|---|---|
| empty list returns None | `post: len(strings) > 0 or __return__ is None` | `[] -> None` |

Input domain (agreed with C): ...

LLM assistance: which model, what it was asked, what was kept / changed by hand.
Written before looking at the Qwen contracts: yes/no.
