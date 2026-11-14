# Jiahao — AI milestone speaker notes

Target: about 2–3 minutes. Slides 1–3 are the main section; slides 4–5 are backup.

## Slide 1

For the AI component, I built a generation pipeline and ran a small pilot with Qwen3.8-27B-FP8, with thinking disabled. We used six HumanEval tasks and generated three independent responses per task. Each response contains an implementation and a proposed PEP 316 contract. I then repeated the same tasks with a second prompt that explicitly requests one-line contract expressions. That gives us 36 responses in total. The model and deployment settings stayed the same. We retained all outputs, including failures. This combines AI4FM, generating specifications, with FM4AI, checking generated programs.

## Slide 2

The main observed difference was parser compatibility. After removing code fences without changing the Python or contract content, six of eighteen original contracts were readable, compared with thirteen of eighteen under the revised prompt. Implementation test passes were eighteen and seventeen. One revised output placed contract text in the function body and became invalid Python. Among readable contracts, our finite probes found semantic failures in three original outputs and two revised outputs. These denominators differ, and this is a small development pilot, so we cannot claim a general improvement in semantic correctness. Passing tests is also not a proof of implementation correctness.

Definitions: parser compatibility = number of readable explicit contracts divided by 18 attempted responses. Semantic-failure count records at least one concrete excluded valid input, rejected reference output, or accepted incorrect output. The probe suite was developed during pilot inspection and applied to both versions. Source: ai/analysis/prompt_comparison.json and both semantic_probes.json files.

## Slide 3

Here is a semantic problem that remained under the revised prompt. For the parentheses task, this contract checks that the result is a list of integers, has the right number of entries, and contains nonnegative values. But it never says that those values equal the maximum nesting depths. For the input double opening and double closing parentheses, the correct answer is two, yet a list containing zero satisfies every condition. We reproduced this with the actual parsed contract expressions. Next, the FM and benchmark owners can evaluate these unchanged contracts against shared, validated mutants. They can start with the saved outputs immediately.

## Chinese explanation

1. 我完成了生成和归档流程，并用相同模型设置对比两版 prompt。总共 36 份输出，全部保留。
2. 格式提示之后，可解析规格从 6/18 变成 13/18；但这是小规模开发实验，不能说已经证明语义正确率提高。
3. 新版仍有具体的错误：括号深度规格只检查形状和非负数，允许把正确的 [2] 写成 [0]。

## Likely questions

**Did the model solve every programming task?** V1 passed 18/18 finite official tests. V2 passed 17/18; one output is invalid Python because contract text escaped the docstring. Passing finite tests is not a proof.

**Did the prompt cause a semantic improvement?** We observed a parser-compatibility difference. Three samples per task, no seed matching, a development sample, and different eligible-contract denominators do not establish a general semantic or causal improvement.

**Are these mutation scores?** No. These are finite reference-output and wrong-output probes. C/B still need a shared, independently validated mutant pool for the proposal's mutation score.

**Why not DeepSeek?** Qwen already exposed specification-quality problems. We kept the milestone focused on one deployment and a controlled prompt change. DeepSeek can be added after the evaluation protocol is ready.

**Can FM begin now?** Yes. Each saved sample includes source, its unchanged contract, task ID, prompt version and settings. The final AI batch is not a prerequisite for building and exercising the verifier.

**Did you fix bad contracts by hand?** No. We removed code fences in separately labeled diagnostic copies. Contract expressions and Python content remain unchanged.
