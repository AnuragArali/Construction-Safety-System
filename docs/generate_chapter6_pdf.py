"""
SIT Tumakuru – Edge-Enabled Privacy-Preserving Construction Safety System
Academic Project Report – Chapter 6 PDF Generator
Sections: 6.1 Software Requirements, 6.2 Algorithm, 6.3 Flowchart
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF
from io import BytesIO

# ── Paths ──────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent
OUTPUT = BASE / "SIT_Chapter6_Software_Algorithm_Flowchart.pdf"

# ── Colour Palette ─────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#0D1B2A")
TEAL     = colors.HexColor("#1B6CA8")
LTBLUE   = colors.HexColor("#D6E8F7")
ORANGE   = colors.HexColor("#E87722")
LGREY    = colors.HexColor("#F4F4F4")
MIDGREY  = colors.HexColor("#CCCCCC")
DARKGREY = colors.HexColor("#555555")
WHITE    = colors.white
BLACK    = colors.black

PAGE_W, PAGE_H = A4

# ── Page-number / header-footer ────────────────────────────────────────────
def _page_decor(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(1.5*cm, h - 0.75*cm,
                      "Edge-Enabled Privacy-Preserving Construction Safety System")
    canvas.drawRightString(w - 1.5*cm, h - 0.75*cm, "SIT Tumakuru  |  2026-27")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.5*cm, 0.3*cm,
                      "Department of ECE / CSE")
    canvas.drawRightString(w - 1.5*cm, 0.3*cm, f"Page {doc.page}")
    canvas.restoreState()

def _first_page(canvas, doc):
    pass  # Cover page has no header/footer

# ── Style Sheet ────────────────────────────────────────────────────────────
def build_styles():
    ss = getSampleStyleSheet()
    def add(name, **kw):
        ss.add(ParagraphStyle(name=name, **kw))

    add("ChapterTitle",
        fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
        spaceBefore=14, spaceAfter=6, alignment=TA_LEFT)
    add("SectionTitle",
        fontName="Helvetica-Bold", fontSize=13, textColor=TEAL,
        spaceBefore=10, spaceAfter=4, alignment=TA_LEFT)
    add("SubSection",
        fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
        spaceBefore=8, spaceAfter=3, alignment=TA_LEFT)
    add("SubSubSection",
        fontName="Helvetica-Bold", fontSize=10, textColor=DARKGREY,
        spaceBefore=6, spaceAfter=2, alignment=TA_LEFT)
    add("BodyJ",
        fontName="Helvetica", fontSize=10, textColor=BLACK,
        leading=15, spaceBefore=4, spaceAfter=4, alignment=TA_JUSTIFY)
    add("BodyL",
        fontName="Helvetica", fontSize=10, textColor=BLACK,
        leading=15, spaceBefore=2, spaceAfter=2, alignment=TA_LEFT)
    add("Caption",
        fontName="Helvetica-Oblique", fontSize=9, textColor=DARKGREY,
        spaceBefore=2, spaceAfter=8, alignment=TA_CENTER)
    add("BulletItem",
        fontName="Helvetica", fontSize=10, textColor=BLACK,
        leading=14, spaceBefore=2, spaceAfter=2,
        leftIndent=20, bulletIndent=8, alignment=TA_JUSTIFY)
    add("SubBullet",
        fontName="Helvetica", fontSize=9.5, textColor=DARKGREY,
        leading=13, spaceBefore=1, spaceAfter=1,
        leftIndent=36, bulletIndent=22, alignment=TA_LEFT)
    add("CodeBlock",
        fontName="Courier", fontSize=8, textColor=BLACK,
        leading=11.5, spaceBefore=4, spaceAfter=4,
        leftIndent=12, backColor=LGREY)
    add("TableHeader",
        fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
        alignment=TA_CENTER)
    add("TableCell",
        fontName="Helvetica", fontSize=9, textColor=BLACK,
        alignment=TA_LEFT, leading=12)
    add("CoverTitle",
        fontName="Helvetica-Bold", fontSize=22, textColor=NAVY,
        alignment=TA_CENTER, leading=28, spaceBefore=10, spaceAfter=10)
    add("CoverSub",
        fontName="Helvetica", fontSize=13, textColor=TEAL,
        alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
    add("CoverBody",
        fontName="Helvetica", fontSize=11, textColor=DARKGREY,
        alignment=TA_CENTER, spaceBefore=3, spaceAfter=3)
    add("StepNum",
        fontName="Helvetica-Bold", fontSize=10, textColor=TEAL,
        spaceBefore=6, spaceAfter=1, alignment=TA_LEFT)
    add("StepBody",
        fontName="Helvetica", fontSize=10, textColor=BLACK,
        leading=14, spaceBefore=1, spaceAfter=3,
        leftIndent=12, alignment=TA_JUSTIFY)
    return ss

# ── Helpers ────────────────────────────────────────────────────────────────
def hr(ss):
    return HRFlowable(width="100%", thickness=1, color=TEAL,
                      spaceBefore=4, spaceAfter=4)

def sp(h=0.3):
    return Spacer(1, h*cm)

def tbl(data, col_widths, header_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style = TableStyle([
        ("BACKGROUND",     (0, 0), (-1, header_rows-1), NAVY),
        ("TEXTCOLOR",      (0, 0), (-1, header_rows-1), WHITE),
        ("FONTNAME",       (0, 0), (-1, header_rows-1), "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, header_rows-1), 9),
        ("ALIGN",          (0, 0), (-1, header_rows-1), "CENTER"),
        ("FONTNAME",       (0, header_rows), (-1, -1), "Helvetica"),
        ("FONTSIZE",       (0, header_rows), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [WHITE, LGREY]),
        ("ALIGN",          (1, header_rows), (-1, -1), "LEFT"),
        ("ALIGN",          (0, header_rows), (0, -1), "LEFT"),
        ("GRID",           (0, 0), (-1, -1), 0.4, MIDGREY),
        ("BOX",            (0, 0), (-1, -1), 1, TEAL),
        ("TOPPADDING",     (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
    ])
    t.setStyle(style)
    return t

def bullet(ss, text, style_name="BulletItem"):
    return Paragraph(text, ss[style_name], bulletText="\u2022")

def sub_bullet(ss, text):
    return Paragraph(text, ss["SubBullet"], bulletText="-")

# ══════════════════════════════════════════════════════════════════════════
#  FLOWCHART GENERATION (using ReportLab Drawing primitives)
# ══════════════════════════════════════════════════════════════════════════

def _draw_box(d, x, y, w, h, text, fill_color, text_color=WHITE, font_size=8, bold=True):
    """Draw a rounded-corner rectangle with centred text."""
    d.add(Rect(x, y, w, h, rx=6, ry=6, fillColor=fill_color, strokeColor=colors.HexColor("#333333"), strokeWidth=0.7))
    lines = text.split("\n")
    font_name = "Helvetica-Bold" if bold else "Helvetica"
    total_h = len(lines) * (font_size + 2)
    start_y = y + h/2 + total_h/2 - font_size/2
    for i, line in enumerate(lines):
        d.add(String(x + w/2, start_y - i*(font_size+2), line,
                     fontName=font_name, fontSize=font_size,
                     fillColor=text_color, textAnchor="middle"))

def _draw_diamond(d, cx, cy, half_w, half_h, text, fill_color, text_color=WHITE, font_size=7):
    """Draw a diamond (decision) shape."""
    pts = [cx, cy+half_h, cx+half_w, cy, cx, cy-half_h, cx-half_w, cy]
    d.add(Polygon(pts, fillColor=fill_color, strokeColor=colors.HexColor("#333333"), strokeWidth=0.7))
    lines = text.split("\n")
    total_h = len(lines) * (font_size + 1)
    start_y = cy + total_h/2 - font_size/2
    for i, line in enumerate(lines):
        d.add(String(cx, start_y - i*(font_size+1), line,
                     fontName="Helvetica-Bold", fontSize=font_size,
                     fillColor=text_color, textAnchor="middle"))

def _arrow_down(d, x, y1, y2, clr=colors.HexColor("#333333")):
    d.add(Line(x, y1, x, y2, strokeColor=clr, strokeWidth=1))
    # arrowhead
    d.add(Polygon([x, y2, x-3, y2+7, x+3, y2+7],
                  fillColor=clr, strokeColor=clr, strokeWidth=0.3))

def _arrow_right(d, x1, y, x2, clr=colors.HexColor("#333333")):
    d.add(Line(x1, y, x2, y, strokeColor=clr, strokeWidth=1))
    d.add(Polygon([x2, y, x2-7, y+3, x2-7, y-3],
                  fillColor=clr, strokeColor=clr, strokeWidth=0.3))

def _arrow_left(d, x1, y, x2, clr=colors.HexColor("#333333")):
    d.add(Line(x1, y, x2, y, strokeColor=clr, strokeWidth=1))
    d.add(Polygon([x2, y, x2+7, y+3, x2+7, y-3],
                  fillColor=clr, strokeColor=clr, strokeWidth=0.3))


def generate_system_flowchart():
    """Generate the main system-level flowchart (Figure 6.1)."""
    W, H = 460, 680
    d = Drawing(W, H)

    # Colours
    C_START   = colors.HexColor("#1B6CA8")
    C_PROCESS = colors.HexColor("#0D1B2A")
    C_DECIDE  = colors.HexColor("#E87722")
    C_ALERT   = colors.HexColor("#C62828")
    C_DB      = colors.HexColor("#2E7D32")
    C_END     = colors.HexColor("#555555")

    bw, bh = 160, 32
    cx = W/2 - bw/2  # left edge of centred boxes

    y = H - 40
    _draw_box(d, cx, y, bw, bh, "START", C_START); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Camera Input\n(Webcam / AR / Video)", C_PROCESS); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Image Preprocessing\n(CLAHE + Letterbox)", C_PROCESS); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "AI Detection Module\n(YOLOv8 + HSV PPE)", C_PROCESS); y -= 55
    _arrow_down(d, W/2, y+bh+23, y+bh)

    # Decision diamond
    dy = y + bh/2
    _draw_diamond(d, W/2, dy, 90, 25, "Violation\nDetected?", C_DECIDE); y -= 55
    _arrow_down(d, W/2, dy-25, y+bh)

    # Yes path (centre)
    _draw_box(d, cx, y, bw, bh, "Safety Analysis\n(Rules + Debounce)", C_ALERT, font_size=8); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Generate Recommendation", C_ALERT, font_size=8); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Voice Alert (TTS)\n(EN / HI / KN / ES)", C_ALERT, font_size=8); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Store Safety Event\n(SQLite - Local Only)", C_DB, font_size=8); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    _draw_box(d, cx, y, bw, bh, "Privacy Guard\n(Face Blur + Annotate)", C_PROCESS, font_size=8); y -= 50
    _arrow_down(d, W/2, y+bh+18, y+bh)

    # Decision: Continue?
    dy2 = y + bh/2
    _draw_diamond(d, W/2, dy2, 90, 25, "Continue\nMonitoring?", C_DECIDE); y -= 50

    # Yes loops back
    d.add(String(W/2-100, dy2+2, "Yes", fontName="Helvetica-Bold", fontSize=7,
                 fillColor=colors.HexColor("#2E7D32"), textAnchor="middle"))
    # Left-side loop-back arrow
    loop_x = cx - 30
    d.add(Line(W/2-90, dy2, loop_x, dy2, strokeColor=colors.HexColor("#2E7D32"), strokeWidth=1))
    d.add(Line(loop_x, dy2, loop_x, H-40+bh/2, strokeColor=colors.HexColor("#2E7D32"), strokeWidth=1))
    _arrow_right(d, loop_x, H-40+bh/2, cx, clr=colors.HexColor("#2E7D32"))

    # No -> END
    _arrow_down(d, W/2, dy2-25, y+bh)
    d.add(String(W/2+12, dy2-30, "No", fontName="Helvetica-Bold", fontSize=7,
                 fillColor=C_ALERT, textAnchor="start"))
    _draw_box(d, cx, y, bw, bh, "STOP", C_END)

    # "No violation" side branch from first diamond
    no_x = cx + bw + 30
    no_y_diamond = H - 40 - 50*3 - 55/2 + bh/2   # y of first diamond
    d.add(String(W/2+95, no_y_diamond+2, "No", fontName="Helvetica-Bold", fontSize=7,
                 fillColor=colors.HexColor("#2E7D32"), textAnchor="start"))
    # Arrow right from diamond then down to Privacy Guard
    privacy_y = H - 40 - 50*3 - 55 - 50*4  # y of "Privacy Guard" box
    d.add(Line(W/2+90, no_y_diamond, no_x+40, no_y_diamond,
               strokeColor=colors.HexColor("#2E7D32"), strokeWidth=1))
    d.add(Line(no_x+40, no_y_diamond, no_x+40, privacy_y+bh/2,
               strokeColor=colors.HexColor("#2E7D32"), strokeWidth=1))
    _arrow_left(d, no_x+40, privacy_y+bh/2, cx+bw,
                clr=colors.HexColor("#2E7D32"))

    d.add(String(W/2+12, H - 40 - 50*3 - 55/2 + bh/2 - 8, "Yes",
                 fontName="Helvetica-Bold", fontSize=7,
                 fillColor=C_ALERT, textAnchor="start"))

    return d


def generate_edge_pipeline_flowchart():
    """Generate the edge processing pipeline flowchart (Figure 6.2)."""
    W, H = 460, 420
    d = Drawing(W, H)

    C_PIPE  = colors.HexColor("#1565C0")
    C_AI    = colors.HexColor("#E87722")
    C_PRIV  = colors.HexColor("#2E7D32")
    C_OUT   = colors.HexColor("#C62828")

    bw, bh = 130, 28
    gap = 10
    # Row 1 — single pipeline strip
    x_start = 10
    y_row1 = H - 50

    boxes_row1 = [
        ("Frame\nCapture", C_PIPE),
        ("CLAHE\nEnhance", C_PIPE),
        ("YOLO\nInference", C_AI),
        ("HSV PPE\nVerify", C_AI),
    ]
    short_bw = 95
    for i, (label, clr) in enumerate(boxes_row1):
        bx = x_start + i*(short_bw + gap)
        _draw_box(d, bx, y_row1, short_bw, bh+6, label, clr, font_size=7.5)
        if i > 0:
            _arrow_right(d, bx - gap + 2, y_row1 + (bh+6)/2, bx - 2,
                         clr=colors.HexColor("#333333"))

    # Arrow down from HSV PPE Verify
    last_x = x_start + 3*(short_bw + gap) + short_bw/2
    _arrow_down(d, last_x, y_row1, y_row1 - 40)

    # Row 2
    y_row2 = y_row1 - 40 - bh - 6
    boxes_row2 = [
        ("PPE-Worker\nAssociation", C_AI),
        ("Violation\nAnalyzer", C_OUT),
        ("Alert\nManager", C_OUT),
        ("Voice TTS\nEngine", C_OUT),
    ]
    for i, (label, clr) in enumerate(boxes_row2):
        bx = x_start + (3-i)*(short_bw + gap)  # right to left
        _draw_box(d, bx, y_row2, short_bw, bh+6, label, clr, font_size=7.5)

    # Arrows for row 2 (right to left)
    for i in range(3):
        bx_from = x_start + (3-i)*(short_bw + gap)
        bx_to   = x_start + (3-i-1)*(short_bw + gap) + short_bw
        _arrow_left(d, bx_from - 2, y_row2 + (bh+6)/2, bx_to + 2,
                     clr=colors.HexColor("#333333"))

    # Connect row 1 -> row 2
    row2_first_x = x_start + 3*(short_bw + gap) + short_bw/2
    _arrow_down(d, row2_first_x, y_row1 - 2, y_row2 + bh + 6 + 2,
                clr=colors.HexColor("#333333"))

    # Arrow down from Voice TTS to Row 3
    tts_cx = x_start + short_bw/2
    _arrow_down(d, tts_cx, y_row2, y_row2 - 40,
                clr=colors.HexColor("#333333"))

    # Row 3
    y_row3 = y_row2 - 40 - bh - 6
    boxes_row3 = [
        ("Face Blur\n(Privacy)", C_PRIV),
        ("Annotate\nFrame", C_PIPE),
        ("MJPEG\nEncode", C_PIPE),
        ("Browser\nStream", C_PIPE),
    ]
    for i, (label, clr) in enumerate(boxes_row3):
        bx = x_start + i*(short_bw + gap)
        _draw_box(d, bx, y_row3, short_bw, bh+6, label, clr, font_size=7.5)
        if i > 0:
            _arrow_right(d, bx - gap + 2, y_row3 + (bh+6)/2, bx - 2,
                         clr=colors.HexColor("#333333"))

    # Connect row 2 -> row 3
    _arrow_down(d, tts_cx, y_row2 - 2, y_row3 + bh + 6 + 2,
                clr=colors.HexColor("#333333"))

    # Row 4: DB persist (side branch from Violation Analyzer)
    y_db = y_row2 - 25
    va_cx = x_start + 2*(short_bw + gap) + short_bw/2  # violation analyser centre
    db_bx = va_cx - short_bw/2
    _draw_box(d, db_bx, y_row3 - 50, short_bw, bh+6, "SQLite\nLocal DB", C_PRIV, font_size=7.5)
    _arrow_down(d, va_cx, y_row2 - 2, y_row3 - 50 + bh + 6 + 2,
                clr=colors.HexColor("#2E7D32"))

    # Legend
    y_leg = 20
    for i, (label, clr) in enumerate([("Camera / Stream", C_PIPE), ("AI / Detection", C_AI),
                                       ("Alert / Violation", C_OUT), ("Privacy / Storage", C_PRIV)]):
        lx = x_start + i*115
        d.add(Rect(lx, y_leg, 12, 12, fillColor=clr, strokeWidth=0))
        d.add(String(lx+16, y_leg+2, label, fontName="Helvetica", fontSize=7, fillColor=BLACK))

    return d


def generate_data_flow_flowchart():
    """Generate the frontend-backend data flow diagram (Figure 6.3)."""
    W, H = 460, 300
    d = Drawing(W, H)

    C_FE   = colors.HexColor("#1565C0")
    C_API  = colors.HexColor("#E87722")
    C_BE   = colors.HexColor("#0D1B2A")
    C_EDGE = colors.HexColor("#2E7D32")

    bw, bh = 110, 70

    # Frontend column
    fe_x, fe_y = 10, H - 100
    _draw_box(d, fe_x, fe_y, bw, bh,
              "React Frontend\n\nDashboard\nLive Monitor\nAlerts / History\nAnalytics", C_FE, font_size=7)

    # API Gateway column
    api_x = fe_x + bw + 40
    _draw_box(d, api_x, fe_y, bw, bh,
              "FastAPI REST\n\n/api/v1/*\n14 endpoints\nJSON + MJPEG", C_API, font_size=7)

    # Backend column
    be_x = api_x + bw + 40
    _draw_box(d, be_x, fe_y, bw, bh,
              "Backend Modules\n\nAI Detection\nSafety Analysis\nVoice Alerts\nPrivacy Guard", C_BE, font_size=7)

    # Arrows
    _arrow_right(d, fe_x+bw+2, fe_y + bh/2 + 8, api_x-2, clr=C_FE)
    d.add(String(fe_x+bw+14, fe_y+bh/2+14, "Axios HTTP", fontName="Helvetica", fontSize=6, fillColor=DARKGREY))

    _arrow_left(d, api_x-2, fe_y + bh/2 - 8, fe_x+bw+2, clr=C_API)
    d.add(String(fe_x+bw+14, fe_y+bh/2-18, "JSON / MJPEG", fontName="Helvetica", fontSize=6, fillColor=DARKGREY))

    _arrow_right(d, api_x+bw+2, fe_y + bh/2 + 8, be_x-2, clr=C_API)
    d.add(String(api_x+bw+10, fe_y+bh/2+14, "Function call", fontName="Helvetica", fontSize=6, fillColor=DARKGREY))

    _arrow_left(d, be_x-2, fe_y + bh/2 - 8, api_x+bw+2, clr=C_BE)
    d.add(String(api_x+bw+10, fe_y+bh/2-18, "Results dict", fontName="Helvetica", fontSize=6, fillColor=DARKGREY))

    # Edge hardware row
    edge_y = fe_y - 80
    items = [("Camera\nHardware", C_EDGE), ("SQLite DB\n(Local)", C_EDGE),
             ("TTS Engine\n(pyttsx3)", C_EDGE), ("GPIO / MQTT\n(Future)", C_EDGE)]
    short = 90
    for i, (label, clr) in enumerate(items):
        ix = 25 + i*(short + 18)
        _draw_box(d, ix, edge_y, short, 40, label, clr, font_size=7)
        # Vertical arrow up to backend
        _arrow_down(d, ix + short/2, fe_y - 2, edge_y + 40 + 2, clr=C_EDGE)

    # Label
    d.add(String(W/2, edge_y - 18, "All processing local on Raspberry Pi (no cloud)",
                 fontName="Helvetica-Bold", fontSize=8, fillColor=C_EDGE, textAnchor="middle"))

    return d


# ══════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ══════════════════════════════════════════════════════════════════════════

def build_cover(ss, story):
    story.append(sp(3.5))
    # Institution bar
    cover_bar = Table(
        [[Paragraph("SIT", ParagraphStyle("_L", fontName="Helvetica-Bold",
                                           fontSize=36, textColor=WHITE,
                                           alignment=TA_CENTER)),
          Paragraph("Siddaganga Institute of Technology\nTumakuru - 572 103, Karnataka",
                    ParagraphStyle("_R", fontName="Helvetica", fontSize=12,
                                    textColor=WHITE, alignment=TA_LEFT, leading=18))]],
        colWidths=[3*cm, 12*cm]
    )
    cover_bar.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), NAVY),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1), 14),
    ]))
    story.append(cover_bar)
    story.append(sp(1.5))

    story.append(Paragraph(
        "Edge-Enabled Privacy-Preserving System for<br/>Construction Workspace Management",
        ss["CoverTitle"]))
    story.append(sp(0.3))
    story.append(HRFlowable(width="80%", thickness=2, color=ORANGE,
                            spaceBefore=0, spaceAfter=0))
    story.append(sp(0.6))
    story.append(Paragraph("Chapter 6", ss["CoverSub"]))
    story.append(Paragraph(
        "Software Requirements, Algorithm &amp; Flowchart", ss["CoverSub"]))
    story.append(sp(1.0))
    story.append(Paragraph("Mini-Project Report  |  Academic Year 2026 - 27", ss["CoverBody"]))
    story.append(Paragraph(
        "Department of ECE / CSE  |  Siddaganga Institute of Technology, Tumakuru",
        ss["CoverBody"]))
    story.append(sp(1.5))

    team_data = [
        [Paragraph("<b>Team Members</b>", ParagraphStyle("_th", fontName="Helvetica-Bold",
                    fontSize=10, textColor=WHITE, alignment=TA_CENTER))],
        [Paragraph("Mahalakshmi R",      ss["CoverBody"])],
        [Paragraph("Prathibha V",         ss["CoverBody"])],
        [Paragraph("Priyanka S",          ss["CoverBody"])],
        [Paragraph("Anurag A Aralimarad", ss["CoverBody"])],
        [Paragraph("Badagi Lokamurthy",   ss["CoverBody"])],
    ]
    team_tbl = Table(team_data, colWidths=[8*cm])
    team_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(0,0), TEAL),
        ("BACKGROUND",  (0,1),(0,-1), LGREY),
        ("ALIGN",       (0,0),(0,-1), "CENTER"),
        ("GRID",        (0,0),(0,-1), 0.5, MIDGREY),
        ("BOX",         (0,0),(0,-1), 1, TEAL),
        ("TOPPADDING",  (0,0),(0,-1), 5),
        ("BOTTOMPADDING",(0,0),(0,-1), 5),
    ]))
    story.append(team_tbl)
    story.append(PageBreak())


# ────────────────────────────────────────────────────────────────────────
#  6.1  SOFTWARE REQUIREMENTS
# ────────────────────────────────────────────────────────────────────────
def build_section_6_1(ss, story):
    story.append(Paragraph("CHAPTER 6", ss["SectionTitle"]))
    story.append(Paragraph("Software Requirements, Algorithm &amp; Flowchart", ss["ChapterTitle"]))
    story.append(hr(ss))
    story.append(sp(0.3))
    story.append(Paragraph(
        "This chapter documents the complete software requirements for the Edge-Enabled "
        "Privacy-Preserving Construction Safety System, describes the algorithmic logic "
        "that drives safety detection and alerting, and presents the system flowcharts "
        "illustrating data and control flow from camera input through to voice alert "
        "delivery.", ss["BodyJ"]))
    story.append(sp(0.4))

    # ── 6.1 ─────────────────────────────────────────────────────────────
    story.append(Paragraph("6.1  About Software Requirements", ss["SectionTitle"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The system is architected as a two-tier application (backend + frontend) "
        "deployed entirely on a local edge device (Raspberry Pi 4). Both tiers "
        "communicate over a local-network REST API. The tables below detail every "
        "software dependency, its purpose, minimum compatible version, and licence.",
        ss["BodyJ"]))
    story.append(sp(0.3))

    # ── 6.1.1  Hardware Requirements ─────────────────────────────────────
    story.append(Paragraph("6.1.1  Hardware Requirements", ss["SubSection"]))
    story.append(sp(0.2))

    hw_data = [
        ["Component",            "Specification",                          "Purpose"],
        ["Processing Unit",      "Raspberry Pi 4 Model B (4 GB RAM)",     "Edge inference, local web server, database host"],
        ["Camera",               "USB Webcam / Pi Camera V2 / AR/VR HMD", "Real-time frame capture of construction workspace"],
        ["Storage",              "16 GB+ Class 10 MicroSD (A1 rated)",    "OS, application code, SQLite database, YOLO model weights"],
        ["Network",              "Ethernet / Wi-Fi (site LAN only)",      "Frontend access from on-site devices; no internet required"],
        ["Audio Output",         "3.5 mm speaker or USB audio adapter",   "Voice alert playback via pyttsx3/espeak"],
        ["Power Supply",         "5 V / 3 A USB-C PSU (UPS HAT recommended)", "Continuous operation at construction sites"],
        ["Development Machine",  "Intel i5+ / 8 GB RAM / Windows 10+",   "Development, testing, model training (CPU or GPU)"],
    ]
    story.append(tbl(hw_data, [3.5*cm, 5.5*cm, 6.5*cm]))
    story.append(Paragraph("Table 6.1 -- Hardware requirements specification.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.1.2  Backend Software Requirements ────────────────────────────
    story.append(Paragraph("6.1.2  Backend Software Requirements (Python)", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The backend is implemented entirely in Python and runs as a FastAPI ASGI "
        "server. Table 6.2 lists all production dependencies with their roles.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    be_data = [
        ["Package",          "Version",    "Licence",     "Role in System"],
        ["Python",           ">= 3.10",    "PSF",         "Runtime interpreter"],
        ["FastAPI",          ">= 0.110",   "MIT",         "REST API framework; async ASGI server"],
        ["Uvicorn",          ">= 0.28",    "BSD-3",       "ASGI server (production-grade, multi-worker)"],
        ["Pydantic",         ">= 2.6",     "MIT",         "Request/response validation; Settings model"],
        ["SQLAlchemy",       ">= 2.0",     "MIT",         "ORM for SQLite; models, sessions, queries"],
        ["SQLite",           "3.x (std-lib)", "Public Domain", "Local edge database; zero-config"],
        ["OpenCV-Python",    ">= 4.8",     "Apache 2.0",  "Image capture, preprocessing, CLAHE, blur, annotation"],
        ["NumPy",            ">= 1.24",    "BSD-3",       "Array operations for image and HSV analysis"],
        ["Pillow",           ">= 10.0",    "HPND",        "Supplementary image I/O"],
        ["Ultralytics",      ">= 8.1",     "AGPL-3",      "YOLOv8 model loading, inference, export APIs"],
        ["PyTorch",          ">= 2.0",     "BSD-3",       "Deep-learning backend for YOLO inference"],
        ["TorchVision",      ">= 0.15",    "BSD-3",       "Image transforms (required by Ultralytics)"],
        ["pyttsx3",          ">= 2.90",    "MPL-2.0",     "Offline text-to-speech for voice safety alerts"],
        ["python-multipart", ">= 0.0.9",   "Apache 2.0",  "File upload handling (video samples)"],
        ["pytest",           ">= 8.0",     "MIT",         "Unit and integration test framework"],
        ["HTTPX",            ">= 0.27",    "BSD-3",       "Async test client for FastAPI endpoints"],
    ]
    story.append(tbl(be_data, [3*cm, 2*cm, 2.5*cm, 7.5*cm]))
    story.append(Paragraph("Table 6.2 -- Backend software dependencies.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.1.3  Frontend Software Requirements ──────────────────────────
    story.append(Paragraph("6.1.3  Frontend Software Requirements (React)", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The frontend is a single-page application (SPA) built with React 18 and "
        "bundled by Vite. It communicates with the backend exclusively via Axios HTTP "
        "calls. No AI logic, database operations, or camera access exists in the "
        "frontend -- maintaining strict separation of concerns.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    fe_data = [
        ["Package",           "Version",    "Licence",  "Role in System"],
        ["Node.js",           ">= 18.x",    "MIT",      "JavaScript runtime for build tooling"],
        ["React",             "18.3",       "MIT",      "Component-based UI framework"],
        ["React DOM",         "18.3",       "MIT",      "Browser rendering engine for React"],
        ["React Router DOM",  "6.29",       "MIT",      "Client-side routing (7 pages)"],
        ["Vite",              "6.1",        "MIT",      "Lightning-fast HMR dev server and production bundler"],
        ["Tailwind CSS",      "3.4",        "MIT",      "Utility-first CSS framework for responsive design"],
        ["Axios",             "1.7",        "MIT",      "Promise-based HTTP client for REST API calls"],
        ["Recharts",          "2.15",       "MIT",      "Composable charting library (bar, pie, area, line)"],
        ["Lucide React",      "0.475",      "ISC",      "Icon library (safety, status, navigation icons)"],
        ["PostCSS",           "8.5",        "MIT",      "CSS transformer (Tailwind integration)"],
        ["Autoprefixer",      "10.4",       "MIT",      "Vendor prefix injection for cross-browser CSS"],
    ]
    story.append(tbl(fe_data, [3.2*cm, 2*cm, 1.8*cm, 8*cm]))
    story.append(Paragraph("Table 6.3 -- Frontend software dependencies.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.1.4  Operating System & Deployment ────────────────────────────
    story.append(Paragraph("6.1.4  Operating System and Deployment Requirements", ss["SubSection"]))
    story.append(sp(0.2))

    os_data = [
        ["Environment",     "OS / Platform",                    "Notes"],
        ["Development",     "Windows 10/11 (x64)",             "Full development, testing, model training"],
        ["Edge Deployment", "Raspberry Pi OS Lite 64-bit (Bookworm)", "Headless; systemd autostart; espeak TTS driver"],
        ["Browser Client",  "Any modern browser (Chromium / Firefox / Edge)", "Accesses dashboard via site LAN IP"],
    ]
    story.append(tbl(os_data, [3.5*cm, 5.5*cm, 6.5*cm]))
    story.append(Paragraph("Table 6.4 -- Operating system and deployment platforms.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.1.5  Functional Requirements ──────────────────────────────────
    story.append(Paragraph("6.1.5  Functional Requirements Summary", ss["SubSection"]))
    story.append(sp(0.2))

    func_items = [
        ("FR-01", "Camera Ingestion", "Capture frames from USB webcam, Pi Camera V2, uploaded video, or synthetic scene generator."),
        ("FR-02", "Image Preprocessing", "Apply CLAHE contrast enhancement and letterbox resize to normalise frames for YOLO input."),
        ("FR-03", "Worker Detection", "Detect and localise construction workers using YOLOv8 person detection or skin-tone contour analysis."),
        ("FR-04", "PPE Detection", "Identify safety helmets and high-visibility vests via YOLO class labels or HSV anatomical region analysis."),
        ("FR-05", "PPE-Worker Association", "Associate detected PPE items with individual workers using IoU-based spatial containment logic."),
        ("FR-06", "Violation Analysis", "Evaluate each worker against configurable safety rules (missing helmet, missing vest, zone intrusion)."),
        ("FR-07", "Alert Debounce", "Suppress duplicate alerts for the same worker and violation type within a configurable cooldown window (default 6 s)."),
        ("FR-08", "Voice Alert Generation", "Convert violation warnings to speech in the configured language (EN, HI, KN, ES) using pyttsx3."),
        ("FR-09", "Safety Recommendations", "Return multilingual corrective-action text for each violation type."),
        ("FR-10", "Local Database Persistence", "Store safety events, rules, and audit log entries in SQLite; support purge by retention period."),
        ("FR-11", "Privacy Safeguards", "Blur worker faces before display/storage; never store raw video; never transmit to cloud."),
        ("FR-12", "MJPEG Live Stream", "Encode annotated frames as MJPEG and serve via HTTP for browser-based live monitoring."),
        ("FR-13", "REST API", "Expose 14 endpoints for system control, data retrieval, configuration, and privacy auditing."),
        ("FR-14", "Web Dashboard", "Provide 7 React pages: Dashboard, Live Monitoring, Alerts, History, Analytics, Safety Info, Settings."),
    ]
    func_data = [["ID", "Requirement", "Description"]]
    for fid, fname, fdesc in func_items:
        func_data.append([fid, fname, Paragraph(fdesc, ss["TableCell"])])
    story.append(tbl(func_data, [1.5*cm, 3.5*cm, 10.5*cm]))
    story.append(Paragraph("Table 6.5 -- Functional requirements specification.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.1.6  Non-Functional Requirements ──────────────────────────────
    story.append(Paragraph("6.1.6  Non-Functional Requirements", ss["SubSection"]))
    story.append(sp(0.2))
    nfr_items = [
        ("NFR-01", "Latency", "End-to-end frame-to-alert latency < 200 ms on dev machine (CPU); < 400 ms on Raspberry Pi 4."),
        ("NFR-02", "Throughput", ">= 10 FPS on dev machine; >= 2.5 FPS on Raspberry Pi 4."),
        ("NFR-03", "Privacy", "No raw video storage; no cloud transmission; facial anonymisation; GDPR data-minimisation principles."),
        ("NFR-04", "Availability", "Autostart via systemd; graceful restart on crash; UPS-recommended power."),
        ("NFR-05", "Maintainability", "Modular backend (9 independent packages); all dependencies pinned; documented REST API."),
        ("NFR-06", "Portability", "Runs on Windows (dev), Linux ARM64 (Pi 4), and any Chromium-based browser (frontend)."),
    ]
    nfr_data = [["ID", "Quality Attribute", "Requirement"]]
    for nid, nattr, ndesc in nfr_items:
        nfr_data.append([nid, nattr, Paragraph(ndesc, ss["TableCell"])])
    story.append(tbl(nfr_data, [1.5*cm, 3*cm, 11*cm]))
    story.append(Paragraph("Table 6.6 -- Non-functional requirements.", ss["Caption"]))

    story.append(PageBreak())


# ────────────────────────────────────────────────────────────────────────
#  6.2  ABOUT ALGORITHM
# ────────────────────────────────────────────────────────────────────────
def build_section_6_2(ss, story):
    story.append(Paragraph("6.2  About Algorithm", ss["SectionTitle"]))
    story.append(hr(ss))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The core intelligence of the system is a multi-stage edge AI pipeline that "
        "processes each video frame through a sequence of well-defined algorithmic "
        "steps. This section describes each algorithm in detail, including its inputs, "
        "outputs, computational complexity, and implementation rationale.",
        ss["BodyJ"]))
    story.append(sp(0.4))

    # ── 6.2.1  Overall Pipeline Algorithm ────────────────────────────────
    story.append(Paragraph("6.2.1  Edge Safety Detection Pipeline (Main Algorithm)", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The main processing loop runs as a background daemon thread "
        "(VideoProcessor._processing_loop). Each iteration performs the following steps:",
        ss["BodyJ"]))
    story.append(sp(0.2))

    steps = [
        ("Step 1: Frame Capture",
         "Read the next BGR frame from the active camera source (USB webcam, uploaded "
         "video file, or synthetic scene generator). If no frame is available (camera "
         "disconnected or end-of-video), sleep 50 ms and retry. The synthetic mode "
         "generates animated construction-site scenes for demonstration when no "
         "physical camera is attached."),

        ("Step 2: CLAHE Contrast Enhancement",
         "Convert the BGR frame to LAB colour space. Apply Contrast-Limited Adaptive "
         "Histogram Equalisation (CLAHE) with clipLimit=2.0 and tileGridSize=(8, 8) "
         "to the L (luminance) channel. Merge back and convert to BGR. This improves "
         "detection robustness under variable outdoor construction lighting. "
         "Time complexity: O(W x H) where W, H are frame dimensions."),

        ("Step 3: YOLOv8 Object Detection",
         "Pass the enhanced frame to the YOLOv8n model via ultralytics predict() with "
         "confidence threshold 0.40, IoU threshold 0.45, and input size 640x640. The "
         "model returns bounding boxes, class IDs, and confidence scores. 'person' / "
         "'worker' detections are classified as workers; 'helmet', 'hardhat', 'vest', "
         "'jacket' detections are classified as equipment. Inference complexity: "
         "O(N) where N = number of grid cells x anchors (architecture-dependent)."),

        ("Step 4: HSV Anatomical PPE Verification",
         "When the YOLO model detects workers but no PPE classes (as with the generic "
         "COCO-trained YOLOv8n), a colour-based verification algorithm activates:\n"
         "a) Head Region (top 25% of worker box): Convert to HSV. Apply inRange() "
         "masks for yellow [20,80,100]-[35,255,255], orange [5,120,120]-[18,255,255], "
         "and white [0,0,190]-[180,40,255] helmets. If the combined mask ratio exceeds "
         "0.14, a 'safety-helmet' detection is emitted.\n"
         "b) Torso Region (25%-70% of worker box): Apply HSV masks for yellow vest "
         "[22,90,100]-[40,255,255] and orange vest [6,120,110]-[19,255,255]. If the "
         "combined ratio exceeds 0.18, a 'safety-vest' detection is emitted.\n"
         "Time complexity: O(W_r x H_r) per worker, where W_r, H_r are region "
         "dimensions."),

        ("Step 5: PPE-Worker Association",
         "For each detected PPE item, compute the Intersection-over-Union (IoU) "
         "and containment ratio with every worker bounding box. Assign the PPE to "
         "the worker with the highest IoU (minimum threshold: 0.1). Each worker's "
         "record is updated with boolean flags has_helmet and has_vest. "
         "Time complexity: O(W x E) where W = workers, E = equipment items."),

        ("Step 6: Safety Violation Analysis",
         "For each worker, evaluate against the active safety rule set:\n"
         "Rule 1: If has_helmet is False -> MISSING_HELMET (severity: HIGH)\n"
         "Rule 2: If has_vest is False -> MISSING_VEST (severity: MEDIUM)\n"
         "Rule 3: If worker bounding box overlaps a restricted zone (normalised "
         "coordinates) -> RESTRICTED_ZONE_INTRUSION (severity: CRITICAL)\n"
         "Each violation is checked against the debounce cache: if the same "
         "(worker_id, violation_type) pair was alerted within the cooldown window "
         "(default 6 seconds), the alert is suppressed to prevent alarm fatigue."),

        ("Step 7: Alert Dispatch and Database Persistence",
         "Violations with trigger_alert=True are: (a) pushed into a ring-buffer "
         "alert queue (capacity: 50); (b) inserted into the SQLite safety_events "
         "table with violation type, severity, confidence, recommendation, and UTC "
         "timestamp; (c) dispatched to the voice TTS engine for spoken alert."),

        ("Step 8: Privacy Guard - Facial Blur",
         "If BLUR_FACES_IN_EVENTS is enabled (default: True), the top 28% of each "
         "worker bounding box (head region) is Gaussian-blurred with a dynamically "
         "sized kernel (ksize = max(15, region_width/3 | 1), sigma=30). This ensures "
         "no identifiable facial biometrics appear in the MJPEG stream or any stored "
         "frame."),

        ("Step 9: Safety Annotation Overlay",
         "Draw visual overlays on the frame: red-tinted semi-transparent rectangles "
         "for restricted zones; green bounding boxes for compliant workers; red "
         "bounding boxes with violation labels for non-compliant workers; teal/orange "
         "boxes for detected equipment items with confidence percentages. FPS and "
         "latency counters are overlaid in the top-right corner."),

        ("Step 10: MJPEG Encoding and Streaming",
         "Encode the annotated frame as JPEG (quality=80) and store in a thread-safe "
         "buffer. The /api/v1/stream endpoint reads this buffer and delivers a "
         "multipart/x-mixed-replace MJPEG stream to the browser. The loop then "
         "sleeps for max(10 ms, 1/TARGET_FPS - elapsed) to pace at ~15 FPS."),
    ]

    for title, body in steps:
        story.append(Paragraph(title, ss["StepNum"]))
        story.append(Paragraph(body.replace("\n", "<br/>"), ss["StepBody"]))

    story.append(sp(0.4))

    # ── 6.2.2  YOLOv8 Detection Algorithm ────────────────────────────────
    story.append(Paragraph("6.2.2  YOLOv8 Object Detection Algorithm", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "YOLOv8 (You Only Look Once, version 8) is a single-stage, anchor-free object "
        "detection architecture developed by Ultralytics. The system uses the YOLOv8n "
        "(nano) variant, selected for its optimal balance between accuracy and inference "
        "speed on resource-constrained edge hardware.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    story.append(Paragraph("Architecture Components:", ss["SubSubSection"]))
    yolo_arch = [
        ("Backbone (CSPDarknet53)", "Extracts hierarchical feature maps from the input image "
         "using cross-stage partial connections that reduce computation while maintaining "
         "gradient flow."),
        ("Neck (PANet + FPN)", "Aggregates features at multiple scales via a Path Aggregation "
         "Network and Feature Pyramid Network, enabling detection of both large (workers) "
         "and small (helmets) objects."),
        ("Head (Decoupled)", "Separate classification and regression heads predict class "
         "probabilities and bounding-box coordinates independently, improving convergence."),
        ("Loss Function", "CIoU (Complete IoU) for bounding-box regression; Binary "
         "Cross-Entropy for classification; Distribution Focal Loss for objectness."),
        ("Post-Processing", "Non-Maximum Suppression (NMS) with IoU threshold 0.45 removes "
         "overlapping detections."),
    ]
    for name, desc in yolo_arch:
        story.append(Paragraph(f"<b>{name}:</b> {desc}", ss["BulletItem"], bulletText="\u2022"))

    story.append(sp(0.3))
    story.append(Paragraph("YOLOv8n Model Specifications:", ss["SubSubSection"]))
    yolo_spec_data = [
        ["Parameter",              "Value"],
        ["Input Resolution",       "640 x 640 px (letterboxed)"],
        ["Parameters",             "3.2 million"],
        ["FLOPs",                  "8.7 billion"],
        ["mAP@0.5 (COCO)",        "37.3%"],
        ["Model File Size",       "6.3 MB (.pt)"],
        ["ONNX Exported Size",    "~12 MB (.onnx, FP32)"],
        ["INT8 Quantised Size",   "~3 MB (estimated)"],
    ]
    story.append(tbl(yolo_spec_data, [5*cm, 10.5*cm]))
    story.append(Paragraph("Table 6.7 -- YOLOv8n model specifications.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.2.3  HSV PPE Verification Algorithm ────────────────────────────
    story.append(Paragraph("6.2.3  HSV Colour-Based PPE Verification Algorithm", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "Since the generic COCO-trained YOLOv8n model does not contain 'helmet' or 'vest' "
        "as native classes, the system implements a supplementary colour-based PPE "
        "verification algorithm that operates on anatomically segmented worker regions.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    story.append(Paragraph("Pseudocode:", ss["SubSubSection"]))
    pseudo = """\
FUNCTION verify_ppe(frame, worker_boxes):
    hsv_frame = BGR_to_HSV(frame)
    FOR EACH worker IN worker_boxes:
        box = worker.bounding_box
        head_region = box[y1 : y1 + 0.25*height, x1 : x2]
        torso_region = box[y1 + 0.25*height : y1 + 0.70*height, x1 : x2]

        // HELMET CHECK
        yellow_mask = inRange(head_region, [20,80,100], [35,255,255])
        orange_mask = inRange(head_region, [5,120,120], [18,255,255])
        white_mask  = inRange(head_region, [0,0,190],   [180,40,255])
        helmet_ratio = count_nonzero(OR(yellow, orange, white)) / area
        IF helmet_ratio > 0.14:
            EMIT detection("safety-helmet", confidence=0.65+ratio)

        // VEST CHECK
        vest_yellow = inRange(torso_region, [22,90,100], [40,255,255])
        vest_orange = inRange(torso_region, [6,120,110], [19,255,255])
        vest_ratio = count_nonzero(OR(vest_yellow, vest_orange)) / area
        IF vest_ratio > 0.18:
            EMIT detection("safety-vest", confidence=0.60+ratio)
    RETURN equipment_list"""
    story.append(Paragraph(pseudo.replace("\n", "<br/>").replace(" ", "&nbsp;"),
                            ss["CodeBlock"]))
    story.append(sp(0.2))

    hsv_data = [
        ["PPE Item",      "Region",         "HSV Lower Bound", "HSV Upper Bound", "Min Ratio"],
        ["Yellow Helmet",  "Head (top 25%)", "[20, 80, 100]",   "[35, 255, 255]",  "0.14"],
        ["Orange Helmet",  "Head (top 25%)", "[5, 120, 120]",   "[18, 255, 255]",  "0.14"],
        ["White Helmet",   "Head (top 25%)", "[0, 0, 190]",     "[180, 40, 255]",  "0.14"],
        ["Yellow Vest",    "Torso (25-70%)", "[22, 90, 100]",   "[40, 255, 255]",  "0.18"],
        ["Orange Vest",    "Torso (25-70%)", "[6, 120, 110]",   "[19, 255, 255]",  "0.18"],
    ]
    story.append(tbl(hsv_data, [2.8*cm, 2.8*cm, 3*cm, 3*cm, 2*cm]))
    story.append(Paragraph("Table 6.8 -- HSV colour thresholds for PPE verification.", ss["Caption"]))
    story.append(sp(0.4))

    # ── 6.2.4  Alert Debounce Algorithm ──────────────────────────────────
    story.append(Paragraph("6.2.4  Alert Debounce Algorithm", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "To prevent alarm fatigue from continuous violations, the system implements a "
        "per-worker, per-violation-type debounce mechanism. The algorithm maintains a "
        "hash map of (worker_id, violation_type) -> last_alert_timestamp. A new alert "
        "is triggered only when the elapsed time exceeds the configurable cooldown "
        "period (default: 6 seconds).",
        ss["BodyJ"]))
    story.append(sp(0.2))

    debounce_pseudo = """\
FUNCTION should_trigger_alert(worker_id, violation_type, current_time):
    key = (worker_id, violation_type)
    last_time = debounce_cache.get(key, 0)
    IF (current_time - last_time) >= COOLDOWN_SECONDS:
        debounce_cache[key] = current_time
        RETURN True
    RETURN False"""
    story.append(Paragraph(debounce_pseudo.replace("\n", "<br/>").replace(" ", "&nbsp;"),
                            ss["CodeBlock"]))
    story.append(sp(0.4))

    # ── 6.2.5  Privacy-Preserving Facial Blur Algorithm ──────────────────
    story.append(Paragraph("6.2.5  Privacy-Preserving Facial Anonymisation Algorithm", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The privacy module applies Gaussian blur to the estimated head region (top 28% "
        "of each worker bounding box) with a dynamically computed kernel size. This "
        "ensures anonymisation without requiring a dedicated face-detection model, "
        "reducing computational overhead on edge hardware.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    blur_pseudo = """\
FUNCTION apply_face_blur(frame, workers):
    FOR EACH worker IN workers:
        box = worker.bounding_box
        head_y2 = box.y1 + 0.28 * (box.y2 - box.y1)
        face_roi = frame[box.y1 : head_y2, box.x1 : box.x2]
        ksize = max(15, (face_roi.width / 3) | 1)   // ensure odd
        blurred = GaussianBlur(face_roi, (ksize, ksize), sigma=30)
        frame[box.y1 : head_y2, box.x1 : box.x2] = blurred
    RETURN frame"""
    story.append(Paragraph(blur_pseudo.replace("\n", "<br/>").replace(" ", "&nbsp;"),
                            ss["CodeBlock"]))
    story.append(sp(0.4))

    # ── 6.2.6  Synthetic Worker Detection Algorithm ──────────────────────
    story.append(Paragraph("6.2.6  Synthetic Worker Detection (Demonstration Mode)", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "When no physical camera is connected, the system generates animated "
        "construction-site scenes and detects worker positions using skin-tone "
        "contour analysis. This enables full-pipeline demonstration without "
        "hardware dependencies.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    synth_pseudo = """\
FUNCTION detect_synthetic_workers(frame):
    hsv = BGR_to_HSV(frame)
    skin_mask = inRange(hsv, [8, 50, 130], [25, 180, 240])
    contours = findContours(skin_mask, RETR_EXTERNAL)
    workers = []
    FOR EACH contour IN contours:
        area = contourArea(contour)
        IF 150 < area < 1500:
            (hx, hy, hw, hh) = boundingRect(contour)
            cx, cy = hx + hw/2, hy + hh/2
            worker_box = extrapolate_body(cx, cy, width=56, height=175)
            workers.append(worker_box)
    equipment = verify_ppe(frame, workers)   // reuse HSV PPE algorithm
    RETURN workers, equipment"""
    story.append(Paragraph(synth_pseudo.replace("\n", "<br/>").replace(" ", "&nbsp;"),
                            ss["CodeBlock"]))
    story.append(sp(0.3))

    # ── 6.2.7  Complexity Summary ────────────────────────────────────────
    story.append(Paragraph("6.2.7  Computational Complexity Summary", ss["SubSection"]))
    story.append(sp(0.2))

    complex_data = [
        ["Algorithm Stage",          "Time Complexity",     "Dominant Factor"],
        ["CLAHE Enhancement",        "O(W x H)",            "Frame pixel count"],
        ["YOLOv8n Inference",        "O(N)",                "Grid cells x anchors (fixed by architecture)"],
        ["HSV PPE Verification",     "O(K x W_r x H_r)",   "K workers x region pixel area"],
        ["PPE-Worker Association",   "O(K x E)",            "K workers x E equipment items"],
        ["Violation Analysis",       "O(K x R)",            "K workers x R rules"],
        ["Alert Debounce",           "O(1) amortised",      "Hash-map lookup"],
        ["Facial Blur",              "O(K x W_f x H_f)",   "K workers x face region area"],
        ["JPEG Encoding",            "O(W x H)",            "Output frame pixels"],
    ]
    story.append(tbl(complex_data, [4*cm, 3.5*cm, 8*cm]))
    story.append(Paragraph("Table 6.9 -- Computational complexity of each pipeline stage.", ss["Caption"]))

    story.append(PageBreak())


# ────────────────────────────────────────────────────────────────────────
#  6.3  ABOUT FLOWCHART
# ────────────────────────────────────────────────────────────────────────
def build_section_6_3(ss, story):
    story.append(Paragraph("6.3  About Flowchart", ss["SectionTitle"]))
    story.append(hr(ss))
    story.append(sp(0.2))
    story.append(Paragraph(
        "This section presents three flowcharts that together describe the complete "
        "data and control flow of the Edge-Enabled Privacy-Preserving Construction "
        "Safety System. Each flowchart corresponds to a different abstraction level: "
        "(1) the high-level system processing loop, (2) the internal edge pipeline "
        "module interconnections, and (3) the frontend-backend data flow architecture.",
        ss["BodyJ"]))
    story.append(sp(0.5))

    # ── Flowchart 1 ──────────────────────────────────────────────────────
    story.append(Paragraph("6.3.1  System Processing Flowchart", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "Figure 6.1 illustrates the main system processing loop from camera input "
        "through AI detection, safety analysis, voice alert generation, database "
        "storage, and privacy-guarded frame annotation. The loop continues until "
        "monitoring is explicitly stopped by the operator via the dashboard.",
        ss["BodyJ"]))
    story.append(sp(0.3))

    fc1 = generate_system_flowchart()
    story.append(fc1)
    story.append(Paragraph(
        "Figure 6.1 -- System processing flowchart: Camera input through detection, "
        "analysis, alerting, and privacy-guarded output. Green arrows indicate the "
        "'No violation' and loop-back paths.", ss["Caption"]))
    story.append(PageBreak())

    # ── Flowchart 2 ──────────────────────────────────────────────────────
    story.append(Paragraph("6.3.2  Edge Processing Pipeline Flowchart", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "Figure 6.2 shows the internal module-level pipeline within the backend. "
        "Frames flow left-to-right through capture and enhancement, then right-to-left "
        "through AI detection and alert generation, and finally left-to-right again "
        "through privacy guard and browser streaming. The SQLite database receives "
        "events as a side-channel from the Violation Analyser.",
        ss["BodyJ"]))
    story.append(sp(0.3))

    fc2 = generate_edge_pipeline_flowchart()
    story.append(fc2)
    story.append(Paragraph(
        "Figure 6.2 -- Edge processing pipeline: module-level data flow with colour-coded "
        "functional categories (blue = camera/stream, orange = AI, red = alerts, green = "
        "privacy/storage).", ss["Caption"]))
    story.append(sp(0.5))

    # ── Flowchart 3 ──────────────────────────────────────────────────────
    story.append(Paragraph("6.3.3  Frontend-Backend Data Flow Diagram", ss["SubSection"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "Figure 6.3 depicts the separation of concerns between the React frontend, "
        "the FastAPI REST API layer, and the backend processing modules. All data "
        "exchange occurs over HTTP on the local network. No direct database access or "
        "AI computation exists in the frontend. The bottom row shows the edge hardware "
        "peripherals accessed exclusively by the backend.",
        ss["BodyJ"]))
    story.append(sp(0.3))

    fc3 = generate_data_flow_flowchart()
    story.append(fc3)
    story.append(Paragraph(
        "Figure 6.3 -- Frontend-backend data flow architecture. Bidirectional Axios/HTTP "
        "communication over local LAN. All processing remains on the edge device.",
        ss["Caption"]))
    story.append(sp(0.5))

    # ── Flowchart Descriptions Table ─────────────────────────────────────
    story.append(Paragraph("6.3.4  Flowchart Symbol Legend", ss["SubSection"]))
    story.append(sp(0.2))
    legend_data = [
        ["Symbol",               "Shape",      "Meaning"],
        ["Rounded Rectangle",   "Process",     "A processing step or module execution"],
        ["Diamond",             "Decision",    "Conditional branch (Yes/No evaluation)"],
        ["Arrow",               "Flow",        "Direction of data or control flow"],
        ["Colour: Navy/Blue",   "---",         "Core processing or stream modules"],
        ["Colour: Orange",      "---",         "AI detection and inference modules"],
        ["Colour: Red",         "---",         "Violation detection and alert modules"],
        ["Colour: Green",       "---",         "Privacy guard and local storage modules"],
        ["Colour: Grey",        "---",         "Terminal states (Start / Stop)"],
    ]
    story.append(tbl(legend_data, [3.5*cm, 3*cm, 9*cm]))
    story.append(Paragraph("Table 6.10 -- Flowchart symbol and colour legend.", ss["Caption"]))


# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    ss = build_styles()
    story = []

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=2.0*cm,  bottomMargin=1.6*cm,
        title="SIT Construction Safety System -- Chapter 6: Software Requirements, Algorithm & Flowchart",
        author="SIT Tumakuru Mini-Project Team 2026-27",
    )

    build_cover(ss, story)
    build_section_6_1(ss, story)
    build_section_6_2(ss, story)
    build_section_6_3(ss, story)

    def on_page(canvas, doc):
        if doc.page > 1:
            _page_decor(canvas, doc)

    doc.build(story, onFirstPage=_first_page, onLaterPages=on_page)

    size_kb = OUTPUT.stat().st_size // 1024
    print(f"PDF generated successfully!")
    print(f"Location : {OUTPUT}")
    print(f"Size     : {size_kb} KB")


if __name__ == "__main__":
    main()
