// Two slides to merge into the team's Google-Slides deck: the new demo (page 5) and the poster
// layout (page 10). Build: cat deck_head.js demo_slide.js two_slides.js > build_two.js && node build_two.js out.pptx
const POSTER_PNG = process.env.POSTER_PNG;

function s_poster() {
  const s = base("Showcase poster draft",
`Poster draft for the CS Immersion Showcase, for feedback. The file is due December 3.
It is a 48 by 36 inch landscape poster with three columns. Left: the motivation and research question, the definitions with every term written mathematically, the pilot setup, and who did what. Middle: the verification pipeline, the same example as our demo (one wrong program, two contracts), and the determinacy chart. Right: mutation scores per task, the main findings, the takeaway and next steps.
All numbers are from the six-task pilot and will be replaced by the 30-task results. We would like feedback on what to cut: the middle column is the densest.`);
  const ih = 4.0, iw = ih * 4 / 3;
  s.addShape(pres.shapes.RECTANGLE, { x: M - 0.02, y: 1.06, w: iw + 0.04, h: ih + 0.04, fill: { color: "FFFFFF" },
    line: { color: LINE, width: 1 } });
  s.addImage({ path: POSTER_PNG, x: M, y: 1.08, w: iw, h: ih, altText: "Poster draft: three-column layout" });
  const rx = M + iw + 0.35, rw = W - M - rx;
  const items = [
    ["Format", "48 × 36 in landscape, three columns; file due Dec 3"],
    ["Left", "motivation, definitions, pilot setup, team"],
    ["Middle", "pipeline, demo example, determinacy chart"],
    ["Right", "mutation scores, findings, takeaway"],
    ["Feedback wanted", "what to cut; the middle column is the densest"],
  ];
  items.forEach(([h, b], i) => {
    s.addText([{ text: h, options: { bold: true, color: TEAL, breakLine: true } }, { text: b, options: { color: INK } }],
      { x: rx, y: 1.1 + i * 0.78, w: rw, h: 0.72, fontFace: FONT, fontSize: 11.5, valign: "top", margin: 0,
        isTextBox: true });
  });
}

page = 4; PRESENTER = "Bingsong"; s_demo();
page = 9; PRESENTER = "Keyu"; s_poster();
pres.writeFile({ fileName: process.argv[2] }).then(f => console.log("wrote " + f));
