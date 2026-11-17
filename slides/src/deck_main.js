
// ================================================================ new team slides

function s_title() {
  const s = pres.addSlide();
  s.background = { color: INK };
  page += 1;
  s.addText("Verifying AI-Generated Code", { x: M, y: 0.75, w: 6.1, h: 1.35, fontFace: FONT, fontSize: 36,
    bold: true, color: "FFFFFF", valign: "bottom", margin: 0, isTextBox: true });
  s.addText("Group E  ·  Topic 7  ·  Milestone 1", { x: M, y: 2.25, w: 6.2, h: 0.4, fontFace: FONT,
    fontSize: 16, color: "6FD1C3", margin: 0, isTextBox: true });
  s.addText("Jiahao Zhang, Bingsong Liu, Zoey Tang, Keyu Huang", { x: M, y: 2.95, w: 6.2, h: 0.4,
    fontFace: FONT, fontSize: 16, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText("CS 3892 / 5892  ·  November 17, 2026", { x: M, y: 3.35, w: 6.2, h: 0.35, fontFace: FONT,
    fontSize: 13, color: "B8C2CC", margin: 0, isTextBox: true });
  s.addText("github.com/huank14/cs3892-ai-code-verification", { x: M, y: 4.6, w: 6.2, h: 0.3,
    fontFace: FONT, fontSize: 11, color: "B8C2CC", margin: 0, isTextBox: true,
    hyperlink: { url: "https://github.com/huank14/cs3892-ai-code-verification" } });
  // quiet motif: a contract, the object the project is about
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.85, y: 1.3, w: 2.65, h: 2.4, rectRadius: 0.1,
    fill: { color: "2A3743" }, line: { type: "none" } });
  s.addText([
    { text: '"""', options: { color: "7D8B97", breakLine: true } },
    { text: "pre:  ...", options: { color: "6FD1C3", breakLine: true } },
    { text: "post: ...", options: { color: "6FD1C3", breakLine: true } },
    { text: '"""', options: { color: "7D8B97", breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "strong enough to", options: { color: "B8C2CC", breakLine: true } },
    { text: "reject wrong code?", options: { color: "FFFFFF", bold: true } },
  ], { x: 7.1, y: 1.45, w: 2.3, h: 2.1, fontFace: MONO, fontSize: 13, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("Title. Group E, Topic 7, Verifying AI-Generated Code. Jiahao Zhang, Bingsong Liu, Zoey Tang, Keyu Huang.");
}

function s_motivation() {
  const s = base("Can LLM-written contracts catch incorrect code?",
`Motivation, brief recap. We ask a model to write a Python implementation together with a formal contract, a precondition and postconditions in PEP 316 form. The question is whether those contracts are strong enough to reject incorrect implementations.
The example on the left is our toy run from the proposal: a contract for max that only says the result is at least a and at least b. CrossHair confirms it over all paths, even though the code returns a plus b. Verification "passes" on wrong code, so passing tells us nothing about the contract.
Our overview, right: the model writes code and contract; CrossHair checks each contract against the reference solution, deliberately wrong mutants, and the generated code; we measure how many wrong mutants each contract rejects, compared with a human reference contract.`);

  s.addText("A weak contract accepts wrong code", { x: M, y: 1.12, w: 4.5, h: 0.3, fontFace: FONT,
    fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.5, w: 4.5, h: 1.6, rectRadius: 0.06,
    fill: { color: CODEBG }, line: { type: "none" } });
  s.addText([
    { text: "def max_weak(a: int, b: int) -> int:", options: { color: INK, breakLine: true } },
    { text: '    """', options: { color: INK, breakLine: true } },
    { text: "    post: __return__ >= a", options: { color: INK, breakLine: true } },
    { text: "    post: __return__ >= b", options: { color: INK, breakLine: true } },
    { text: '    """', options: { color: INK, breakLine: true } },
    { text: "    return a + b", options: { color: BRICK, bold: true } },
    { text: "      # wrong on purpose", options: { color: MUTED } },
  ], { x: M + 0.15, y: 1.6, w: 4.2, h: 1.45, fontFace: MONO, fontSize: 10.5, valign: "top", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 3.25, w: 4.5, h: 0.5, rectRadius: 0.06,
    fill: { color: TERM }, line: { type: "none" } });
  s.addText("CrossHair: Confirmed over all paths.  (0.6 s)", { x: M + 0.15, y: 3.25, w: 4.2, h: 0.5,
    fontFace: MONO, fontSize: 10.5, color: "7EE0B5", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Passing verification says nothing about the contract's strength.", { x: M, y: 3.9, w: 4.5,
    h: 0.5, fontFace: FONT, fontSize: 12, color: INK, italic: true, margin: 0, valign: "top", isTextBox: true });

  const rx = 5.4, rw = W - M - rx;
  s.addText("Overview", { x: rx, y: 1.12, w: rw, h: 0.3, fontFace: FONT, fontSize: 13, bold: true,
    color: INK, margin: 0, isTextBox: true });
  const steps = [
    ["AI writes (Jiahao)", "Qwen writes an implementation and a PEP 316 contract per HumanEval task."],
    ["FM checks (Bingsong)", "CrossHair checks each contract against the reference, mutants, and generated code."],
    ["We score (Zoey)", "How many wrong mutants each contract rejects."],
    ["Human baseline (Keyu)", "The same scoring for human-written reference contracts."],
  ];
  steps.forEach(([h, b], i) => {
    const y = 1.5 + i * 0.84;
    s.addShape(pres.shapes.OVAL, { x: rx, y, w: 0.42, h: 0.42, fill: { color: TEAL }, line: { type: "none" } });
    s.addText(String(i + 1), { x: rx, y, w: 0.42, h: 0.42, fontFace: FONT, fontSize: 14, bold: true,
      color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([{ text: h, options: { bold: true, color: INK, fontSize: 13, breakLine: true } },
               { text: b, options: { color: INK, fontSize: 11 } }],
      { x: rx + 0.6, y: y - 0.04, w: rw - 0.6, h: 0.78, fontFace: FONT, valign: "top", margin: 0, isTextBox: true });
  });
}

function s_changes() {
  const s = base("Changes since the proposal",
`Changes since the proposal. AI side: instead of the full 30-task, two-model run we first ran a development pilot, 6 HumanEval tasks, 3 fresh responses each, under two prompts: 36 responses. The model is Qwen3.8-27B-FP8 with thinking off; no DeepSeek requests have been made yet. The second prompt, V2, asks for each contract condition on one line, written after we saw V1's format errors.
FM side: four changes, each prompted by the first runs. Bounded verification: with unbounded lists CrossHair almost never finishes, so each task gets one size bound, inserted as the first precondition. Declared types: we analyse with the contract's signature, because the HumanEval/40 reference is annotated only as list. Discriminating kills: a mutant only counts as caught if the reference satisfies the contract at the same input. And a concrete check on the official test inputs, which we report as tested, not verified.`);

  const cols = [
    ["AI component", [
      ["Pilot first", "6 HumanEval tasks × 3 responses × 2 prompts = 36 (plan: 30 tasks × 2 models × 3)"],
      ["Model", "Qwen3.8-27B-FP8, thinking off; no DeepSeek requests yet"],
      ["Second prompt (V2)", "one contract condition per line, added after V1 format errors"],
    ]],
    ["FM component", [
      ["Bounded verification", "one size bound B_T per task, inserted as the first pre:"],
      ["Declared types", "analysis uses the contract's signature, not the reference's"],
      ["Discriminating kills", "a mutant counts only if the reference satisfies c at the same x"],
      ["Concrete check", "official test inputs too; reported as tested, not verified"],
    ]],
  ];
  const cw = (W - 2 * M - 0.3) / 2;
  cols.forEach(([h, items], ci) => {
    const x = M + ci * (cw + 0.3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.12, w: cw, h: 3.85, rectRadius: 0.08,
      fill: { color: TINT }, line: { type: "none" } });
    s.addText(h, { x: x + 0.25, y: 1.25, w: cw - 0.5, h: 0.35, fontFace: FONT, fontSize: 15, bold: true,
      color: INK, margin: 0, isTextBox: true });
    items.forEach(([a, b], i) => {
      s.addText([{ text: a, options: { bold: true, color: TEAL, breakLine: true } },
                 { text: b, options: { color: INK } }],
        { x: x + 0.25, y: 1.75 + i * 0.8, w: cw - 0.5, h: 0.74, fontFace: FONT, fontSize: 11.5,
          valign: "top", margin: 0, isTextBox: true });
    });
  });
}

function s_fm_approach() {
  const s = base("FM component: how one pair is verified",
`FM component, the verification pipeline. For every contract and every implementation of a task, the contract's docstring is copied verbatim into the implementation; nothing in the contract is edited.
CrossHair then checks the Hoare triple on the left: for every input that satisfies the precondition, the returned value satisfies every postcondition. It runs twice: first with one size bound per task, which lets it explore every path and prove postconditions within the bound; then without the bound, only searching for counterexamples.
A counterexample is an input where the precondition holds and a postcondition is false. We re-run every one in a fresh process, together with the reference on the same input.
That gives one of four verdicts, on the right. "Inconclusive" means the budget ran out with neither a counterexample nor a proof; we never count it as evidence of correctness.`);

  // flow strip
  const flow = ["Contract × implementation", "Compose: docstring copied verbatim", "CrossHair: bounded proof, then unbounded search",
                "Re-execute x, and the reference at x", "Verdict"];
  const fw = [1.6, 1.75, 2.05, 1.85, 0.95], fy = 1.1, fh = 0.62, ag = 0.2;
  let x = M;
  flow.forEach((t, i) => {
    const first = i === 0, last = i === flow.length - 1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: fy, w: fw[i], h: fh, rectRadius: 0.06,
      fill: { color: last ? INK : (first ? "FFFFFF" : TINT) }, line: first ? { color: LINE, width: 1 } : { type: "none" } });
    s.addText(t, { x: x + 0.08, y: fy, w: fw[i] - 0.16, h: fh, fontFace: FONT, fontSize: 10, bold: last || first,
      color: last ? "FFFFFF" : INK, align: last ? "center" : "left", valign: "middle", margin: 0, isTextBox: true });
    if (!last) arrow(s, x + fw[i] + 0.02, fy + fh / 2, x + fw[i] + ag - 0.02);
    x += fw[i] + ag;
  });

  // formulas
  const rows = [
    ["Contract", "c = (pre_c, post_c),   post_c = φ₁ ∧ … ∧ φ_k"],
    ["Correctness (Hoare triple)", "∀x. pre_c(x) ⇒ post_c(x, f(x))"],
    ["Bounded check", "∀x. B_T(x) ∧ pre_c(x) ⇒ post_c(x, f(x)),   B₈: len(numbers) ≤ 4"],
    ["Counterexample", "x with pre_c(x) ∧ ¬φ_i(x, f(x)), confirmed by re-execution"],
  ];
  rows.forEach(([l, f], i) => {
    const y = 2.0 + i * 0.66;
    s.addText(l, { x: M, y, w: 5.3, h: 0.22, fontFace: FONT, fontSize: 10.5, bold: true, color: TEAL, margin: 0, isTextBox: true });
    s.addText(f, { x: M, y: y + 0.22, w: 5.3, h: 0.34, fontFace: MATH, fontSize: 13, color: INK, margin: 0,
      valign: "middle", isTextBox: true });
  });

  // verdicts 2x2
  const rx = 6.05, rw = W - M - rx;
  s.addText("Verdict per pair", { x: rx, y: 2.0, w: rw, h: 0.26, fontFace: FONT, fontSize: 12, bold: true,
    color: INK, margin: 0, isTextBox: true });
  const v = [
    ["Rejected", BRICK, "counterexample re-executes; reference passes at x"],
    ["Non-discriminating", AMBER, "reference also violates c at x"],
    ["Proven (bounded)", TEAL, "every φ_i confirmed on all paths within B_T"],
    ["Inconclusive", MUTED, "budget ended with neither; not evidence"],
  ];
  v.forEach(([h, col, b], i) => {
    const y = 2.34 + i * 0.6;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y, w: rw, h: 0.52, rectRadius: 0.05,
      fill: { color: CODEBG }, line: { type: "none" } });
    s.addShape(pres.shapes.OVAL, { x: rx + 0.12, y: y + 0.11, w: 0.12, h: 0.12, fill: { color: col }, line: { type: "none" } });
    s.addText([{ text: h, options: { bold: true, color: col, breakLine: true } },
               { text: b, options: { color: INK, fontSize: 9.5 } }],
      { x: rx + 0.32, y: y + 0.04, w: rw - 0.4, h: 0.46, fontFace: FONT, fontSize: 11, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("Code: github.com/huank14/cs3892-ai-code-verification   (fm/pipeline/)", { x: M, y: 4.85, w: 7,
    h: 0.24, fontFace: FONT, fontSize: 10, color: TEAL, margin: 0, isTextBox: true,
    hyperlink: { url: "https://github.com/huank14/cs3892-ai-code-verification/tree/main/fm/pipeline" } });
}

function s_results_ai() {
  const s = base("AI component: readable contracts 6/18 → 13/18",
`AI component. I built a generation runner with versioned prompts, archived every response, and ran a development pilot. After removing code fences without changing the Python or contract text, 6 of 18 original contracts were readable, compared with 13 of 18 under the revised prompt. Implementation test passes were 18 and 17. One revised output placed contract text in the function body and became invalid Python. Among readable contracts, finite probes found semantic failures in 3 original and 2 revised outputs. These denominators differ and this is a small development pilot, so we do not claim a general improvement in semantic correctness. Passing tests is also not a proof.
Right: a readable contract can still be wrong. For the parentheses task the contract checks the type, the number of groups and non-negativity, but never the actual depth, so a result of [0] for '(())' satisfies every condition.`);

  const hdr = ["Check", "V1", "V2"].map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: INK } } }));
  const rows = [["Implementation passes official tests", "18/18", "17/18"],
                ["Readable explicit contracts", "6/18", "13/18"],
                ["Readable contracts with observed semantic failures", "3/6", "2/13"]]
    .map(r => r.map((t, j) => ({ text: t, options: { color: INK, align: j ? "center" : "left", bold: j > 0 && r[0].startsWith("Readable explicit") } })));
  s.addTable([hdr, ...rows], { x: M, y: 1.12, w: 5.3, colW: [3.5, 0.9, 0.9], fontFace: FONT, fontSize: 11.5,
    rowH: [0.38, 0.5, 0.5, 0.5], border: { type: "solid", pt: 0.75, color: LINE }, margin: [0.03, 0.1, 0.03, 0.1], valign: "middle" });
  s.addText([{ text: "Parser compatibility", options: { bold: true, color: TEAL } },
             { text: " = readable contracts / 18 attempted responses", options: { color: INK } }],
    { x: M, y: 3.2, w: 5.3, h: 0.3, fontFace: FONT, fontSize: 11.5, margin: 0, isTextBox: true });
  s.addText("Qwen3.8-27B-FP8, thinking off; 6 tasks × 3 responses per prompt. Descriptive pilot: denominators differ (3/6 vs 2/13), so no general prompt ranking.",
    { x: M, y: 3.6, w: 5.3, h: 0.6, fontFace: FONT, fontSize: 10.5, color: MUTED, margin: 0, valign: "top", isTextBox: true });

  const rx = 6.1, rw = W - M - rx;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y: 1.12, w: rw, h: 3.2, rectRadius: 0.08,
    fill: { color: TINT }, line: { type: "none" } });
  s.addText("A readable contract can accept a wrong result", { x: rx + 0.2, y: 1.25, w: rw - 0.4, h: 0.5,
    fontFace: FONT, fontSize: 12, bold: true, color: INK, margin: 0, valign: "top", isTextBox: true });
  s.addText("v2 / HumanEval_6_1", { x: rx + 0.2, y: 1.78, w: rw - 0.4, h: 0.25, fontFace: MONO, fontSize: 10,
    bold: true, color: MUTED, margin: 0, isTextBox: true });
  s.addText([
    { text: "post: isinstance(__return__, list)", options: { breakLine: true } },
    { text: "post: all(isinstance(x, int)", options: { breakLine: true } },
    { text: "        for x in __return__)", options: { breakLine: true } },
    { text: "post: len(__return__) ==", options: { breakLine: true } },
    { text: "        len(paren_string.split(' '))", options: { breakLine: true } },
    { text: "post: all(x >= 0 for x in __return__)" },
  ], { x: rx + 0.2, y: 2.08, w: rw - 0.3, h: 1.4, fontFace: MONO, fontSize: 8.5, color: INK, valign: "top", margin: 0, isTextBox: true });
  s.addText([{ text: "'(())'", options: { fontFace: MONO, bold: true } }, { text: ": expected [2]; " },
             { text: "[0]", options: { fontFace: MONO, bold: true, color: BRICK } },
             { text: " satisfies every condition. Depth is never constrained." }],
    { x: rx + 0.2, y: 3.6, w: rw - 0.4, h: 0.85, fontFace: FONT, fontSize: 11, color: INK, valign: "top", margin: 0, isTextBox: true });
}

function s_questions() {
  const s = base("Questions and issues",
`Open questions. First, the input domain. Zoey fixed one legal input domain per task from the task text before scoring: the empty string is legal for HumanEval/6, infinity and NaN are not legal for HumanEval/0. So v2_6_1 is over-restrictive, while the NaN counterexample on HumanEval/0 is outside the domain and does not count against the contract. Is fixing the domain per task, from the task text, an acceptable way to judge over-restrictive contracts?
Second, bounded proofs only hold up to the size bound; we report them separately from unbounded results and want to know whether that is acceptable evidence.
Third, two tool limits keep six checks inconclusive; we report them instead of rewriting contracts so CrossHair can handle them.
Fourth, human reference contracts may use LLM help with human review and disclosure; is that independent enough for a human baseline?`);

  const q = [
    ["Input domain (fixed by Zoey)", "Empty string legal for /6; inf and NaN not legal for /0. One domain per task from the task text: acceptable?"],
    ["Bounded proofs", "Confirmations hold only up to B_T (e.g. len ≤ 4). Reported separately from unbounded results: acceptable evidence?"],
    ["Tool limits", "Float lists and nonlinear products stay inconclusive at 60 s. We report them, not rewrite contracts."],
    ["LLM help for human contracts", "Allowed with human review and disclosure. Independent enough for a human baseline?"],
  ];
  const cw = (W - 2 * M - 0.3) / 2, chh = 1.32;
  q.forEach(([h, b], i) => {
    const x = M + (i % 2) * (cw + 0.3), y = 1.12 + Math.floor(i / 2) * (chh + 0.2);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: chh, rectRadius: 0.08, fill: { color: TINT }, line: { type: "none" } });
    s.addShape(pres.shapes.OVAL, { x: x + 0.18, y: y + 0.17, w: 0.36, h: 0.36, fill: { color: TEAL }, line: { type: "none" } });
    s.addText(String(i + 1), { x: x + 0.18, y: y + 0.17, w: 0.36, h: 0.36, fontFace: FONT, fontSize: 12, bold: true,
      color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([{ text: h, options: { bold: true, color: INK, fontSize: 12.5, breakLine: true } },
               { text: b, options: { color: INK, fontSize: 11 } }],
      { x: x + 0.68, y: y + 0.14, w: cw - 0.85, h: chh - 0.24, fontFace: FONT, valign: "top", margin: 0, isTextBox: true });
  });
  pending(s, M, 4.05, W - 2 * M, 0.6, "Keyu, Zoey", "questions that come up while writing human contracts and mutants for the 30 tasks.");
}

// ================================================================ order (one presenter per slide, contiguous)
PRESENTER = "Jiahao";    s_title();
PRESENTER = "Jiahao";    s_motivation();
PRESENTER = "Jiahao";    s_changes();
PRESENTER = "Jiahao";    s_results_ai();
PRESENTER = "Bingsong";  s_fm_approach();
PRESENTER = "Bingsong";  s_demo();
PRESENTER = "Zoey";      old_results();
PRESENTER = "Zoey";      s_quality();
PRESENTER = "Keyu";      s_keyu();
PRESENTER = "Keyu";      s_questions();
PRESENTER = "";          old_defects();
PRESENTER = "";          old_backup();

pres.writeFile({ fileName: process.argv[2] || "deck.pptx" }).then(f => console.log("wrote", f));
