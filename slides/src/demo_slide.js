function s_demo() {
  const s = base("Demo: one wrong program, two contracts",
`Demo. One command, about three seconds, run live (recording as backup).
The implementation is Zoey's mutant m4 of HumanEval/40: it looks for a PAIR that sums to zero instead of a triple, so it is wrong, for example on [1, -1, 5].
The same mutant is checked against two contracts, both with the task bound len(l) <= 4.
Left: Qwen's contract v1_40_2. Its only postcondition is "the result is a bool". CrossHair confirms it over all paths, so the wrong program is formally ACCEPTED within the bound. Proven is not the same as correct: the contract is too weak.
Right: Keyu's human contract says the result equals "some three positions sum to zero". CrossHair finds two opposite numbers (in this run [-47925, 47925]; the numbers change from run to run, so do not read them out): the mutant returns True, the formula says False. The pipeline re-runs it in a fresh process, checks that the input is legal, and checks that the reference (False) satisfies the contract, so this is a discriminating kill.
Over the full pilot, this Qwen contract accepts all six HumanEval/40 mutants and the human contract kills all six.`);

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.06, w: W - 2 * M, h: 0.36, rectRadius: 0.05,
    fill: { color: CODEBG }, line: { type: "none" } });
  s.addText("$ python -m pipeline.demo --task HumanEval/40 --contract qwen_v1_40_2,human --impl mutant_m4 --bounded",
    { x: M + 0.15, y: 1.06, w: W - 2 * M - 0.3, h: 0.36, fontFace: MONO, fontSize: 9.5, color: INK,
      valign: "middle", margin: 0, isTextBox: true });

  s.addText([
    { text: "Program under test: ", options: { bold: true } },
    { text: "mutant m4 of HumanEval/40 (Zoey). It checks for a pair that sums to zero instead of a triple, so it is wrong on [1, -1, 5]. Both contracts get the bound len(l) ≤ 4." },
  ], { x: M, y: 1.5, w: W - 2 * M, h: 0.42, fontFace: FONT, fontSize: 11, color: INK, valign: "middle",
    margin: 0, isTextBox: true });

  const cw = (W - 2 * M - 0.3) / 2, cy = 2.02;
  const ok = "C9D1D9", bad = "FF9B8F", dim = "8B949E", good = "7EE0B5";
  const cols = [
    { x: M, head: "Qwen contract v1_40_2", color: AMBER,
      code: [["pre:  all(isinstance(x, int) for x in l)", INK], ["post: isinstance(__return__, bool)", INK]],
      term: [["line 33: info: Confirmed over all paths.", ok], ["(1.2s)", dim], [" ", ok],
             ["no counterexample", ok]],
      verdict: "ACCEPTED_PROVEN_BOUNDED", note: "contract too weak" },
    { x: M + cw + 0.3, head: "Human contract (Keyu)", color: TEAL,
      code: [["post: isinstance(__return__, bool)", INK], ["post: __return__ == any(l[i]+l[j]+l[k] == 0", INK],
             ["        for i < j < k)", INK]],
      term: [["line 21: error: false when calling", bad], ["  triples_sum_to_zero([-47925, 47925])", bad],
             ["  (which returns True)", bad], ["re-run: legal input; reference: False", dim]],
      verdict: "REJECTED", note: "discriminating kill, re-executed" },
  ];
  cols.forEach(c => {
    s.addText(c.head, { x: c.x, y: cy, w: cw, h: 0.26, fontFace: FONT, fontSize: 12, bold: true, color: INK,
      margin: 0, isTextBox: true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: cy + 0.3, w: cw, h: 0.62, rectRadius: 0.05,
      fill: { color: CODEBG }, line: { type: "none" } });
    s.addText(c.code.map(([t, col], i) => ({ text: t, options: { color: col, breakLine: i < c.code.length - 1 } })),
      { x: c.x + 0.12, y: cy + 0.34, w: cw - 0.24, h: 0.54, fontFace: MONO, fontSize: 8.5, valign: "middle",
        margin: 0, isTextBox: true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: cy + 1.0, w: cw, h: 0.95, rectRadius: 0.05,
      fill: { color: TERM }, line: { type: "none" } });
    s.addText(c.term.map(([t, col], i) => ({ text: t, options: { color: col, breakLine: i < c.term.length - 1 } })),
      { x: c.x + 0.12, y: cy + 1.06, w: cw - 0.24, h: 0.83, fontFace: MONO, fontSize: 8.5, valign: "top",
        margin: 0, isTextBox: true });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: cy + 2.05, w: cw, h: 0.5, rectRadius: 0.06,
      fill: { color: c.color }, line: { type: "none" } });
    s.addText([{ text: c.verdict, options: { bold: true, fontFace: MONO, fontSize: 11 } },
               { text: "   " + c.note, options: { fontSize: 10 } }],
      { x: c.x + 0.12, y: cy + 2.05, w: cw - 0.24, h: 0.5, fontFace: FONT, color: "FFFFFF", valign: "middle",
        margin: 0, isTextBox: true });
  });
  s.addText([{ text: "Full pilot run: ", options: { bold: true } },
             { text: "v1_40_2 accepts all 6 HumanEval/40 mutants as proven; the human contract kills all 6." }],
    { x: M, y: 4.7, w: W - 2 * M, h: 0.3, fontFace: FONT, fontSize: 11, color: INK, valign: "middle",
      margin: 0, isTextBox: true });
}
