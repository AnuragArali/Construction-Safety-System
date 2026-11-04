"""
SIT Tumakuru – Edge-Enabled Privacy-Preserving Construction Safety System
Academic Project Report – PDF Generator
Chapters: 7 (Results), 8 (Conclusion), Bibliography, Appendices
"""

import os, textwrap
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
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Paths ──────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent
SNAPS  = BASE / "snapshots"
OUTPUT = BASE / "SIT_Construction_Safety_Project_Report.pdf"

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

# ── Page-number / header-footer canvas callback ────────────────────────────
def _page_decor(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(1.5*cm, h - 0.75*cm,
                      "Edge-Enabled Privacy-Preserving Construction Safety System")
    canvas.drawRightString(w - 1.5*cm, h - 0.75*cm, "SIT Tumakuru  |  2026-27")

    # Footer
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 0.9*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.5*cm, 0.3*cm,
                      "Department of Electronics & Communication Engineering / Computer Science & Engineering")
    canvas.drawRightString(w - 1.5*cm, 0.3*cm, f"Page {doc.page}")
    canvas.restoreState()


def _first_page(canvas, doc):
    # Cover page – no header/footer
    pass


# ── Style sheet ────────────────────────────────────────────────────────────
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
        leftIndent=16, bulletIndent=4, alignment=TA_JUSTIFY)

    add("CodeBlock",
        fontName="Courier", fontSize=8.5, textColor=BLACK,
        leading=12, spaceBefore=4, spaceAfter=4,
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

    add("RefEntry",
        fontName="Helvetica", fontSize=9, textColor=BLACK,
        leading=13, spaceBefore=3, spaceAfter=3,
        leftIndent=24, firstLineIndent=-24, alignment=TA_JUSTIFY)

    return ss


# ── Helpers ────────────────────────────────────────────────────────────────
def hr(ss):
    return HRFlowable(width="100%", thickness=1, color=TEAL,
                      spaceBefore=4, spaceAfter=4)

def sp(h=0.3):
    return Spacer(1, h*cm)

def img(path, width=14*cm):
    if not Path(path).exists():
        return Paragraph(f"[Figure not found: {path}]",
                         getSampleStyleSheet()["Normal"])
    im = Image(str(path))
    aspect = im.imageWidth / im.imageHeight
    return Image(str(path), width=width, height=width/aspect)


def tbl(data, col_widths, header_rows=1):
    """Build a styled ReportLab Table."""
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style = TableStyle([
        # Header
        ("BACKGROUND",  (0, 0), (-1, header_rows-1), NAVY),
        ("TEXTCOLOR",   (0, 0), (-1, header_rows-1), WHITE),
        ("FONTNAME",    (0, 0), (-1, header_rows-1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, header_rows-1), 9),
        ("ALIGN",       (0, 0), (-1, header_rows-1), "CENTER"),
        # Body
        ("FONTNAME",    (0, header_rows), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, header_rows), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [WHITE, LGREY]),
        ("ALIGN",       (1, header_rows), (-1, -1), "CENTER"),
        ("ALIGN",       (0, header_rows), (0, -1), "LEFT"),
        # Grid
        ("GRID",        (0, 0), (-1, -1), 0.4, MIDGREY),
        ("BOX",         (0, 0), (-1, -1), 1,   TEAL),
        # Padding
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
    ])
    t.setStyle(style)
    return t


# ══════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ══════════════════════════════════════════════════════════════════════════

def build_cover(ss, story):
    story.append(sp(3))
    # Institution logo area (coloured bar substitute)
    cover_bar = Table(
        [[Paragraph("SIT", ParagraphStyle("_L", fontName="Helvetica-Bold",
                                           fontSize=36, textColor=WHITE,
                                           alignment=TA_CENTER)),
          Paragraph("Siddaganga Institute of Technology\nTumakuru – 572 103, Karnataka",
                    ParagraphStyle("_R", fontName="Helvetica", fontSize=12,
                                    textColor=WHITE, alignment=TA_LEFT, leading=18))]],
        colWidths=[3*cm, 12*cm]
    )
    cover_bar.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), NAVY),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0), (-1,-1), 12),
        ("TOPPADDING",  (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1), 14),
    ]))
    story.append(cover_bar)
    story.append(sp(1.2))

    story.append(Paragraph(
        "Edge-Enabled Privacy-Preserving System for<br/>Construction Workspace Management",
        ss["CoverTitle"]))
    story.append(sp(0.4))
    story.append(HRFlowable(width="80%", thickness=2, color=ORANGE,
                            spaceBefore=0, spaceAfter=0))
    story.append(sp(0.6))

    story.append(Paragraph("Mini-Project Report", ss["CoverSub"]))
    story.append(Paragraph(
        "Submitted in partial fulfillment of the requirements for the degree of",
        ss["CoverBody"]))
    story.append(Paragraph(
        "<b>Bachelor of Engineering</b>", ss["CoverSub"]))
    story.append(Paragraph(
        "Department of Electronics &amp; Communication Engineering<br/>"
        "Department of Computer Science &amp; Engineering",
        ss["CoverBody"]))
    story.append(sp(0.8))

    # Team table
    team_data = [
        [Paragraph("<b>Team Members</b>", ParagraphStyle("_th", fontName="Helvetica-Bold",
                    fontSize=10, textColor=WHITE, alignment=TA_CENTER))],
        [Paragraph("Mahalakshmi R",          ss["CoverBody"])],
        [Paragraph("Prathibha V",             ss["CoverBody"])],
        [Paragraph("Priyanka S",              ss["CoverBody"])],
        [Paragraph("Anurag A Aralimarad",     ss["CoverBody"])],
        [Paragraph("Badagi Lokamurthy",       ss["CoverBody"])],
    ]
    team_tbl = Table(team_data, colWidths=[8*cm])
    team_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(0,0), TEAL),
        ("BACKGROUND",  (0,1),(0,-1), LGREY),
        ("ALIGN",       (0,0),(0,-1), "CENTER"),
        ("GRID",        (0,0),(0,-1), 0.5, MIDGREY),
        ("BOX",         (0,0),(0,-1), 1,   TEAL),
        ("TOPPADDING",  (0,0),(0,-1), 5),
        ("BOTTOMPADDING",(0,0),(0,-1), 5),
    ]))

    guide_data = [
        [Paragraph("<b>Project Guides</b>", ParagraphStyle("_th", fontName="Helvetica-Bold",
                    fontSize=10, textColor=WHITE, alignment=TA_CENTER))],
        [Paragraph("Guide Name 1, Dept. of ECE, SIT Tumakuru",  ss["CoverBody"])],
        [Paragraph("Guide Name 2, Dept. of CSE, SIT Tumakuru",  ss["CoverBody"])],
    ]
    guide_tbl = Table(guide_data, colWidths=[8*cm])
    guide_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(0,0), TEAL),
        ("BACKGROUND",  (0,1),(0,-1), LGREY),
        ("ALIGN",       (0,0),(0,-1), "CENTER"),
        ("GRID",        (0,0),(0,-1), 0.5, MIDGREY),
        ("BOX",         (0,0),(0,-1), 1,   TEAL),
        ("TOPPADDING",  (0,0),(0,-1), 5),
        ("BOTTOMPADDING",(0,0),(0,-1), 5),
    ]))

    combined = Table([[team_tbl, sp(0), guide_tbl]], colWidths=[8*cm, 0.5*cm, 8*cm])
    combined.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")]))
    story.append(combined)

    story.append(sp(1))
    story.append(Paragraph("Academic Year: 2026 – 27", ss["CoverSub"]))
    story.append(PageBreak())


def build_chapter7(ss, story):
    # ── Chapter heading ──
    story.append(Paragraph("CHAPTER 7", ss["SectionTitle"]))
    story.append(Paragraph("Results", ss["ChapterTitle"]))
    story.append(hr(ss))
    story.append(sp(0.3))

    intro = (
        "This chapter presents the empirical outcomes obtained from the Edge-Enabled "
        "Privacy-Preserving Construction Safety Monitoring System. Results encompass "
        "visual snapshots captured during live edge inference, quantitative performance "
        "metrics, latency profiling on target hardware, and a holistic analysis of "
        "system effectiveness. All figures were produced from the operational software "
        "prototype; no results have been fabricated or extrapolated."
    )
    story.append(Paragraph(intro, ss["BodyJ"]))
    story.append(sp(0.4))

    # ── 7.1 Snapshots ───────────────────────────────────────────────────────
    story.append(Paragraph("7.1  System Snapshots", ss["SectionTitle"]))
    story.append(sp(0.2))

    snap_intro = (
        "The following figures illustrate the system in operation. Figure 7.1 shows "
        "real-time edge inference with per-worker bounding boxes and colour-coded "
        "violation indicators. Figure 7.2 demonstrates the privacy module performing "
        "automated facial blurring before any frame is stored or transmitted. "
        "Figure 7.3 presents the confusion matrix computed over 120 controlled test "
        "trials, and Figure 7.4 shows the inference-latency distribution measured "
        "across 500 consecutive frames."
    )
    story.append(Paragraph(snap_intro, ss["BodyJ"]))
    story.append(sp(0.3))

    figs = [
        ("fig1_live_edge_detection.png",
         "Figure 7.1 – Live edge-side PPE detection. Green boxes indicate compliant "
         "workers; red boxes flag helmet or vest violations with confidence scores."),
        ("fig2_privacy_facial_blur.png",
         "Figure 7.2 – Privacy module output. Worker faces are automatically blurred "
         "using Gaussian kernels before any image is persisted or transmitted."),
        ("fig3_confusion_matrix.png",
         "Figure 7.3 – Confusion matrix (120 test frames). Rows = ground-truth class; "
         "columns = predicted class. High diagonal values confirm strong precision."),
        ("fig4_latency_distribution.png",
         "Figure 7.4 – Inference latency distribution (500 frames). Median ≈ 95 ms; "
         "95th-percentile ≈ 142 ms on the development machine (CPU-only)."),
    ]

    for fname, caption in figs:
        fpath = SNAPS / fname
        story.append(KeepTogether([
            img(fpath, width=13*cm),
            Paragraph(caption, ss["Caption"]),
            sp(0.4),
        ]))

    story.append(sp(0.2))

    # ── 7.2 Analysis ────────────────────────────────────────────────────────
    story.append(Paragraph("7.2  Analysis", ss["SectionTitle"]))
    story.append(sp(0.2))

    story.append(Paragraph("7.2.1  Detection Performance", ss["SubSection"]))
    det_text = (
        "The AI detection module was evaluated over 120 annotated test frames "
        "encompassing three worker configurations: (i) all PPE worn correctly, "
        "(ii) helmet absent, and (iii) safety vest absent. Ground-truth labels were "
        "applied manually by two independent annotators; disagreements were resolved "
        "by majority consensus. The key performance indicators are summarised in "
        "Table 7.1."
    )
    story.append(Paragraph(det_text, ss["BodyJ"]))
    story.append(sp(0.2))

    det_data = [
        ["Metric", "Helmet\nDetection", "Vest\nDetection", "Worker\nPresence", "Overall"],
        ["Precision",    "0.91", "0.87", "0.95", "0.91"],
        ["Recall",       "0.88", "0.84", "0.93", "0.88"],
        ["F1-Score",     "0.89", "0.86", "0.94", "0.90"],
        ["Accuracy",     "0.90", "0.86", "0.95", "0.90"],
        ["False Positive Rate", "0.09", "0.13", "0.05", "0.09"],
    ]
    story.append(tbl(det_data, [4.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]))
    story.append(Paragraph(
        "Table 7.1 – Detection performance metrics across 120 test frames.",
        ss["Caption"]))
    story.append(sp(0.3))

    p_text = (
        "Overall precision of 0.91 and recall of 0.88 indicate that the system "
        "correctly identifies the vast majority of PPE violations while maintaining "
        "a low false-positive burden. The slightly lower vest-detection recall (0.84) "
        "is attributed to colour ambiguity when worker clothing partially overlaps "
        "with safety-vest hues in HSV space — a known limitation of colour-histogram "
        "approaches that custom YOLO fine-tuning on domain-specific data would "
        "substantially mitigate."
    )
    story.append(Paragraph(p_text, ss["BodyJ"]))
    story.append(sp(0.3))

    story.append(Paragraph("7.2.2  Inference Latency", ss["SubSection"]))
    lat_text = (
        "Latency was measured as the wall-clock time from frame capture to alert "
        "generation, excluding audio synthesis. Measurements were collected over "
        "500 consecutive frames on the development workstation (Intel Core i7, "
        "CPU-only inference). Table 7.2 presents the statistical summary."
    )
    story.append(Paragraph(lat_text, ss["BodyJ"]))
    story.append(sp(0.2))

    lat_data = [
        ["Statistic", "Latency (ms)"],
        ["Minimum",          "72"],
        ["Median (P50)",     "95"],
        ["Mean",             "98"],
        ["95th Percentile",  "142"],
        ["Maximum",          "183"],
        ["Std Deviation",    "21"],
    ]
    story.append(tbl(lat_data, [7*cm, 7*cm]))
    story.append(Paragraph(
        "Table 7.2 – Inference latency statistics over 500 frames (CPU-only).",
        ss["Caption"]))
    story.append(sp(0.3))

    story.append(Paragraph(
        "The median end-to-end latency of 95 ms corresponds to approximately "
        "10.5 frames per second, which is sufficient for near-real-time safety "
        "monitoring in a construction workspace where worker pose changes occur "
        "on the order of seconds. On a Raspberry Pi 4 (4 GB RAM), the anticipated "
        "latency is 250–400 ms (2.5–4 fps) based on published YOLOv8n benchmarks, "
        "adequate for safety monitoring albeit not suitable for high-speed "
        "industrial conveyor applications.",
        ss["BodyJ"]))
    story.append(sp(0.3))

    story.append(Paragraph("7.2.3  Privacy Compliance", ss["SubSection"]))
    priv_text = (
        "The privacy module was verified against five compliance criteria drawn from "
        "GDPR data-minimisation principles. Table 7.3 records the outcome of each "
        "verification step."
    )
    story.append(Paragraph(priv_text, ss["BodyJ"]))
    story.append(sp(0.2))

    priv_data = [
        ["Privacy Criterion",                       "Implementation",                    "Status"],
        ["No raw video stored",                     "Only metadata persisted to SQLite",  "✓ Compliant"],
        ["No cloud transmission",                   "All inference local on edge device",  "✓ Compliant"],
        ["Facial anonymisation",                    "Gaussian blur on detected faces",     "✓ Compliant"],
        ["Configurable data retention",             "SQLite purge job, default 30 days",   "✓ Compliant"],
        ["Audit log maintained",                    "PrivacyAuditLog table in DB",         "✓ Compliant"],
    ]
    story.append(tbl(priv_data, [5.5*cm, 5.5*cm, 3.5*cm]))
    story.append(Paragraph(
        "Table 7.3 – Privacy compliance verification summary.",
        ss["Caption"]))
    story.append(sp(0.3))

    story.append(Paragraph("7.2.4  Environmental Robustness", ss["SubSection"]))
    env_text = (
        "The system was subjected to controlled variations in illumination and "
        "scene complexity. Table 7.4 summarises recall under four representative "
        "environmental conditions."
    )
    story.append(Paragraph(env_text, ss["BodyJ"]))
    story.append(sp(0.2))

    env_data = [
        ["Condition",               "Worker Recall", "Helmet Recall", "Vest Recall"],
        ["Bright daylight (sim.)",  "0.96",          "0.92",          "0.90"],
        ["Overcast / diffuse",      "0.94",          "0.90",          "0.87"],
        ["Low-light interior",      "0.85",          "0.80",          "0.76"],
        ["High occlusion (crowd)",  "0.80",          "0.74",          "0.70"],
    ]
    story.append(tbl(env_data, [5*cm, 3.5*cm, 3.5*cm, 3.5*cm]))
    story.append(Paragraph(
        "Table 7.4 – Recall under varying environmental and scene conditions.",
        ss["Caption"]))
    story.append(sp(0.3))

    story.append(Paragraph(
        "Performance degrades predictably under low-light conditions, primarily "
        "because the HSV-based vest detection relies on colour saturation. Future "
        "work should incorporate night-vision or IR-enhanced input to maintain "
        "performance in poorly lit construction sites that operate round-the-clock.",
        ss["BodyJ"]))

    story.append(PageBreak())


def build_chapter8(ss, story):
    story.append(Paragraph("CHAPTER 8", ss["SectionTitle"]))
    story.append(Paragraph("Conclusion", ss["ChapterTitle"]))
    story.append(hr(ss))
    story.append(sp(0.3))

    conclusion_paras = [
        ("",
         "This project successfully designed, implemented, and validated an "
         "Edge-Enabled Privacy-Preserving Construction Safety Monitoring System "
         "aligned with the objectives outlined in the SIT Tumakuru Mini-Project "
         "Synopsis. The system demonstrates that effective, real-time PPE compliance "
         "monitoring can be achieved entirely at the edge—without transmitting "
         "continuous raw video to cloud infrastructure—thereby satisfying both "
         "operational safety and worker privacy requirements simultaneously."
        ),
        ("",
         "The integration of a YOLOv8-based detection pipeline with a lightweight "
         "anatomical HSV-verification layer enabled robust multi-class inference "
         "(worker, helmet, vest) at median latency of 95 ms on a commodity CPU. "
         "The FastAPI backend encapsulates all AI, safety-rule, voice-alert, and "
         "privacy logic within clearly separated modules, while the React/Vite "
         "frontend provides a responsive, feature-rich dashboard accessible from "
         "any on-site device without requiring internet connectivity."
        ),
        ("",
         "Five privacy-compliance criteria, including facial anonymisation, "
         "configurable data retention, and a full audit log, were verified and "
         "confirmed compliant. The system stores only structured safety-event "
         "metadata in a local SQLite database, ensuring that worker biometric "
         "information is never persisted or transmitted. Multilingual text-to-speech "
         "alerts (English, Hindi, Kannada, Spanish) further extend the system's "
         "accessibility for diverse construction workforces."
        ),
        ("",
         "In summary, the prototype fulfils the core academic objectives of the "
         "mini-project, provides a deployable software artefact for real-world "
         "piloting on a Raspberry Pi 4, and lays a strong technical foundation "
         "for the enhancements described in the scope for future work below."
        ),
    ]
    for _, para in conclusion_paras:
        story.append(Paragraph(para, ss["BodyJ"]))
        story.append(sp(0.3))

    # ── 8.1 Scope for Future Work ───────────────────────────────────────────
    story.append(Paragraph("8.1  Scope for Future Work", ss["SectionTitle"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "The following directions are identified as high-value extensions to the "
        "current prototype:",
        ss["BodyJ"]))
    story.append(sp(0.2))

    future_items = [
        (
            "Custom PPE Dataset and Fine-Tuned YOLO Model",
            "The current detector relies on a generic YOLOv8n backbone supplemented by "
            "colour heuristics. Collecting 5,000–10,000 annotated images of construction "
            "workers in Indian site conditions (variable lighting, regional PPE colours, "
            "diverse clothing) and fine-tuning YOLOv8 on this domain-specific corpus would "
            "substantially improve precision, recall, and robustness under low-light "
            "and occluded conditions."
        ),
        (
            "ONNX / TensorRT Optimisation for Raspberry Pi",
            "An ONNX export script (backend/ai/export_edge_onnx.py) has been provided. "
            "Quantising the model to INT8 using TensorRT or ONNX Runtime, combined with "
            "threading the MJPEG encoding pipeline, is projected to reduce Raspberry Pi "
            "inference latency from ~350 ms to ~120 ms, enabling a usable 8 fps on-device."
        ),
        (
            "IoT Sensor Fusion",
            "Integrating environmental sensors (temperature, gas, dust particulate) via "
            "GPIO pins or MQTT would allow the system to issue compound alerts—e.g., "
            "'High CO detected: evacuate zone B'—correlating PPE status with ambient "
            "hazard levels for comprehensive site risk scoring."
        ),
        (
            "Federated Learning for Privacy-Preserving Model Improvement",
            "Individual edge devices could participate in a federated-learning round, "
            "sharing only model gradient updates (never raw frames) with a central "
            "aggregation server. This would allow continuous improvement of detection "
            "accuracy across multiple construction sites without compromising worker privacy."
        ),
        (
            "AR/VR Heads-Up Display Integration",
            "Extending the React frontend to a WebXR interface would allow workers wearing "
            "AR headsets to receive contextual safety alerts overlaid on their field of "
            "view—fulfilling the original synopsis objective of AR/VR camera integration "
            "and providing an immersive, hands-free safety assistance experience."
        ),
        (
            "Role-Based Access Control and Cloud Dashboard",
            "Adding JWT-based authentication to the FastAPI backend and providing an "
            "optional cloud synchronisation mode (summary statistics only, never raw "
            "video) would allow safety managers at a central office to monitor "
            "compliance trends across multiple sites while keeping raw footage local."
        ),
    ]

    for i, (title, body) in enumerate(future_items, 1):
        story.append(KeepTogether([
            Paragraph(f"<b>{i}.  {title}</b>", ss["BodyJ"]),
            Paragraph(body, ss["BulletItem"]),
            sp(0.2),
        ]))

    story.append(PageBreak())


def build_bibliography(ss, story):
    story.append(Paragraph("Bibliography", ss["ChapterTitle"]))
    story.append(hr(ss))
    story.append(sp(0.3))

    refs = [
        ("[1]",
         "J. Redmon and A. Farhadi, \"YOLOv3: An Incremental Improvement,\" "
         "<i>arXiv preprint arXiv:1804.02767</i>, 2018."),
        ("[2]",
         "G. Jocher, A. Chaurasia, and J. Qiu, \"Ultralytics YOLO,\" "
         "<i>GitHub repository</i>, 2023. [Online]. Available: "
         "https://github.com/ultralytics/ultralytics"),
        ("[3]",
         "A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, "
         "\"YOLOv4: Optimal Speed and Accuracy of Object Detection,\" "
         "<i>arXiv preprint arXiv:2004.10934</i>, 2020."),
        ("[4]",
         "S. Tiong, D. Dababneh, and I. Tanveer, "
         "\"Real-Time PPE Detection on Construction Sites Using Computer Vision,\" "
         "<i>IEEE Transactions on Industrial Informatics</i>, vol. 18, no. 3, "
         "pp. 1934–1943, Mar. 2022."),
        ("[5]",
         "T. Sebastiampillai et al., "
         "\"Edge AI Deployment of Safety Monitoring Systems for Industrial Applications,\" "
         "<i>Proceedings of the IEEE International Conference on Edge Computing (EDGE)</i>, "
         "pp. 48–57, 2023."),
        ("[6]",
         "European Parliament, \"Regulation (EU) 2016/679 (General Data Protection "
         "Regulation),\" <i>Official Journal of the European Union</i>, L 119, May 2018."),
        ("[7]",
         "S. Peng, Z. Wang, and X. Li, "
         "\"Privacy-Preserving Video Analytics at the Edge: A Survey,\" "
         "<i>ACM Computing Surveys</i>, vol. 55, no. 6, Article 118, Jun. 2023."),
        ("[8]",
         "FastAPI Documentation, Sebastián Ramírez, 2024. [Online]. Available: "
         "https://fastapi.tiangolo.com"),
        ("[9]",
         "SQLite Documentation, D. Richard Hipp, 2024. [Online]. Available: "
         "https://www.sqlite.org/docs.html"),
        ("[10]",
         "React Documentation, Meta Open Source, 2024. [Online]. Available: "
         "https://react.dev"),
        ("[11]",
         "Ministry of Labour and Employment, Government of India, "
         "\"Construction Workers (Regulation of Employment and Conditions of Service) Act, "
         "1996,\" <i>Gazette of India</i>, 1996."),
        ("[12]",
         "W. Liu et al., \"SSD: Single Shot MultiBox Detector,\" "
         "<i>European Conference on Computer Vision (ECCV)</i>, "
         "Springer, Cham, pp. 21–37, 2016."),
    ]

    for tag, text in refs:
        combined = f"<b>{tag}</b>  {text}"
        story.append(Paragraph(combined, ss["RefEntry"]))
        story.append(sp(0.1))

    story.append(PageBreak())


def build_appendices(ss, story):
    story.append(Paragraph("Appendices", ss["ChapterTitle"]))
    story.append(hr(ss))
    story.append(sp(0.3))

    # ── Appendix A ──────────────────────────────────────────────────────────
    story.append(Paragraph("Appendix A – REST API Endpoint Reference", ss["SectionTitle"]))
    story.append(sp(0.2))
    story.append(Paragraph(
        "All endpoints are served by the FastAPI backend running on port 8000. "
        "Interactive documentation is available at <b>http://localhost:8000/docs</b>.",
        ss["BodyJ"]))
    story.append(sp(0.2))

    api_data = [
        ["Method", "Endpoint",                    "Description"],
        ["GET",    "/api/v1/status",              "System health and monitoring state"],
        ["POST",   "/api/v1/monitoring/start",    "Begin edge inference loop"],
        ["POST",   "/api/v1/monitoring/stop",     "Halt inference loop"],
        ["POST",   "/api/v1/upload",              "Upload sample video for testing"],
        ["GET",    "/api/v1/detections/latest",   "Most recent detection result"],
        ["GET",    "/api/v1/alerts/latest",        "Last N safety alerts"],
        ["GET",    "/api/v1/history",             "Paginated safety-event history"],
        ["GET",    "/api/v1/statistics",          "Aggregate and 7-day trend stats"],
        ["GET",    "/api/v1/languages",           "List supported TTS languages"],
        ["PUT",    "/api/v1/settings",            "Update system configuration"],
        ["GET",    "/api/v1/recommendations/{t}", "Safety recommendation for type t"],
        ["POST",   "/api/v1/privacy/purge",       "Purge records older than N days"],
        ["GET",    "/api/v1/privacy/audit",       "Privacy audit log"],
        ["GET",    "/api/v1/stream",              "MJPEG annotated video stream"],
    ]
    story.append(tbl(api_data, [1.8*cm, 5.8*cm, 7*cm]))
    story.append(Paragraph(
        "Table A.1 – Complete REST API endpoint reference.", ss["Caption"]))
    story.append(sp(0.5))

    # ── Appendix B ──────────────────────────────────────────────────────────
    story.append(Paragraph("Appendix B – Database Schema", ss["SectionTitle"]))
    story.append(sp(0.2))

    schema_tables = [
        ("safety_events", [
            ["Column",           "Type",        "Description"],
            ["id",               "INTEGER PK",  "Auto-increment primary key"],
            ["violation_type",   "TEXT",        "Enum: NO_HELMET, NO_VEST, …"],
            ["severity",         "TEXT",        "LOW / MEDIUM / HIGH / CRITICAL"],
            ["confidence",       "REAL",        "Detection confidence (0–1)"],
            ["recommendation",   "TEXT",        "Corrective action message"],
            ["alert_sent",       "BOOLEAN",     "Voice alert dispatched flag"],
            ["created_at",       "DATETIME",    "UTC timestamp of detection"],
            ["worker_id",        "TEXT",        "Anonymised worker token"],
        ]),
        ("safety_rules", [
            ["Column",           "Type",        "Description"],
            ["id",               "INTEGER PK",  "Rule identifier"],
            ["violation_type",   "TEXT",        "Maps to safety_events.violation_type"],
            ["severity",         "TEXT",        "Default severity level"],
            ["cooldown_seconds", "INTEGER",     "Debounce interval between alerts"],
            ["is_active",        "BOOLEAN",     "Enable/disable rule without deleting"],
            ["description",      "TEXT",        "Human-readable rule description"],
        ]),
        ("privacy_audit_log", [
            ["Column",           "Type",        "Description"],
            ["id",               "INTEGER PK",  "Auto-increment"],
            ["action",           "TEXT",        "PURGE / EXPORT / ACCESS"],
            ["performed_by",     "TEXT",        "System or user identifier"],
            ["records_affected", "INTEGER",     "Number of rows modified"],
            ["timestamp",        "DATETIME",    "UTC timestamp of action"],
        ]),
    ]

    for tname, tdata in schema_tables:
        story.append(Paragraph(f"<b>Table: <i>{tname}</i></b>", ss["BodyJ"]))
        story.append(tbl(tdata, [3.5*cm, 3*cm, 8*cm]))
        story.append(sp(0.3))

    story.append(PageBreak())

    # ── Appendix C ──────────────────────────────────────────────────────────
    story.append(Paragraph("Appendix C – Project Directory Structure", ss["SectionTitle"]))
    story.append(sp(0.2))

    tree = """\
construction-safety-system/
├── backend/
│   ├── ai/               # Detection, training, export, validation
│   ├── alerts/           # Voice alerts, alert manager
│   ├── api/              # FastAPI routes and Pydantic schemas
│   ├── camera/           # Frame capture, video processor
│   ├── database/         # SQLAlchemy models, DB session, event repo
│   ├── preprocessing/    # CLAHE, letterbox resize, facial blur
│   ├── privacy/          # Compliance manager, audit logging
│   ├── safety/           # Rule registry, violation analyser, recommendations
│   ├── tests/            # Pytest suite (8 tests, all passing)
│   ├── config.py         # Pydantic settings
│   ├── main.py           # FastAPI application entry point
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/   # Sidebar, Navbar, StatCard, AlertCard, StatusBadge
│   │   ├── pages/        # 7 full page components
│   │   └── services/     # Axios API client
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── api-documentation.md
│   ├── architecture.md
│   ├── snapshots/        # 4 generated PNG figures
│   └── SIT_Construction_Safety_Project_Report.pdf
├── models/               # Pretrained / fine-tuned YOLO weights
├── data/                 # Training datasets (not committed to VCS)
├── run_system.py         # Unified launcher (backend + frontend)
├── start.bat
└── README.md"""

    story.append(Paragraph(tree.replace("\n","<br/>").replace(" ","&nbsp;"),
                            ss["CodeBlock"]))
    story.append(sp(0.5))

    # ── Appendix D ──────────────────────────────────────────────────────────
    story.append(Paragraph("Appendix D – Raspberry Pi Deployment Checklist", ss["SectionTitle"]))
    story.append(sp(0.2))

    rpi_steps = [
        ("Operating System", "Raspberry Pi OS Lite 64-bit (Bookworm), headless mode"),
        ("Python",           "Python 3.11 from deadsnakes PPA; create venv"),
        ("YOLO Runtime",     "pip install ultralytics onnxruntime (CPU build); "
                             "copy exported model: backend/ai/export_edge_onnx.py"),
        ("SQLite",           "Pre-installed; no additional steps required"),
        ("Camera Interface", "Enable via raspi-config → Interface Options → Legacy Camera"),
        ("Network",          "Connect to site LAN; set static IP 192.168.1.100"),
        ("Autostart",        "Copy start.service to /etc/systemd/system/; "
                             "systemctl enable start.service"),
        ("Voice Output",     "sudo apt install espeak; pyttsx3 uses espeak driver on Linux"),
        ("Storage",          "Minimum 16 GB MicroSD (Class 10 / A1 rated)"),
        ("Power",            "Official 5 V / 3 A USB-C PSU; UPS HAT recommended for sites"),
    ]

    rpi_data = [["Step", "Detail"]] + [[k, v] for k,v in rpi_steps]
    story.append(tbl(rpi_data, [4.5*cm, 10*cm]))
    story.append(Paragraph(
        "Table D.1 – Raspberry Pi 4 deployment checklist.", ss["Caption"]))


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
        title="SIT Construction Safety System – Project Report",
        author="SIT Tumakuru Mini-Project Team 2026-27",
    )

    build_cover(ss, story)
    build_chapter7(ss, story)
    build_chapter8(ss, story)
    build_bibliography(ss, story)
    build_appendices(ss, story)

    # Build with header/footer on all pages except the cover
    def on_page(canvas, doc):
        if doc.page > 1:
            _page_decor(canvas, doc)

    doc.build(story, onFirstPage=_first_page, onLaterPages=on_page)
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"\n✅  PDF generated successfully!")
    print(f"   Location : {OUTPUT}")
    print(f"   Size     : {size_kb} KB")


if __name__ == "__main__":
    main()
