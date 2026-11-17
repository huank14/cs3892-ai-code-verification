// CS Immersion Showcase poster draft, Group E (48 x 36 in, landscape). Style follows the lab's
// VUSE poster: Times New Roman, tan section headers, dark rounded outlines.
// Run: NODE_PATH=../deck/node_modules node poster.js Verifying-AI-Generated-Code-Poster-Draft.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "POSTER48x36", width: 48, height: 36 });
pres.layout = "POSTER48x36";
pres.author = "Group E";
pres.title = "Verifying AI-Generated Code - Poster draft";

const SERIF = "Times New Roman", MATH = "Cambria", MONO = "Courier New";
const INK = "000000", TAN = "EDD9A3", EDGE = "1E1E1E", GREY = "555555", CODE = "F3F3F3",
      TERM = "1E2329", GREEN = "2E7D32", RED = "B42318", GOLD = "9A6700", BLUE = "1F5F8B";
const BODY = 32;
const s = pres.addSlide();
s.background = { color: "FFFFFF" };
if (process.env.CUT) {   // debugging aid: keep only the first CUT add* calls
  let n = 0; const lim = +process.env.CUT;
  for (const m of ["addText", "addShape", "addImage", "addTable", "addChart"]) {
    const f = s[m].bind(s); s[m] = (...a) => (++n <= lim ? f(...a) : s);
  }
  s.count = () => n;
}
const here = (f) => path.join(__dirname, f);

// ---------- header ----------
s.addImage({ path: here("m_image1.png"), x: 1.2, y: 0.95, w: 8.6, h: 1.757 });
s.addText("Verifying AI-Generated Code", { x: 10, y: 0.55, w: 28, h: 1.45, fontFace: SERIF, fontSize: 88,
  bold: true, color: INK, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("Can LLM-Written Contracts Catch Incorrect Programs?", { x: 9, y: 2.0, w: 30, h: 1.0, fontFace: SERIF,
  fontSize: 56, color: INK, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText("Jiahao Zhang, Bingsong Liu, Zoey Tang, Keyu Huang", { x: 9, y: 3.08, w: 30, h: 0.75, fontFace: SERIF,
  fontSize: 42, color: INK, align: "center", valign: "middle", margin: 0, isTextBox: true });
s.addText([
  { text: "Department of Computer Science, Vanderbilt University, Nashville, TN, USA", options: { breakLine: true } },
  { text: "CS 3892 / 5892 Formal Methods: Safe and Trustworthy AI, Fall 2026" },
], { x: 9, y: 3.85, w: 30, h: 1.15, fontFace: SERIF, fontSize: 32, italic: true, color: INK, align: "center",
  valign: "middle", margin: 0, isTextBox: true });
s.addImage({ path: here("qr_repo.png"), x: 43.1, y: 0.7, w: 3.6, h: 3.6 });
s.addText("Code and data", { x: 41.6, y: 4.35, w: 6.6, h: 0.55, fontFace: SERIF, fontSize: 26, color: INK,
  align: "center", margin: 0, isTextBox: true });
s.addText("DRAFT: pilot results (6 tasks)", { x: 35.0, y: 1.6, w: 7.6, h: 0.9, fontFace: SERIF, fontSize: 28,
  bold: true, color: RED, align: "center", valign: "middle", margin: 0, isTextBox: true,
  line: { color: RED, width: 2.5, dashType: "dash" } });

// ---------- section frame ----------
function section(x, y, w, h, title) {
  if (h < 2) throw new Error("section too small: " + title + " h=" + h);
  // Tan header with rounded top corners: a rounded rectangle whose lower half is squared off by a
  // plain rectangle; the frame outline is drawn last so it sits on top of both.
  // (pptxgenjs writes an unreadable round2SameRect when given rectRadius.)
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.25, fill: { color: "FFFFFF" },
    line: { type: "none" } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.85, rectRadius: 0.25, fill: { color: TAN },
    line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.4, w, h: 0.45, fill: { color: TAN }, line: { type: "none" } });
  s.addShape(pres.shapes.LINE, { x, y: y + 0.85, w, h: 0, line: { color: EDGE, width: 2.5 } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.25, fill: { type: "none" },
    line: { color: EDGE, width: 2.5 } });
  s.addText(title, { x, y, w, h: 0.85, fontFace: SERIF, fontSize: 40, bold: true, color: INK, align: "center",
    valign: "middle", margin: 0, isTextBox: true });
  return { x: x + 0.35, y: y + 1.05, w: w - 0.7, h: h - 1.25 };
}
// runs: array of [text, opts]; strings become plain paragraphs
function para(items, box, opts) {
  const runs = [];
  items.forEach((it, i) => {
    const last = i === items.length - 1;
    if (typeof it === "string") runs.push({ text: it, options: { breakLine: !last } });
    else if (it.bullet) it.parts.forEach((p, k) => runs.push({ text: p[0], options: Object.assign({ bullet: k === 0 ? { indent: 28 } : undefined, breakLine: k === it.parts.length - 1 && !last }, p[1] || {}) }));
    else it.parts.forEach((p, k) => runs.push({ text: p[0], options: Object.assign({ breakLine: k === it.parts.length - 1 && !last }, p[1] || {}) }));
  });
  s.addText(runs, Object.assign({ x: box.x, y: box.y, w: box.w, h: box.h, fontFace: SERIF, fontSize: BODY, color: INK,
    valign: "top", margin: 0, paraSpaceAfter: 6, isTextBox: true }, opts || {}));
}
const B = (t) => [t, { bold: true }];
const I = (t) => [t, { italic: true }];

const top = 5.55, bottom = 35.55;
const LX = 0.45, LW = 11.6, MX = 12.4, MW = 23.2, RX = 35.95, RW = 11.6;

// ---------- left column ----------
let b = section(LX, top, LW, 7.3, "Motivation");
para([
  "LLMs now write much of everyday code. Tests catch some mistakes, but passing tests does not mean the program is correct.",
  { parts: [["A formal "], B("contract"), [" (pre- and postconditions) plus a verifier could check AI code automatically, but only if the contract itself says enough. If the LLM writes both the code and the contract, a weak contract can certify wrong code."]] },
  { parts: [B("Question: "), I("are LLM-written PEP 316 contracts strong enough to reject incorrect implementations?")] },
], b);

b = section(LX, top + 7.6, LW, 10.9, "Definitions");
const defs = [
  ["Contract", "c = (pre_c, post_c),  post_c = φ₁ ∧ … ∧ φ_k"],
  ["Correctness (Hoare triple)", "{pre_c} f {post_c}:  ∀x. pre_c(x) ⇒ post_c(x, f(x))"],
  ["Bounded check (size bound B_T)", "∀x. B_T(x) ∧ pre_c(x) ⇒ post_c(x, f(x))"],
  ["Killed mutant (f* = reference)", "∃x. pre_c(x) ∧ ¬post_c(x, m(x)) ∧ post_c(x, f*(x))"],
  ["Mutation score", "MS(c) = |{m ∈ M_T : killed(c, m)}| / |M_T|"],
  ["Effective score", "MS_eff(c) = 0 if c rejects f* on a legal input x ∈ D_T, else MS(c)"],
];
defs.forEach(([h, f], i) => {
  s.addText(h, { x: b.x, y: b.y + i * 1.6, w: b.w, h: 0.55, fontFace: SERIF, fontSize: 30, bold: true,
    color: BLUE, margin: 0, isTextBox: true });
  s.addText(f, { x: b.x + 0.2, y: b.y + i * 1.6 + 0.55, w: b.w - 0.2, h: 0.95, fontFace: MATH, fontSize: 27,
    color: INK, margin: 0, valign: "top", isTextBox: true });
});

b = section(LX, top + 18.8, LW, 6.6, "Setup (pilot)");
para([
  { bullet: true, parts: [B("Tasks: "), ["6 HumanEval tasks (30 for the final)"]] },
  { bullet: true, parts: [B("LLM: "), ["Qwen3.8-27B-FP8, 2 prompt versions × 3 samples per task = 36 responses; 19 contracts parse"]] },
  { bullet: true, parts: [B("Baseline: "), ["6 human-reviewed reference contracts"]] },
  { bullet: true, parts: [B("Mutants: "), ["36 validated wrong programs, each with a witness input"]] },
  { bullet: true, parts: [B("Verifier: "), ["CrossHair 0.0.110 + Z3 5.1.0, 60 s per postcondition"]] },
], b);

b = section(LX, top + 25.7, LW, bottom - (top + 25.7), "Team");
para([
  { parts: [B("Jiahao Zhang: "), ["LLM generation, contract parsing"]] },
  { parts: [B("Bingsong Liu: "), ["verification pipeline, demo"]] },
  { parts: [B("Zoey Tang: "), ["mutants, input domains, evaluation"]] },
  { parts: [B("Keyu Huang: "), ["human reference contracts"]] },
], b);

// ---------- middle column ----------
b = section(MX, top, MW, 9.9, "Verification Pipeline");
// inputs row
const inY = b.y + 0.2, boxH = 1.55, gap = 0.45;
const inputs = [["Qwen output", "implementation + contract"], ["Human contract", "reviewed reference spec"],
                ["Mutants", "6 wrong programs per task"], ["HumanEval reference", "f*, official tests"]];
const iw = (b.w - 3 * gap) / 4;
inputs.forEach(([h, t], i) => {
  const x = b.x + i * (iw + gap);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: inY, w: iw, h: boxH, rectRadius: 0.15, fill: { color: "FFFFFF" },
    line: { color: EDGE, width: 1.5 } });
  s.addText([{ text: h, options: { bold: true, breakLine: true } }, { text: t, options: { fontSize: 22 } }],
    { x: x + 0.1, y: inY, w: iw - 0.2, h: boxH, fontFace: SERIF, fontSize: 26, color: INK, align: "center",
      valign: "middle", margin: 0, isTextBox: true });
});
const steps = [
  ["Compose", "contract × implementation, task bound B_T inserted as the first pre:"],
  ["CrossHair + Z3", "bounded proof within B_T, then an unbounded counterexample search"],
  ["Re-execute", "every counterexample in a fresh process; check x ∈ D_T and the reference at x"],
];
const sy = inY + boxH + 0.75, sh = 2.1, sw = (b.w - 2 * 0.9 - 4.2 - 0.9) / 3;
s.addShape(pres.shapes.LINE, { x: b.x, y: inY + boxH + 0.35, w: b.w, h: 0, line: { color: EDGE, width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: b.x + b.w / 2, y: inY + boxH, w: 0, h: 0.35, line: { color: EDGE, width: 1.5 } });
steps.forEach(([h, t], i) => {
  const x = b.x + i * (sw + 0.9);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: sy, w: sw, h: sh, rectRadius: 0.15, fill: { color: "FFFFFF" },
    line: { color: EDGE, width: 1.5, dashType: "dash" } });
  s.addText([{ text: h, options: { bold: true, underline: { style: "sng" }, breakLine: true } },
             { text: t, options: { fontSize: 22 } }],
    { x: x + 0.15, y: sy, w: sw - 0.3, h: sh, fontFace: SERIF, fontSize: 26, color: INK, align: "center",
      valign: "middle", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: x + sw + 0.05, y: sy + sh / 2, w: 0.8, h: 0,
    line: { color: EDGE, width: 2, endArrowType: "triangle" } });
});
if (true) {
  const x = b.x + 3 * (sw + 0.9);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: sy, w: b.w - (x - b.x), h: sh, rectRadius: 0.15,
    fill: { color: TAN }, line: { color: EDGE, width: 1.5 } });
  s.addText("Verdict", { x, y: sy, w: b.w - (x - b.x), h: sh, fontFace: SERIF, fontSize: 30, bold: true,
    color: INK, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
const verdicts = [
  ["REJECTED", RED, "a re-executed counterexample, and the reference satisfies c at the same input"],
  ["NON-DISCRIMINATING", GOLD, "the reference violates c at that input too: no credit"],
  ["PROVEN (bounded)", GREEN, "every φᵢ confirmed on all paths within B_T"],
  ["INCONCLUSIVE", GREY, "budget ran out; never read as correct"],
];
const vy = sy + sh + 0.45, vw = (b.w - 0.45) / 2;
verdicts.forEach(([h, c, t], i) => {
  const x = b.x + (i % 2) * (vw + 0.45), y = vy + Math.floor(i / 2) * 1.15;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 0.42, h: 0.42, rectRadius: 0.21, fill: { color: c },
    line: { type: "none" } });
  s.addText([{ text: h + ": ", options: { bold: true, color: c } }, { text: t }],
    { x: x + 0.6, y: y - 0.12, w: vw - 0.6, h: 1.05, fontFace: SERIF, fontSize: 24, color: INK, valign: "top",
      margin: 0, isTextBox: true });
});
s.addText("Determinacy = (rejected + proven) / checks.  Over-restrictive: c rejects f* at some x ∈ D_T.",
  { x: b.x, y: b.y + b.h - 0.6, w: b.w, h: 0.55, fontFace: SERIF, fontSize: 24, italic: true, color: GREY,
    margin: 0, isTextBox: true });

// example
b = section(MX, top + 10.2, MW, 10.0, "Example: One Wrong Program, Two Contracts");
para([{ parts: [B("Mutant m4 of HumanEval/40 "), ["(triples_sum_to_zero) checks for a "], I("pair"), [" that sums to zero instead of a triple, so it is wrong on [1, −1, 5]. Both contracts get the bound len(l) ≤ 4."]] }],
  { x: b.x, y: b.y, w: b.w, h: 1.0 }, { fontSize: 26 });
const ew = (b.w - 0.6) / 2, ey = b.y + 1.25;
[
  { x: b.x, head: "Qwen contract v1_40_2", code: ["pre:  all(isinstance(x, int) for x in l)", "post: isinstance(__return__, bool)"],
    term: [["Confirmed over all paths.  (1.2 s)", "C9D1D9"], ["no counterexample", "C9D1D9"]],
    verdict: "PROVEN (bounded): the wrong program is verified", color: GOLD },
  { x: b.x + ew + 0.6, head: "Human reference contract", code: ["post: isinstance(__return__, bool)", "post: __return__ == any(l[i]+l[j]+l[k] == 0", "                       for i < j < k)"],
    term: [["false when calling", "FF9B8F"], ["  triples_sum_to_zero([-47925, 47925])", "FF9B8F"], ["  returns True; reference returns False", "8B949E"]],
    verdict: "REJECTED: discriminating kill, re-executed", color: GREEN },
].forEach(c => {
  s.addText(c.head, { x: c.x, y: ey, w: ew, h: 0.55, fontFace: SERIF, fontSize: 28, bold: true, color: INK,
    margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: ey + 0.65, w: ew, h: 1.75, rectRadius: 0.12,
    fill: { color: CODE }, line: { type: "none" } });
  s.addText(c.code.map((t, i) => ({ text: t, options: { breakLine: i < c.code.length - 1 } })),
    { x: c.x + 0.25, y: ey + 0.7, w: ew - 0.5, h: 1.65, fontFace: MONO, fontSize: 20, color: INK, valign: "middle",
      margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: ey + 2.55, w: ew, h: 1.95, rectRadius: 0.12,
    fill: { color: TERM }, line: { type: "none" } });
  s.addText(c.term.map(([t, col], i) => ({ text: t, options: { color: col, breakLine: i < c.term.length - 1 } })),
    { x: c.x + 0.25, y: ey + 2.6, w: ew - 0.5, h: 1.85, fontFace: MONO, fontSize: 20, valign: "middle",
      margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x, y: ey + 4.65, w: ew, h: 0.95, rectRadius: 0.12,
    fill: { color: c.color }, line: { type: "none" } });
  s.addText(c.verdict, { x: c.x + 0.2, y: ey + 4.65, w: ew - 0.4, h: 0.95, fontFace: SERIF, fontSize: 26,
    bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
});
para([{ parts: [B("Proven is not correct: "), ["across the pilot, v1_40_2 accepts all 6 HumanEval/40 mutants, while the human contract kills all 6."]] }],
  { x: b.x, y: ey + 5.8, w: b.w, h: 0.9 }, { fontSize: 26 });

// determinacy chart
b = section(MX, top + 20.5, MW, bottom - (top + 20.5), "Bounding Input Size Makes the Verifier Decide");
const labels = ["All 38 checks", "Contract × reference", "Contract × Qwen code"];
s.addChart(pres.charts.BAR, [
  { name: "Unbounded (proposal setup)", labels, values: [11, 11, 11] },
  { name: "Combined (bounded + unbounded)", labels, values: [84, 79, 89] },
], { x: b.x, y: b.y - 0.1, w: 13.6, h: b.h + 0.1, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60,
  chartColors: ["A9B1B9", BLUE], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"',
  dataLabelFontSize: 22, dataLabelColor: INK, dataLabelFontFace: SERIF,
  valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 25, valAxisLabelFormatCode: '0"%"',
  valAxisLabelFontSize: 20, catAxisLabelFontSize: 22, valAxisLabelColor: GREY, catAxisLabelColor: INK,
  valAxisLabelFontFace: SERIF, catAxisLabelFontFace: SERIF,
  valGridLine: { color: "E3E7EA", size: 1 }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "t", legendFontSize: 22, legendFontFace: SERIF, legendColor: INK,
  showTitle: true, title: "Determinate checks (rejected or proven), 19 Qwen contracts", titleFontSize: 24,
  titleColor: INK, titleFontFace: SERIF });
para([
  { parts: [["Unbounded, CrossHair never finishes exploring lists and strings: "], B("11%"), [" of checks decide at 60 s."]] },
  { parts: [["One size bound per task (e.g. len ≤ 4): "], B("84%"), [", above our 80% target. Proofs then hold only within the bound."]] },
  { parts: [["Full pilot run (229 checks): "], B("93%"), [" determinate, "], B("98%"), [" of contract × mutant checks."]] },
  { parts: [["Remaining inconclusive: float lists and nonlinear products (tool limits)."]] },
], { x: b.x + 14.0, y: b.y + 0.2, w: b.w - 14.0, h: b.h - 0.3 }, { fontSize: 26, paraSpaceAfter: 10 });

// ---------- right column ----------
b = section(RX, top, RW, 9.4, "Results: Mutation Score");
const hdr = ["Task", "Human", "Qwen median (n)"].map(t => ({ text: t, options: { bold: true, fill: { color: TAN } } }));
const rows = [["HumanEval/0", "1.00", "0.50 (2)"], ["HumanEval/6", "1.00", "0.00 (1)"], ["HumanEval/8", "1.00", "0.75 (4)"],
  ["HumanEval/12", "1.00", "1.00 (2)"], ["HumanEval/28", "1.00", "1.00 (6)"], ["HumanEval/40", "1.00", "1.00 (4)"]]
  .map(r => [{ text: r[0] }, { text: r[1], options: { align: "center" } },
    { text: r[2], options: { align: "center", color: r[2].startsWith("1.00") ? INK : RED, bold: !r[2].startsWith("1.00") } }]);
rows.push([{ text: "All (mean)", options: { bold: true } }, { text: "1.00", options: { bold: true, align: "center" } },
  { text: "0.76 (19)", options: { bold: true, align: "center" } }]);
s.addTable([hdr, ...rows], { x: b.x, y: b.y, w: b.w, colW: [3.9, 2.4, b.w - 6.3], fontFace: SERIF, fontSize: 26,
  color: INK, rowH: 0.78, border: { type: "solid", pt: 1, color: "9A9A9A" }, margin: [0.04, 0.15, 0.04, 0.15],
  valign: "middle" });
s.addText("MS_eff per contract; Qwen = median over its parsed contracts for the task.", { x: b.x, y: b.y + 6.4,
  w: b.w, h: 0.9, fontFace: SERIF, fontSize: 22, italic: true, color: GREY, margin: 0, valign: "top", isTextBox: true });

b = section(RX, top + 9.7, RW, 11.0, "Findings");
para([
  { bullet: true, parts: [B("Human contracts kill all 36 mutants"), [" and never reject the reference."]] },
  { bullet: true, parts: [B("4 of 19 Qwen contracts score 0: "), ["3 reject correct outputs, 1 is too weak to reject anything."]] },
  { bullet: true, parts: [B("Wrong contracts, found by the verifier: "), ["operator precedence (HumanEval/8), the empty string (/6), object identity (/0)."]] },
  { bullet: true, parts: [B("Wrong AI code, found by the human contract: "), ["2 of 35 Qwen implementations return [0] instead of [] for the empty string."]] },
  { bullet: true, parts: [B("Prompting matters: "), ["readable contracts rose from 6/18 to 13/18 with a one-condition-per-line prompt."]] },
], b);

b = section(RX, top + 21.0, RW, 5.0, "Takeaway");
para([
  "A verifier is only as strong as its contract. LLM-written contracts are often right, but about one in five of the parsed ones either rejects correct code or accept everything, so a passing proof needs a contract-strength check (mutants) before it can be trusted.",
], b);

b = section(RX, top + 26.3, RW, bottom - (top + 26.3), "Next Steps");
para([
  { bullet: true, parts: [["30 tasks and a second LLM"]] },
  { bullet: true, parts: [["End-to-end score incl. unparsed outputs"]] },
], b);

if (s.count) console.log("calls", s.count());
pres.writeFile({ fileName: process.argv[2] || "poster.pptx" }).then(f => console.log("wrote " + f));
