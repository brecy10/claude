// Convert a lightweight Markdown dialect (Chinese report) into a styled .docx with docx-js.
// Supported: # / ## / ### headings, paragraphs with **bold** and *italic*, "- " bullets,
// "1. " numbered items, pipe tables (first row = header) preceded by "Table: caption",
// figures "![caption](path)", "> note" callouts, "---pagebreak---", "[[TOC]]", "[[COVER]]".
const fs = require("fs");
const path = require("path");
const d = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, PageBreak, TableOfContents, Footer, Header, PageNumber,
  LevelFormat, TabStopType, VerticalAlign } = d;

const SRC = process.argv[2], OUT = process.argv[3];
const base = path.dirname(SRC);
const lines = fs.readFileSync(SRC, "utf8").split(/\r?\n/);

const FONT = { ascii: "Times New Roman", hAnsi: "Times New Roman", eastAsia: "宋体", cs: "Times New Roman" };
const HFONT = { ascii: "Arial", hAnsi: "Arial", eastAsia: "黑体", cs: "Arial" };
const BLUE = "1F4E79", GREY = "52514E";
const TEXTW = 9638; // A4 (11906) - 2*1134 margins = 9638 DXA

function pngSize(p) {
  const b = fs.readFileSync(p);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

function runs(text, opts = {}) {
  // inline **bold**, *italic*, ^sup^, ~sub~
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|\^[^^]+\^|~[^~]+~)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...opts }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, ...opts }));
    else if (t.startsWith("*")) out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, ...opts }));
    else if (t.startsWith("^")) out.push(new TextRun({ text: t.slice(1, -1), superScript: true, font: FONT, ...opts }));
    else out.push(new TextRun({ text: t.slice(1, -1), subScript: true, font: FONT, ...opts }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...opts }));
  return out;
}

let figNo = 0, tabNo = 0, chap = 0;
const children = [];
let pendingTableCaption = null;

function para(text, extra = {}) {
  return new Paragraph({ children: runs(text, extra.run || {}), spacing: { after: 120, line: 360 }, indent: extra.noIndent ? undefined : { firstLine: 480 }, alignment: AlignmentType.JUSTIFIED, ...(extra.p || {}) });
}

function makeTable(rows) {
  const n = rows[0].length;
  // column widths proportional to max text length (bounded)
  const lens = Array(n).fill(0);
  rows.forEach(r => r.forEach((c, i) => { lens[i] = Math.max(lens[i], Math.min(28, [...c].length)); }));
  const tot = lens.reduce((a, b) => a + Math.max(b, 4), 0);
  let widths = lens.map(l => Math.floor(TEXTW * Math.max(l, 4) / tot));
  widths[n - 1] += TEXTW - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: TEXTW, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((c, ci) => new TableCell({
        borders, width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { fill: "DCE6F2", type: ShadingType.CLEAR, color: "auto" } : (ri % 2 === 0 ? { fill: "F7F7F5", type: ShadingType.CLEAR, color: "auto" } : undefined),
        margins: { top: 50, bottom: 50, left: 80, right: 80 }, verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: { line: 276 },
          children: runs(c.trim(), { size: 18, bold: ri === 0 }) })]
      }))
    }))
  });
}

function cover(title, subtitle, meta) {
  const out = [];
  out.push(new Paragraph({ spacing: { before: 2600 }, children: [] }));
  out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: title, bold: true, size: 44, font: HFONT, color: BLUE })] }));
  out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 900 }, children: [new TextRun({ text: subtitle, size: 28, font: HFONT, color: GREY })] }));
  meta.forEach(m => out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: m, size: 24, font: FONT })] })));
  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

let i = 0;
let tableBuf = [];
function flushTable() {
  if (!tableBuf.length) return;
  const rows = tableBuf.filter(l => !/^\|\s*:?-+/.test(l)).map(l => l.replace(/^\|/, "").replace(/\|\s*$/, "").split("|"));
  tabNo += 1;
  if (pendingTableCaption) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 }, keepNext: true,
      children: [new TextRun({ text: `表 ${chap}-${tabNo}  `, bold: true, size: 20, font: HFONT }), ...runs(pendingTableCaption, { size: 20 })] }));
  }
  children.push(makeTable(rows));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [] }));
  tableBuf = []; pendingTableCaption = null;
}

const meta = {};
for (; i < lines.length; i++) {
  const L = lines[i];
  if (L.startsWith("|")) { tableBuf.push(L); continue; } else flushTable();
  if (!L.trim()) continue;
  if (L.startsWith("@title ")) { meta.title = L.slice(7); continue; }
  if (L.startsWith("@subtitle ")) { meta.subtitle = L.slice(10); continue; }
  if (L.startsWith("@meta ")) { (meta.meta = meta.meta || []).push(L.slice(6)); continue; }
  if (L.trim() === "[[COVER]]") { children.push(...cover(meta.title, meta.subtitle, meta.meta || [])); continue; }
  if (L.trim() === "[[TOC]]") {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: "目  录", bold: true, size: 32, font: HFONT })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: "（打开文档时请选择“更新域”；如目录为空，可右键目录区域 → 更新域，或按 F9）", size: 18, color: GREY, font: FONT })] }));
    children.push(new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-2" }));
    children.push(new Paragraph({ children: [new PageBreak()] }));
    continue;
  }
  if (L.trim() === "---pagebreak---") { children.push(new Paragraph({ children: [new PageBreak()] })); continue; }
  let m;
  if ((m = L.match(/^# (.*)/))) {
    if (!/^(摘要|参考文献|附录)/.test(m[1])) { chap += 1; figNo = 0; tabNo = 0; }
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: children.length > 3, children: [new TextRun({ text: m[1], font: HFONT })] }));
    continue;
  }
  if ((m = L.match(/^## (.*)/))) { children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: m[1], font: HFONT })] })); continue; }
  if ((m = L.match(/^### (.*)/))) { children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: m[1], font: HFONT })] })); continue; }
  if ((m = L.match(/^Table: (.*)/))) { pendingTableCaption = m[1]; continue; }
  if ((m = L.match(/^!\[(.*)\]\((.*)\)(\{(\d+)\})?/))) {
    const p = path.resolve(base, m[2]);
    const sz = pngSize(p); const maxW = m[4] ? parseInt(m[4]) : 620;
    const w = Math.min(maxW, 620), h = Math.round(w * sz.h / sz.w);
    figNo += 1;
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data: fs.readFileSync(p), transformation: { width: w, height: h },
        altText: { title: `图 ${chap}-${figNo}`, description: m[1], name: path.basename(p) } })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: `图 ${chap}-${figNo}  `, bold: true, size: 20, font: HFONT }), ...runs(m[1], { size: 20 })] }));
    continue;
  }
  if ((m = L.match(/^> (.*)/))) {
    children.push(new Paragraph({ children: runs(m[1], { size: 21, color: "1F3864" }), spacing: { before: 80, after: 120, line: 320 },
      shading: { fill: "EEF4FC", type: ShadingType.CLEAR, color: "auto" }, indent: { left: 200, right: 200 },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: "2A78D6", space: 8 } } }));
    continue;
  }
  if ((m = L.match(/^- (.*)/))) { children.push(new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60, line: 340 }, children: runs(m[1]) })); continue; }
  if ((m = L.match(/^  - (.*)/))) { children.push(new Paragraph({ numbering: { reference: "bul", level: 1 }, spacing: { after: 40, line: 320 }, children: runs(m[1], { size: 20 }) })); continue; }
  if ((m = L.match(/^\[(\d+)\] (.*)/))) {
    children.push(new Paragraph({ spacing: { after: 40, line: 280 }, indent: { left: 480, hanging: 480 }, children: [new TextRun({ text: `[${m[1]}] `, font: FONT, size: 18 }), ...runs(m[2], { size: 18 })] }));
    continue;
  }
  if (L.startsWith("=")) { children.push(para(L.slice(1).trim(), { noIndent: true, p: { alignment: AlignmentType.CENTER } })); continue; }
  children.push(para(L));
}
flushTable();

const doc = new Document({
  creator: "TGV-GC study", title: meta.title || "report", features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: HFONT, color: BLUE }, paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: HFONT, color: BLUE }, paragraph: { spacing: { before: 260, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: HFONT, color: "2E2E2E" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ]
  },
  numbering: { config: [{ reference: "bul", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } },
    { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1100, hanging: 300 } } } } ] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1200, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6", space: 4 } },
      children: [new TextRun({ text: "微晶玻璃基板 TGV 三维封装可行性研究方案与多物理场仿真报告", size: 16, color: GREY, font: FONT })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["— ", PageNumber.CURRENT, " —"], size: 18, font: FONT })] })] }) },
    children
  }]
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("written", OUT, children.length, "blocks"); });
