const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ImageRun,
  convertInchesToTwip, VerticalAlign
} = require("docx");
const fs = require("fs");

const QR_IMG = fs.readFileSync("/home/claude/qr_website.png");

const DEEP  = "611426";
const MID   = "8E3850";
const GREY  = "555555";
const LIGHT = "888888";

function sectionHeader(text) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), bold: true, color: DEEP, size: 18, font: "Calibri" })],
    spacing: { before: 120, after: 40 },
    border: { bottom: { color: DEEP, size: 4, style: BorderStyle.SINGLE } },
  });
}

function jobTitle(title, org, dates) {
  return [new Paragraph({
    children: [
      new TextRun({ text: title, bold: true, size: 18, color: "222222", font: "Calibri" }),
      new TextRun({ text: "  ·  ", size: 16, color: LIGHT, font: "Calibri" }),
      new TextRun({ text: org, italics: true, size: 16, color: MID, font: "Calibri" }),
      new TextRun({ text: "  " + dates, size: 15, color: LIGHT, font: "Calibri" }),
    ],
    spacing: { before: 70, after: 20 },
  })];
}

function bullet(text) {
  return new Paragraph({
    children: [new TextRun({ text, size: 16, color: GREY, font: "Calibri" })],
    bullet: { level: 0 },
    spacing: { after: 10 },
  });
}

function skillRow(label, items) {
  return new Paragraph({
    children: [
      new TextRun({ text: label + ":  ", bold: true, size: 16, color: DEEP, font: "Calibri" }),
      new TextRun({ text: items.join("  ·  "), size: 16, color: GREY, font: "Calibri" }),
    ],
    spacing: { after: 30 },
  });
}

// Achievements as a single compact line each
function achievementLine(date, title, org, detail) {
  const parts = [];
  if (date) parts.push(new TextRun({ text: date + "  —  ", size: 15, color: LIGHT, font: "Calibri" }));
  parts.push(new TextRun({ text: title, bold: true, size: 16, color: "222222", font: "Calibri" }));
  parts.push(new TextRun({ text: "  ·  " + org, size: 15, color: MID, italics: true, font: "Calibri" }));
  if (detail) parts.push(new TextRun({ text: "  " + detail, size: 15, color: GREY, font: "Calibri" }));
  return new Paragraph({ children: parts, spacing: { before: 50, after: 15 } });
}

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{
        level: 0,
        format: "bullet",
        text: "–",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 300, hanging: 180 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        margin: {
          top: convertInchesToTwip(0.5),
          bottom: convertInchesToTwip(0.45),
          left: convertInchesToTwip(0.65),
          right: convertInchesToTwip(0.65),
        },
      },
    },
    children: [
      // ── HEADER TABLE ─────────────────────────────────────────────────────
      new Table({
        width: { size: 10116, type: WidthType.DXA },
        borders: {
          top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
          left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
          insideH: { style: BorderStyle.NONE }, insideV: { style: BorderStyle.NONE },
        },
        rows: [new TableRow({
          children: [
            new TableCell({
              width: { size: 8500, type: WidthType.DXA },
              verticalAlign: VerticalAlign.CENTER,
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
              },
              children: [
                new Paragraph({
                  children: [new TextRun({ text: "SHRESTHA ROY", bold: true, size: 48, color: DEEP, font: "Calibri" })],
                  spacing: { after: 30 },
                }),
                new Paragraph({
                  children: [new TextRun({ text: "Fashion Design  ·  Kolkata, India", size: 18, color: MID, italics: true, font: "Calibri" })],
                  spacing: { after: 50 },
                }),
                new Paragraph({
                  children: [
                    new TextRun({ text: "shrestharoy.work@gmail.com", size: 15, color: GREY, font: "Calibri" }),
                    new TextRun({ text: "   |   +91 62892 78968", size: 15, color: GREY, font: "Calibri" }),
                  ],
                }),
              ],
            }),
            new TableCell({
              width: { size: 1616, type: WidthType.DXA },
              verticalAlign: VerticalAlign.CENTER,
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
              },
              children: [
                new Paragraph({
                  alignment: AlignmentType.RIGHT,
                  children: [new ImageRun({ data: QR_IMG, transformation: { width: 70, height: 70 }, type: "png" })],
                }),
                new Paragraph({
                  alignment: AlignmentType.RIGHT,
                  children: [new TextRun({ text: "shrestha-roy.netlify.app", size: 12, color: LIGHT, font: "Calibri" })],
                }),
              ],
            }),
          ],
        })],
      }),

      new Paragraph({
        border: { bottom: { color: "CCCCCC", size: 4, style: BorderStyle.SINGLE } },
        spacing: { after: 0, before: 50 },
      }),

      // ── PROFILE ──────────────────────────────────────────────────────────
      sectionHeader("Profile"),
      new Paragraph({
        children: [new TextRun({
          text: "Fashion designer with strong grounding in garment construction, textile research and creative direction. Experienced in design, illustration, styling, product development and B2B management. Collaborative and detail-oriented; eager to contribute to forward-thinking fashion environments.",
          size: 16, color: GREY, font: "Calibri",
        })],
        spacing: { after: 0 },
      }),

      // ── EXPERIENCE ───────────────────────────────────────────────────────
      sectionHeader("Experience"),

      ...jobTitle("Junior Designer", "Kiran Uttam Ghosh", "2026 – Present"),
      bullet("Fashion design & illustration for seasonal collections; creative direction, product development & quality management."),
      bullet("Fashion merchandising, inventory & B2B sales management; fashion styling and graphic design."),

      ...jobTitle("Graduation Collection — What Remains", "Sister Nivedita University", "Jan – May 2026"),
      bullet("6-look S/S '26 avant-garde womenswear on survival & resilience — concept through construction, full spec sheets & documentation."),
      bullet("Sculptural corset with hand-draped rosettes, faux-leather ensemble with beaded embellishments, sheer floral mesh dress."),

      ...jobTitle("Assistant Designer & Backstage Stylist", "Rohan Pariyar Studios", "Nov 2025"),
      bullet("Styling & coordination for I-Medici collection, Victoria Memorial Hall × Consulate Generale of Italy."),

      ...jobTitle("Fashion Design Intern", "Abhishek Dutta India", "Jun – Aug 2025"),
      bullet("Styled Bengali & Bollywood celebrities for Anandabazaar Patrika, Sananda, Anandalok; editorial swimwear shoot for Sananda."),
      bullet("Pre-production for Style & THE CITY (Darshoo OTT); designed full uniform range for NIPS Hospitality."),

      ...jobTitle("Assistant Designer", "Roy Calcutta — Calcutta Times Fashion Week", "March 2025"),
      bullet("Backstage coordination & styling for Nawabs of Bengal collection."),

      ...jobTitle("Assistant Designer & Stylist", "SNU Fashion Show 2025", "Dec 2024 – Jan 2025"),
      bullet("Conceptualised 28-look collection for 38th AIU Inter-University East Zonal Youth Festival; garment construction & runway hosting."),

      ...jobTitle("Store Associate", "Sutra Handloom", "Aug 2024"),
      bullet("Styling advice, product selection, fitting & visual merchandising."),

      // ── EDUCATION ────────────────────────────────────────────────────────
      sectionHeader("Education"),

      ...jobTitle("B.Des Fashion Design", "Sister Nivedita University, Kolkata", "2022 – 2026"),
      new Paragraph({
        children: [new TextRun({ text: "CGPA: 8.91", size: 15, color: GREY, font: "Calibri" })],
        spacing: { after: 15 },
        indent: { left: convertInchesToTwip(0.1) },
      }),

      ...jobTitle("Indian School Certificate (ISC)", "Modern High School for Girls, Kolkata", "2020 – 2022"),
      new Paragraph({
        children: [new TextRun({ text: "93%", size: 15, color: GREY, font: "Calibri" })],
        spacing: { after: 15 },
        indent: { left: convertInchesToTwip(0.1) },
      }),

      ...jobTitle("ICSE", "Loreto Day School, Dharamtala, Kolkata", "2009 – 2020"),
      new Paragraph({
        children: [new TextRun({ text: "90.6%", size: 15, color: GREY, font: "Calibri" })],
        spacing: { after: 15 },
        indent: { left: convertInchesToTwip(0.1) },
      }),

      // ── SKILLS ───────────────────────────────────────────────────────────
      sectionHeader("Skills"),
      skillRow("Design & Construction", ["Pattern Making", "Draping", "Garment Construction", "Sewing & Finishing", "Hand Embroidery"]),
      skillRow("Illustration & Software", ["Digital Illustration", "Technical Flats", "Photoshop", "Illustrator", "InDesign", "CLO3D", "CorelDraw"]),
      skillRow("Textile & Research", ["Fabric Sourcing", "Print Development", "Natural Dyeing", "Trend Forecasting", "Market Analysis"]),
      skillRow("Fashion & Creative Direction", ["Fashion Design", "Fashion Illustration", "Creative Direction", "Product Development & Management", "Fashion Styling"]),
      skillRow("Business & Management", ["Fashion Merchandising", "Inventory Management", "B2B Sales Management", "Quality Management", "Graphic Design"]),

      // ── ACHIEVEMENTS ─────────────────────────────────────────────────────
      sectionHeader("Achievements & Certificates"),
      achievementLine("Nov 2025", "Assistant Designer Certificate", "Rohan Pariyar Studios", "I-Medici × Victoria Memorial Hall × Consulate General of Italy."),
      achievementLine("Jun – Aug 2025", "Internship Certificate", "Abhishek Dutta India", null),
      achievementLine("2024 – 2025", "Certificate of Merit — Designer of the Year", "Sister Nivedita University", null),
      achievementLine("March 2024", "Assistant Designer Certificate", "Roy Calcutta", "Swatantra Fashion Show — 38th AIU Inter-University East Zonal Youth Festival 2024–25."),
      achievementLine(null, "Certificate of Merit", "Sister Nivedita University", "Representing SNU Fashion Dept. at AIU fest."),
      achievementLine("2024", "Volunteer Certificate", "Sutra Handloom Studies", null),
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/mnt/user-data/outputs/ShresthaRoy_CV_Corporate.docx", buf);
  console.log("Corporate DOCX saved.");
});
