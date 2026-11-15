#!/usr/bin/env python3
"""Convierte docs/documento_proyecto.md en docs/documento_proyecto.pdf.
Uso: pip install reportlab && python tools/build_pdf.py
Para editar el documento: cambia el .md y volve a correr este script."""
import re, math, pathlib, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "docs/documento_proyecto.md", ROOT / "docs/documento_proyecto.pdf"
FD = next((d for d in ["/usr/share/fonts/truetype/dejavu", "C:/Windows/Fonts", "/Library/Fonts", "/usr/share/fonts/dejavu"]
           if os.path.exists(os.path.join(d, "DejaVuSans.ttf"))), None)
if FD:
    for n, f in [("D", "DejaVuSans.ttf"), ("D-B", "DejaVuSans-Bold.ttf"), ("D-I", "DejaVuSans-Oblique.ttf"), ("D-BI", "DejaVuSans-BoldOblique.ttf")]:
        pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))
    pdfmetrics.registerFontFamily("D", normal="D", bold="D-B", italic="D-I", boldItalic="D-BI")
    BASE, BOLD = "D", "D-B"
else:
    BASE, BOLD = "Helvetica", "Helvetica-Bold"  # sin DejaVu algunos simbolos no se ven

INK, ACC, LINE = colors.HexColor("#14202b"), colors.HexColor("#0f766e"), colors.HexColor("#cfd8e0")
S = {
 "t": ParagraphStyle("t", fontName=BOLD, fontSize=24, leading=28, textColor=ACC, spaceAfter=6),
 "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=14, leading=18, textColor=ACC, spaceBefore=14, spaceAfter=6, keepWithNext=1),
 "sub": ParagraphStyle("sub", fontName=BASE, fontSize=12, leading=16, textColor=INK, spaceAfter=8),
 "p": ParagraphStyle("p", fontName=BASE, fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=6),
 "c": ParagraphStyle("c", fontName=BASE, fontSize=7.8, leading=10.2, textColor=INK),
 "ch": ParagraphStyle("ch", fontName=BOLD, fontSize=7.8, leading=10.2, textColor=colors.white),
}
def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r'<font color="#0f766e">\1</font>', t)
def table(rows):
    head, body = rows[0], rows[1:]
    w = [max(8, min(45, max(len(r[i]) for r in rows))) ** 0.7 for i in range(len(head))]
    tw = A4[0] - 4 * cm
    cw = [tw * x / sum(w) for x in w]
    data = [[Paragraph(inline(c), S["ch"]) for c in head]] + [[Paragraph(inline(c), S["c"]) for c in r] for r in body]
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACC), ("GRID", (0, 0), (-1, -1), .4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f6f8")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t
def build():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    story, i, seen_sub = [], 0, False
    while i < len(lines):
        l = lines[i].rstrip()
        if not l: i += 1; continue
        if l.startswith("# "): story.append(Paragraph(inline(l[2:]), S["t"]))
        elif l.startswith("## "):
            if not seen_sub: story.append(Paragraph(inline(l[3:]), S["sub"])); seen_sub = True
            else: story.append(Paragraph(inline(l[3:]), S["h2"]))
        elif l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
                i += 1
            story += [table(rows), Spacer(1, 8)]; continue
        elif re.match(r"(- |\d+\. )", l):
            items, num = [], bool(re.match(r"\d+\. ", l))
            while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
                tx = re.sub(r"^(- |\d+\. )", "", lines[i]).replace("[ ]", "\u2610").replace("[x]", "\u2611")
                items.append(ListItem(Paragraph(inline(tx), S["p"]), leftIndent=14)); i += 1
            story += [ListFlowable(items, bulletType="1" if num else "bullet", bulletFontName=BASE, bulletFontSize=8, start=None if not num else 1, leftIndent=14), Spacer(1, 4)]; continue
        else: story.append(Paragraph(inline(l), S["p"]))
        i += 1
    def foot(c, d):
        c.saveState(); c.setFont(BASE, 7.5); c.setFillColor(colors.HexColor("#5b6b7a"))
        c.drawString(2 * cm, 1.1 * cm, "Simulador de Misiones Espaciales · Borrador 0.1 · 14/11/2026")
        c.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Página {d.page}"); c.restoreState()
    SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Simulador de Misiones Espaciales: documento de proyecto", author="[COMPLETAR]").build(story, onFirstPage=foot, onLaterPages=foot)
    print("OK:", OUT)
if __name__ == "__main__":
    build()
