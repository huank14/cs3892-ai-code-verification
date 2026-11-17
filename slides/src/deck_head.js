// Group E Milestone 1 deck (team version). 16:9, 10 x 5.625 in.
// Build: cat deck_head.js old_slides.js demo_slide.js slides_89.js deck_main.js > build_deck.js
//        node build_deck.js Verifying-AI-Generated-Code-Milestone1.pptx && python strip_dirs.py <pptx>
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Group E";
pres.title = "Verifying AI-Generated Code - Milestone 1";

const INK = "1F2933", MUTED = "5F6B76", TEAL = "0F766E", BRICK = "B42318",
      GRAYBAR = "A9B1B9", TINT = "EEF3F2", CODEBG = "F4F5F7", TERM = "1E2329",
      LINE = "D5DBDF", AMBER = "9A6700";
const FONT = "Arial", MATH = "Cambria", MONO = "Courier New";
const W = 10, M = 0.5;
let page = 0;
let PRESENTER = "";

function base(title, notes) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  page += 1;
  s.addText(title, { x: M, y: 0.28, w: W - 2 * M, h: 0.72, fontFace: FONT, fontSize: 24,
    bold: true, color: INK, valign: "middle", margin: 0, isTextBox: true });
  s.addText("Group E  ·  Verifying AI-Generated Code  ·  Milestone 1", { x: M, y: 5.2, w: 5.5, h: 0.25,
    fontFace: FONT, fontSize: 9, color: MUTED, margin: 0, isTextBox: true });
  s.addText(`${PRESENTER ? "Presenter: " + PRESENTER + "     " : ""}${page}`, { x: W - M - 3.5, y: 5.2, w: 3.5,
    h: 0.25, fontFace: FONT, fontSize: 9, color: MUTED, align: "right", margin: 0, isTextBox: true });
  if (notes) s.addNotes(notes);
  return s;
}

function arrow(s, x1, y, x2) {
  s.addShape(pres.shapes.LINE, { x: x1, y, w: x2 - x1, h: 0,
    line: { color: MUTED, width: 1.5, endArrowType: "triangle" } });
}

// Box for content a teammate still has to supply. Dashed outline, no fill.
function pending(s, x, y, w, h, who, text, size) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: GRAYBAR, width: 1, dashType: "dash" } });
  s.addText([{ text: `To fill (${who}): `, options: { bold: true, color: MUTED } },
             { text, options: { color: MUTED } }],
    { x: x + 0.12, y: y + 0.06, w: w - 0.24, h: h - 0.12, fontFace: FONT, fontSize: size || 10.5,
      valign: "middle", margin: 0, isTextBox: true });
}
