function old_approach() {

  const s = base("The pipeline: compose, check, re-execute",
`Approach, FM side. The pipeline takes every contract for a task, Qwen's or the human reference contract, and every implementation, the HumanEval reference, the validated mutants, and Qwen's own implementations, and checks each pair.
Step 1: the contract's docstring is copied verbatim into the implementation; nothing in the contract is edited.
Step 2: CrossHair runs twice. First with one size bound per task, which lets it explore every path and prove postconditions; then without the bound, searching only for counterexamples, so small bounds cannot hide errors on longer inputs.
Step 3: every counterexample is re-run in a fresh Python process, and the reference is run on the same input. That second check decides whether the counterexample discriminates.
Changes since the proposal are on the lower half; each came from something the first runs showed. The code is in fm/pipeline in the team repository.`);

  // inputs
  const inY = 1.2, boxH = 0.78;
  const inputs = [
    ["Contract", "Qwen (19 parsed) or human reference"],
    ["Implementation", "reference, mutants, Qwen"],
  ];
  inputs.forEach(([h, b], i) => {
    const y = inY + i * (boxH + 0.12);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y, w: 1.8, h: boxH, rectRadius: 0.08,
      fill: { color: "FFFFFF" }, line: { color: LINE, width: 1 } });
    s.addText([{ text: h, options: { bold: true, color: INK, fontSize: 12, breakLine: true } },
               { text: b, options: { color: MUTED, fontSize: 10 } }],
      { x: M + 0.1, y, w: 1.6, h: boxH, fontFace: FONT, valign: "middle", margin: 0, isTextBox: true });
  });
  const flowTop = inY, flowH = 2 * boxH + 0.12, midY = flowTop + flowH / 2;

  const steps = [
    ["Compose", "Contract docstring copied verbatim into the implementation"],
    ["CrossHair", "Bounded proof within B_T, then an unbounded search for counterexamples"],
    ["Re-execute", "Run f(x) in a fresh process; run the reference at the same x"],
  ];
  const sx0 = 2.65, sw = 1.6, gap = 0.35;
  arrow(s, M + 1.8 + 0.05, midY, sx0 - 0.05);
  steps.forEach(([h, b], i) => {
    const x = sx0 + i * (sw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: flowTop, w: sw, h: flowH, rectRadius: 0.08,
      fill: { color: TINT }, line: { type: "none" } });
    s.addShape(pres.shapes.OVAL, { x: x + 0.14, y: flowTop + 0.16, w: 0.34, h: 0.34,
      fill: { color: TEAL }, line: { type: "none" } });
    s.addText(String(i + 1), { x: x + 0.14, y: flowTop + 0.16, w: 0.34, h: 0.34, fontFace: FONT,
      fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(h, { x: x + 0.56, y: flowTop + 0.16, w: sw - 0.6, h: 0.34, fontFace: FONT, fontSize: 12,
      bold: true, color: INK, valign: "middle", margin: 0, isTextBox: true });
    s.addText(b, { x: x + 0.14, y: flowTop + 0.62, w: sw - 0.26, h: flowH - 0.72, fontFace: FONT,
      fontSize: 11, color: INK, valign: "top", margin: 0, isTextBox: true });
    const nx = x + sw;
    if (i < steps.length - 1) arrow(s, nx + 0.05, midY, nx + gap - 0.05);
  });
  // verdict pill
  const vx = sx0 + 3 * (sw + gap);
  arrow(s, vx - gap + 0.05, midY, vx - 0.05);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: vx, y: midY - 0.36, w: W - M - vx, h: 0.72,
    rectRadius: 0.08, fill: { color: INK }, line: { type: "none" } });
  s.addText("Verdict", { x: vx, y: midY - 0.36, w: W - M - vx, h: 0.72, fontFace: FONT, fontSize: 12,
    bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });

  // changes since proposal
  s.addText("Changes since the proposal", { x: M, y: 3.12, w: 6, h: 0.32, fontFace: FONT, fontSize: 14,
    bold: true, color: INK, margin: 0, isTextBox: true });
  const ch = [
    ["Bounded verification", "one size bound B_T per task, inserted as the first pre:"],
    ["Declared types", "analysis uses the contract's signature, not the reference's"],
    ["Discriminating kills", "a mutant counts only if the reference satisfies c at the same x"],
    ["Concrete check", "official test inputs as well; reported as tested, not verified"],
  ];
  ch.forEach(([h, b], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 4.6, y = 3.52 + row * 0.64;
    s.addText([{ text: h, options: { bold: true, color: TEAL, breakLine: true } },
               { text: b, options: { color: INK } }],
      { x, y, w: 4.4, h: 0.6, fontFace: FONT, fontSize: 11.5, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("Code: github.com/huank14/cs3892-ai-code-verification  (fm/pipeline)", { x: M, y: 4.95, w: 6,
    h: 0.22, fontFace: FONT, fontSize: 9, color: TEAL, margin: 0, isTextBox: true,
    hyperlink: { url: "https://github.com/huank14/cs3892-ai-code-verification/tree/main/fm/pipeline" } });
}

function old_definitions() {

  const s = base("Definitions: contract, verdict, mutation score",
`Definitions. A contract is a precondition and a conjunction of postconditions, written in PEP 316 docstrings. What CrossHair checks is the Hoare triple: for every input satisfying the precondition, the returned value satisfies every postcondition.
Bounded check: we add one size bound per task, the same for every contract of that task, for example len(numbers) at most 4 on HumanEval/8. A confirmation then holds only for inputs within the bound; we always say so.
A counterexample is an input where the precondition holds and some postcondition is false. We only count it after re-running it.
A mutant is killed only if the contract rejects the mutant at x and the reference satisfies the contract at the same x. Otherwise an over-strict contract would get credit for rejecting everything.
Mutation score is the fraction of validated mutants killed. Determinacy is the share of checks that end in a rejection or a proof rather than "not confirmed"; the proposal set 80% as the criterion.`);

  const rows = [
    ["Contract", "c = (pre_c, post_c),   post_c = φ₁ ∧ … ∧ φ_k"],
    ["Correctness (Hoare triple)", "{pre_c} f {post_c}  ⇔  ∀x. pre_c(x) ⇒ post_c(x, f(x))"],
    ["Bounded check", "∀x. B_T(x) ∧ pre_c(x) ⇒ post_c(x, f(x)),   e.g. B₈: len(numbers) ≤ 4"],
    ["Counterexample", "x with pre_c(x) ∧ ¬φ_i(x, f(x)),  confirmed by re-execution"],
    ["Kill", "killed(c, m) ⇔ ∃x. pre_c(x) ∧ ¬post_c(x, m(x)) ∧ post_c(x, f*(x))"],
    ["Mutation score", "MS(c) = |{m ∈ M : killed(c, m)}| / |M|"],
    ["Determinacy", "(#rejected + #proven) / #checks"],
  ];
  const y0 = 1.12, rh = 0.53;
  rows.forEach(([l, f], i) => {
    const y = y0 + i * rh;
    s.addText(l, { x: M, y, w: 5.9, h: 0.2, fontFace: FONT, fontSize: 10, bold: true, color: TEAL,
      margin: 0, isTextBox: true });
    s.addText(f, { x: M, y: y + 0.2, w: 5.9, h: 0.3, fontFace: MATH, fontSize: 13, color: INK,
      margin: 0, valign: "middle", isTextBox: true });
  });
  s.addText("f* = HumanEval reference;  M = validated mutants of task T", { x: M, y: y0 + 7 * rh + 0.02,
    w: 5.9, h: 0.22, fontFace: FONT, fontSize: 10, italic: true, color: MUTED, margin: 0, isTextBox: true });

  const rx = 6.7, rw = W - M - rx;
  s.addText("Verdict per pair (c, g)", { x: rx, y: 1.12, w: rw, h: 0.3, fontFace: FONT, fontSize: 13,
    bold: true, color: INK, margin: 0, isTextBox: true });
  const v = [
    ["Rejected", BRICK, "counterexample re-executes; f* satisfies c at x"],
    ["Non-discriminating", AMBER, "f* also violates c at x: no credit"],
    ["Proven (bounded)", TEAL, "every φ_i confirmed on all paths within B_T; none found beyond"],
    ["Inconclusive", MUTED, "budget ended with neither; not evidence of correctness"],
  ];
  v.forEach(([h, col, b], i) => {
    const y = 1.55 + i * 0.86;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y, w: rw, h: 0.76, rectRadius: 0.06,
      fill: { color: CODEBG }, line: { type: "none" } });
    s.addShape(pres.shapes.OVAL, { x: rx + 0.12, y: y + 0.15, w: 0.14, h: 0.14,
      fill: { color: col }, line: { type: "none" } });
    s.addText([{ text: h, options: { bold: true, color: col, breakLine: true } },
               { text: b, options: { color: INK, fontSize: 10 } }],
      { x: rx + 0.34, y: y + 0.07, w: rw - 0.44, h: 0.64, fontFace: FONT, fontSize: 11.5,
        valign: "top", margin: 0, isTextBox: true });
  });
}

function old_demo() {

  const s = base("Demo: CrossHair rejects a correct answer",
`Demo. This is one command; it runs in under two seconds, so it can be shown live, with a recording as backup.
Left: the Qwen contract for sum_product, copied verbatim. The first precondition is our task bound.
Right: CrossHair's output. Seven postconditions are confirmed over all paths within the bound. The sixth one gets a counterexample: sum_product of [0] returns (0, 0), which is correct, and the contract rejects it. The pipeline re-runs this input in a fresh process and reproduces the violation.
Why: Python parses that line as "something if the list is empty, else __return__[1]". For a non-empty list the condition is just the product itself, which is false when the product is 0. So the defect is in the contract, not the implementation, and CrossHair found it without us writing a single test.`);

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.08, w: W - 2 * M, h: 0.38, rectRadius: 0.05,
    fill: { color: CODEBG }, line: { type: "none" } });
  s.addText("$ python -m pipeline.demo --task HumanEval/8 --contract qwen_v1_8_3 --impl reference --bounded",
    { x: M + 0.15, y: 1.08, w: W - 2 * M - 0.3, h: 0.38, fontFace: MONO, fontSize: 10.5, color: INK,
      valign: "middle", margin: 0, isTextBox: true });

  const cy = 1.62, ch = 2.62;
  s.addText("Qwen contract v1/HumanEval_8_3 (excerpt)", { x: M, y: cy, w: 4.45, h: 0.25,
    fontFace: FONT, fontSize: 11, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: cy + 0.3, w: 4.45, h: ch - 0.3, rectRadius: 0.06,
    fill: { color: CODEBG }, line: { type: "none" } });
  const code = [
    ["pre: len(numbers) <= 4", TEAL, "   # B_8, added"],
    ["pre:", INK], ["    all(isinstance(x, int) for x in numbers)", INK],
    ["post:", INK], ["    __return__[0] == sum(numbers)", INK],
    ["    __return__[1] == (lambda acc: acc)(1)", BRICK], ["      * __return__[1] if len(numbers) == 0", BRICK],
    ["      else __return__[1]", BRICK],
    ["    (__return__[1] == 1 if len(numbers) == 0", INK], ["      else True)", INK],
  ];
  const runs = [];
  code.forEach(([t, c, cm], i) => {
    runs.push({ text: t, options: { color: c, bold: c === BRICK, breakLine: !cm && i < code.length - 1 } });
    if (cm) runs.push({ text: cm, options: { color: MUTED, breakLine: true } });
  });
  s.addText(runs, { x: M + 0.15, y: cy + 0.38, w: 4.2, h: ch - 0.45, fontFace: MONO, fontSize: 9.5,
    valign: "top", margin: 0, isTextBox: true });

  const tx = 5.15, tw = W - M - tx;
  s.addText("CrossHair output (condensed) and re-execution", { x: tx, y: cy, w: tw, h: 0.25, fontFace: FONT,
    fontSize: 11, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: tx, y: cy + 0.3, w: tw, h: ch - 0.3, rectRadius: 0.06,
    fill: { color: TERM }, line: { type: "none" } });
  const ok = "C9D1D9", good = "7EE0B5", bad = "FF9B8F", dim = "8B949E";
  const term = [
    ["line 26-30: info: Confirmed over all paths.", ok],
    ["line 31: error: false when calling", bad],
    ["  sum_product([0]) (which returns (0, 0))", bad],
    ["line 32-33: info: Confirmed over all paths.", ok],
    ["(1.6s)", dim],
    ["", ok],
    ["re-executed in a fresh process:", dim],
    ["  input : sum_product([0])", ok],
    ["  output: (0, 0)", ok],
    ["  line 31 post: FALSE    other 7: true", bad],
  ];
  s.addText(term.map(([t, c], i) => ({ text: t || " ", options: { color: c, breakLine: i < term.length - 1 } })),
    { x: tx + 0.15, y: cy + 0.38, w: tw - 0.3, h: ch - 0.45, fontFace: MONO, fontSize: 9.5, valign: "top",
      margin: 0, isTextBox: true });

  s.addText([
    { text: "Why: ", options: { bold: true } },
    { text: "Python reads the red line as (…) if len(numbers) == 0 else __return__[1]. For a non-empty list it only asks that the product be non-zero, so the correct (0, 0) for [0] is rejected. The defect is in the contract." },
  ], { x: M, y: 4.33, w: 5.35, h: 0.78, fontFace: FONT, fontSize: 11, color: INK, valign: "top",
    margin: 0, isTextBox: true });
  pending(s, 6.05, 4.33, W - M - 6.05, 0.75, "needs Keyu + Zoey", "demo 2: a human contract kills a mutant that the Qwen contract misses.", 10);
}

function old_results() {

  const s = base("Bounding input size: 11% → 84% determinate",
`Preliminary results, first: how often the verifier reaches a verdict at all. These are the 19 Qwen contracts that parse, each checked against the HumanEval reference and against the implementation Qwen wrote in the same response: 38 checks, 60 seconds per postcondition, the budget from the proposal.
Unbounded, as in the proposal, only 4 of 38 checks reach a verdict: CrossHair never finishes exploring unbounded lists and strings. With one size bound per task, 32 of 38 are determinate, 84 percent, above our 80 percent criterion.
28 of those are proofs within the bound, so they mean "correct for all inputs up to the bound", not "correct". The six that stay inconclusive are two known tool limits: float lists on HumanEval/0 and products via math.prod on HumanEval/8. We report them rather than editing the contracts.
On the right, three Qwen contracts reject a correct output, each with a re-executed counterexample: an operator-precedence bug on HumanEval/8, the empty string on HumanEval/6, and object identity on HumanEval/0, which the concrete check on official tests caught, so tested, not verified. They match what Jiahao's probes flagged.`);

  const chartData = [
    { name: "Unbounded (proposal setup)", labels: ["All 38 checks", "Contract × reference", "Contract × Qwen impl"], values: [11, 11, 11] },
    { name: "Combined (bounded + unbounded)", labels: ["All 38 checks", "Contract × reference", "Contract × Qwen impl"], values: [84, 79, 89] },
  ];
  s.addChart(pres.charts.BAR, chartData, {
    x: M, y: 1.08, w: 5.5, h: 3.75, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60,
    chartColors: [GRAYBAR, TEAL],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"', dataLabelFontSize: 11,
    dataLabelColor: INK, dataLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 20, valAxisLabelFormatCode: '0"%"',
    valAxisLabelFontSize: 10, catAxisLabelFontSize: 10.5, valAxisLabelColor: MUTED, catAxisLabelColor: INK,
    valAxisLabelFontFace: FONT, catAxisLabelFontFace: FONT,
    valGridLine: { color: "E3E7EA", size: 0.75 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 10, legendFontFace: FONT, legendColor: INK,
    showTitle: true, title: "Determinate verdicts (rejected or proven)", titleFontSize: 12,
    titleColor: INK, titleFontFace: FONT,
  });

  const rx = 6.35, rw = W - M - rx;
  s.addText("32 / 38", { x: rx, y: 1.08, w: rw, h: 0.62, fontFace: FONT, fontSize: 36, bold: true,
    color: TEAL, margin: 0, isTextBox: true });
  s.addText("checks end in a rejection or a proof (determinacy); proposal criterion ≥ 80%", { x: rx, y: 1.7, w: rw, h: 0.5,
    fontFace: FONT, fontSize: 10.5, color: MUTED, margin: 0, isTextBox: true });

  s.addText("Wrong contracts found (re-executed)", { x: rx, y: 2.3, w: rw, h: 0.28, fontFace: FONT, fontSize: 12,
    bold: true, color: INK, margin: 0, isTextBox: true });
  [["v1_8_3", "rejects correct (0, 0) for [0]"], ["v2_6_1", "rejects the reference on empty string"],
   ["v2_0_3", "rejects correct True (official test)"]].forEach(([c, t], k) => {
    s.addText([{ text: c, options: { fontFace: MONO, bold: true, color: BRICK, breakLine: true } },
               { text: t, options: { color: INK } }],
      { x: rx, y: 2.65 + k * 0.5, w: rw, h: 0.46, fontFace: FONT, fontSize: 10.5, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("All 6 inconclusive checks are tool limits: float lists (HumanEval/0) and nonlinear math.prod (HumanEval/8).",
    { x: rx, y: 4.15, w: rw, h: 0.6, fontFace: FONT, fontSize: 10.5, color: INK, margin: 0, valign: "top",
      isTextBox: true });
  s.addText("19 parsed Qwen contracts × {reference, own implementation}; 60 s per postcondition; CrossHair 0.0.110, Z3 5.1.0; commit 0032441",
    { x: M, y: 4.88, w: W - 2 * M, h: 0.25, fontFace: FONT, fontSize: 9, italic: true, color: MUTED,
      margin: 0, isTextBox: true });
}

function old_defects() {

  const s = base("Backup: the three wrong Qwen contracts",
`Three of the nineteen Qwen contracts reject a correct output, and in each case the counterexample re-executes.
v1 HumanEval/8: the operator-precedence bug from the demo.
v2 HumanEval/6: the contract requires as many results as space-separated groups, and on the empty string that count is one, so the reference is rejected. Whether the empty string is a legal input is an input-domain decision Keyu and Zoey are making.
v2 HumanEval/0: found by the concrete check on the official tests, so this one is tested, not verified. The contract uses "b is not a", which compares object identity; on an official test input equal floats are the same object, so the correct True is rejected.
The HumanEval/6 contract is also the one Jiahao showed accepting a wrong answer. So it is too weak and too strict at once. Our scoring handles this: a contract that rejects the reference gets no credit for rejecting mutants.`);

  const hdr = ["Contract", "Found by", "Rejected correct output", "Cause"].map(t => ({ text: t,
    options: { bold: true, color: "FFFFFF", fill: { color: INK } } }));
  const body = [
    ["v1 / HumanEval_8_3", "CrossHair", "sum_product([0]) → (0, 0)", "operator precedence in a conditional expression"],
    ["v2 / HumanEval_6_1", "CrossHair", "reference on the empty string", "len(r) == len(s.split(' ')) counts an empty group"],
    ["v2 / HumanEval_0_3", "official test (concrete)", "True on an official test input", "b is not a compares object identity"],
  ].map(r => r.map((t, j) => ({ text: t, options: { color: INK, fontFace: j === 0 ? MONO : FONT, bold: j === 0 } })));
  s.addTable([hdr, ...body], { x: M, y: 1.12, w: W - 2 * M, colW: [2.0, 1.55, 2.35, 3.1], fontFace: FONT,
    fontSize: 11, rowH: [0.38, 0.5, 0.5, 0.5], border: { type: "solid", pt: 0.75, color: LINE },
    margin: [0.03, 0.1, 0.03, 0.1], valign: "middle" });
  s.addText("Every counterexample re-executed. For v2_0_3 CrossHair also found [-inf, -inf], where inf - inf = NaN makes the reference violate the contract too (non-discriminating).",
    { x: M, y: 3.05, w: W - 2 * M, h: 0.4, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
      margin: 0, valign: "top", isTextBox: true });

  const by = 3.6, bw = (W - 2 * M - 0.3) / 2;
  const blocks = [
    ["Too weak and too strict at once", "v2 / HumanEval_6_1 also accepts the wrong [0] for '(())' (AI section). It rejects a correct output and accepts an incorrect one."],
    ["Why this matters for scoring", "Kills at inputs where the reference also fails do not count, and a contract that rejects the reference on a legal input gets MS_eff = 0."],
  ];
  blocks.forEach(([h, b], i) => {
    const x = M + i * (bw + 0.3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: by, w: bw, h: 1.3, rectRadius: 0.08,
      fill: { color: TINT }, line: { type: "none" } });
    s.addText([{ text: h, options: { bold: true, color: TEAL, fontSize: 13, breakLine: true } },
               { text: b, options: { color: INK, fontSize: 12 } }],
      { x: x + 0.2, y: by + 0.15, w: bw - 0.4, h: 1.05, fontFace: FONT, valign: "top", margin: 0,
        paraSpaceAfter: 4, isTextBox: true });
  });
}

function old_backup() {

  const s = base("Backup: verdict per Qwen contract",
`Backup table, one row per contract or group of contracts. U is the unbounded run, C the combined run. P is proven within the bound, R rejected, N non-discriminating, I inconclusive. The unbounded and combined runs found the same four rejections; bounding only turned inconclusive results into proofs.`);
  const hdr = ["Task", "Contract", "Reference  U / C", "Own Qwen impl  U / C", "Note"].map(t => ({ text: t,
    options: { bold: true, color: "FFFFFF", fill: { color: INK } } }));
  const rows = [
    ["HumanEval/0", "v2_0_2", "I / I", "I / P", "floats: reference not confirmed"],
    ["HumanEval/0", "v2_0_3", "I / I", "N / N", "over-strict (is not)"],
    ["HumanEval/6", "v2_6_1", "R / R", "I / P", "rejects reference on empty string"],
    ["HumanEval/8", "v1_8_2, v2_8_2", "I / I", "I / I", "math.prod (nonlinear)"],
    ["HumanEval/8", "v1_8_3", "R / R", "N / N", "operator precedence"],
    ["HumanEval/8", "v2_8_3", "I / P", "I / P", ""],
    ["HumanEval/12", "v2_12_2, v2_12_3", "I / P", "I / P", ""],
    ["HumanEval/28", "v1_28_1-3, v2_28_1-3", "I / P", "I / P", "all six"],
    ["HumanEval/40", "v1_40_2, v2_40_1-3", "I / P", "I / P", "all four"],
  ].map(r => r.map(t => ({ text: t, options: { color: INK } })));
  s.addTable([hdr, ...rows], { x: M, y: 1.08, w: W - 2 * M, colW: [1.3, 2.25, 1.45, 1.75, 2.25],
    fontFace: FONT, fontSize: 10.5, rowH: 0.34, border: { type: "solid", pt: 0.75, color: LINE },
    margin: [0.02, 0.08, 0.02, 0.08], valign: "middle" });
  s.addText("U = unbounded, C = combined.  P = proven within bound, R = rejected, N = non-discriminating, I = inconclusive.",
    { x: M, y: 4.62, w: W - 2 * M, h: 0.3, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
      margin: 0, isTextBox: true });
}
