# Verifying AI-Generated Code: Specifications as the Contract

CS 3892 / 5892 — Fall 2026  
Group E — Topic 7

## Team

- Jiahao Zhang
- Bingsong Liu
- Zoey Tang
- Keyu Huang

## Project

This project studies whether LLM-generated formal specifications are strong
enough to detect incorrect AI-generated implementations.

We use PEP 316 contracts and CrossHair to analyze Python programs from
HumanEval. Contract strength will be evaluated using deliberately incorrect
mutants and compared with human-written reference contracts.

## Planned Toolchain

- Python
- PEP 316 contracts
- CrossHair
- Z3
- OpenAI HumanEval

## Experimental Plan

- 30 deterministic HumanEval tasks
- DeepSeek-V4.1-Flash and Qwen/Qwen3.8-27B-FP8
- 3 independent generations per model and task
- Human-written reference contracts
- At least 5 behaviorally distinct mutants per task
- Contract strength measured by mutation score

## Current Status

The CrossHair toolchain has been tested on a toy contract and HumanEval/0.
The toy contracts, the exact commands, and the verbatim verifier output are in
[`fm/`](fm/README.md) (CrossHair 0.0.110, Z3 5.1.0, Python 3.13.5).
The full benchmark and experiment pipeline are under development.

## Reproducibility

Prompts, model settings, contracts, mutants, verifier outputs, runtimes,
and counterexamples will be archived in this repository.

Setup, dependencies, run commands, and archived verifier outputs for the toy
runs are documented in [`fm/README.md`](fm/README.md). Instructions for the full
experiment pipeline will be added as it is implemented.
