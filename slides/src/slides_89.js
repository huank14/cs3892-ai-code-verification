function s_quality() {
  const s = base("Mutation score: human vs Qwen contracts",
`[Zoey: adapt these notes; the numbers are from the full pilot run.]
How a contract is scored. A mutant is a deliberately wrong variant of the reference; Zoey wrote six per task, each with a witness input where it is wrong. A mutant counts as killed only if CrossHair finds an input where the contract rejects it, the pipeline re-executes that input, and the reference satisfies the contract at the same input. The mutation score is the fraction of the task's mutants that are killed. A contract that rejects the reference on a legal input is over-restrictive, and its effective score MS_eff is 0.
Right: the full pilot run, 229 checks in combined mode, 60 seconds per postcondition. The human contract kills all 36 mutants. Over the 19 Qwen contracts that parse, the mean effective score is 0.76. Four Qwen contracts score 0: three reject correct outputs (the three on the previous slide), and v1_40_2 is too weak: it only says the result is a bool, so all six HumanEval/40 mutants are accepted as proven. That is the demo.
Bottom: the human contract also checks Qwen's own implementations. Two of the 35 are wrong: on HumanEval/6 they return [0] for the empty string instead of the empty list. 147 of the 150 contract-mutant checks reached a verdict (98 percent).`);

  const lx = M, lw = 4.2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: lx, y: 1.1, w: lw, h: 2.6, rectRadius: 0.08,
    fill: { color: TINT }, line: { type: "none" } });
  s.addText("How a contract is scored", { x: lx + 0.2, y: 1.18, w: lw - 0.4, h: 0.3, fontFace: FONT, fontSize: 13,
    bold: true, color: INK, margin: 0, isTextBox: true });
  const rows = [
    ["Killed mutant", "killed(c, m) ⇔ ∃x. pre_c(x) ∧ ¬post_c(x, m(x))", "                      ∧ post_c(x, f*(x))"],
    ["Mutation score", "MS(c) = |{m ∈ M : killed(c, m)}| / |M|", null],
    ["Effective score", "MS_eff(c) = 0 if c is over-restrictive, else MS(c)", null],
  ];
  let y = 1.52;
  rows.forEach(([l, f, f2]) => {
    s.addText(l, { x: lx + 0.2, y, w: lw - 0.4, h: 0.22, fontFace: FONT, fontSize: 10.5, bold: true, color: TEAL, margin: 0, isTextBox: true });
    const runs = [{ text: f, options: { breakLine: !!f2 } }];
    if (f2) runs.push({ text: f2 });
    const h = f2 ? 0.46 : 0.26;
    s.addText(runs, { x: lx + 0.2, y: y + 0.22, w: lw - 0.3, h, fontFace: MATH, fontSize: 11.5, color: INK, margin: 0, valign: "top", isTextBox: true });
    y += 0.22 + h + 0.08;
  });
  s.addText("f* = reference;  M = 6 validated mutants;  over-restrictive = rejects f* on a legal input", { x: lx + 0.2, y: 3.4, w: lw - 0.4,
    h: 0.22, fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED, margin: 0, isTextBox: true });

  const rx = 4.95, rw = W - M - rx;
  const hdr = ["Task", "Human MS_eff", "Qwen MS_eff, median (n)"].map(t => ({ text: t,
    options: { bold: true, color: "FFFFFF", fill: { color: INK } } }));
  const data = [
    ["HumanEval/0", "1.00", "0.50  (2)"], ["HumanEval/6", "1.00", "0.00  (1)"], ["HumanEval/8", "1.00", "0.75  (4)"],
    ["HumanEval/12", "1.00", "1.00  (2)"], ["HumanEval/28", "1.00", "1.00  (6)"], ["HumanEval/40", "1.00", "1.00  (4)"],
  ];
  const body = data.map(r => [{ text: r[0], options: { color: INK } },
    { text: r[1], options: { color: INK, align: "center" } },
    { text: r[2], options: { color: r[2].startsWith("1.00") ? INK : BRICK, align: "center", bold: !r[2].startsWith("1.00") } }]);
  body.push([{ text: "All (mean)", options: { bold: true, color: INK, fill: { color: TINT } } },
    { text: "1.00", options: { bold: true, color: INK, align: "center", fill: { color: TINT } } },
    { text: "0.76  (19)", options: { bold: true, color: INK, align: "center", fill: { color: TINT } } }]);
  s.addTable([hdr, ...body], { x: rx, y: 1.1, w: rw, colW: [1.35, 1.2, 2.0], fontFace: FONT, fontSize: 10.5,
    rowH: 0.32, border: { type: "solid", pt: 0.75, color: LINE }, margin: [0.02, 0.08, 0.02, 0.08], valign: "middle" });

  s.addText([
    { text: "4 of 19 Qwen contracts score 0: ", options: { bold: true } },
    { text: "3 over-restrictive (v1_8_3, v2_6_1, v2_0_3); v1_40_2 too weak: all 6 mutants proven (demo)." , options: { breakLine: true } },
    { text: "Human contract on Qwen code: ", options: { bold: true } },
    { text: "2 of 35 Qwen implementations wrong (HumanEval/6: [0] instead of [] for the empty string)." },
  ], { x: M, y: 3.82, w: W - 2 * M, h: 0.58, fontFace: FONT, fontSize: 10.5, color: INK, valign: "top",
    margin: 0, paraSpaceAfter: 3, isTextBox: true });
  pending(s, M, 4.47, W - 2 * M, 0.6, "Zoey", "which mutant categories the Qwen contracts miss and why; end-to-end median including the 17 Qwen samples that do not parse (MS = 0).", 10);
}
function s_keyu() {
  const s = base("Human reference contracts and remaining work",
`[Keyu: adapt these notes.]
Human reference contracts. These are the human baseline. Keyu decided the requirements for each task from the HumanEval statement and Zoey's frozen input domain; ChatGPT helped translate them into PEP 316 syntax and check syntax, and that help is disclosed. Every condition was then reviewed against the task text, the input domain, the reference, and edge cases such as empty input, duplicates and ties. Helpers never call the reference.
Checks before use: the contract must not reject the reference. Five of six are proven within the bound; HumanEval/0 is inconclusive because of floats. None rejects the reference, and all 36 mutants are killed.
Right: remaining work toward the final, with owners. The pipeline runs new contracts and mutants with one command, so the work left is writing them for 30 tasks and the second model.`);

  const lx = M, lw = 4.2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: lx, y: 1.1, w: lw, h: 2.75, rectRadius: 0.08,
    fill: { color: TINT }, line: { type: "none" } });
  s.addText("How reference contracts are written", { x: lx + 0.2, y: 1.2, w: lw - 0.4, h: 0.3, fontFace: FONT,
    fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true });
  const items = [
    ["Requirements by hand", "from the task text and the frozen input domain"],
    ["LLM help disclosed", "ChatGPT for syntax only; Keyu reviewed semantics"],
    ["Same format", "PEP 316 pre:/post:; helpers never call the reference"],
    ["Checked before use", "0 / 6 reject the reference; 5 proven within B_T"],
  ];
  items.forEach(([h, b], i) => {
    s.addText([{ text: h, options: { bold: true, color: TEAL, breakLine: true } }, { text: b, options: { color: INK } }],
      { x: lx + 0.2, y: 1.6 + i * 0.55, w: lw - 0.4, h: 0.52, fontFace: FONT, fontSize: 10.5, valign: "top", margin: 0, isTextBox: true });
  });
  pending(s, lx, 4.0, lw, 0.85, "Keyu", "one example contract (e.g. HumanEval/40 from the demo) and the key semantic point you checked for each task.", 10);

  const rx = 5.0, rw = W - M - rx;
  const hdr = ["Remaining work", "Owner", "Due"].map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: INK } } }));
  const rows = [
    ["Reference contracts for 30 tasks", "Keyu", "final"],
    ["Validated mutants, ≥ 5 per task", "Zoey", "final"],
    ["30 tasks and the second model", "Jiahao", "final"],
    ["Full matrix and mutation scores", "Bingsong", "final"],
    ["Showcase poster file", "all", "Dec 3"],
    ["Report, talk, reproducible repo", "all", "Dec 8/10"],
  ].map(r => r.map(t => ({ text: t, options: { color: INK } })));
  s.addTable([hdr, ...rows], { x: rx, y: 1.1, w: rw, colW: [2.55, 0.95, 1.0], fontFace: FONT, fontSize: 10.5,
    rowH: 0.4, border: { type: "solid", pt: 0.75, color: LINE }, margin: [0.03, 0.08, 0.03, 0.08], valign: "middle" });
  s.addText("Pipeline is ready: new contracts and mutants run with one command.", { x: rx, y: 4.0, w: rw, h: 0.5,
    fontFace: FONT, fontSize: 11, color: TEAL, bold: true, margin: 0, valign: "top", isTextBox: true });
}
