from __future__ import annotations

import os
import textwrap
from pathlib import Path

try:
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install with 'pip install reportlab pillow'\n"
        f"Original error: {exc}"
    )

PROFILE_NAME = "Arooshtausif24"
PROFILE_HANDLE = "@Arooshtausif24"
PROFILE_TITLE = "PPS Semester 1"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "code_profile_report.pdf"
PROFILE_IMAGE = BASE_DIR / "profile.png"

# Files to include as screenshot-style pages
CODE_FILES = [
    BASE_DIR / "sum and difference of two numbers.c",
    BASE_DIR / "bitwise operators.c",
    BASE_DIR / "Functions in C.c",
    BASE_DIR / "For loop in C.c",
]


def wrap_code_lines(code_text: str, max_chars: int = 96):
    lines = code_text.splitlines()
    wrapped = []
    for line in lines:
        if len(line) <= max_chars:
            wrapped.append(line)
            continue
        wrapped.extend(textwrap.wrap(line, width=max_chars, break_long_words=False, break_on_hyphens=False))
    return wrapped


def draw_profile_header(pdf: canvas.Canvas, page_w: float, page_h: float):
    card_x = 22 * mm
    card_y = page_h - 42 * mm
    card_w = page_w - 44 * mm
    card_h = 28 * mm

    pdf.setFillColor(HexColor("#f4f7fb"))
    pdf.roundRect(card_x, card_y, card_w, card_h, 7, stroke=0, fill=1)

    img_x = card_x + 8 * mm
    img_y = card_y + 6 * mm
    img_size = 16 * mm

    if PROFILE_IMAGE.exists():
        try:
            img = ImageReader(str(PROFILE_IMAGE))
            pdf.drawImage(img, img_x, img_y, width=img_size, height=img_size, preserveAspectRatio=True)
            pdf.setStrokeColor(HexColor("#dfe8f3"))
            pdf.circle(img_x + img_size / 2, img_y + img_size / 2, img_size / 2 + 2, stroke=1, fill=0)
        except Exception:
            pass
    else:
        pdf.setFillColor(HexColor("#dfe8f3"))
        pdf.circle(img_x + img_size / 2, img_y + img_size / 2, img_size / 2, fill=1, stroke=0)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(img_x + img_size / 2, img_y + img_size / 2 - 3, "MY")

    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(img_x + 20 * mm, card_y + 17 * mm, PROFILE_NAME)

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(HexColor("#4b5563"))
    pdf.drawString(img_x + 20 * mm, card_y + 10 * mm, PROFILE_HANDLE)
    pdf.drawString(img_x + 20 * mm, card_y + 5 * mm, PROFILE_TITLE)

    pdf.setFillColor(HexColor("#0b5fff"))
    pdf.roundRect(card_x + card_w - 52 * mm, card_y + 7 * mm, 28 * mm, 9 * mm, 4, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(card_x + card_w - 38 * mm, card_y + 10 * mm, "PROFILE")


def draw_code_page(pdf: canvas.Canvas, file_path: Path, page_num: int):
    page_w, page_h = A4
    margin = 18 * mm
    code_x = margin
    code_y = 25 * mm
    code_w = page_w - 2 * margin
    code_h = page_h - 45 * mm

    pdf.setFillColor(white)
    pdf.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    pdf.setFillColor(HexColor("#0f172a"))
    pdf.roundRect(10 * mm, page_h - 20 * mm, page_w - 20 * mm, 12 * mm, 5, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(15 * mm, page_h - 15.5 * mm, f"{page_num}. {file_path.name}")

    pdf.setFillColor(HexColor("#111827"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(15 * mm, page_h - 24 * mm, "Source Code Screenshot")

    # Add a code area with border and subtle shadow effect
    pdf.setFillColor(HexColor("#f8fafc"))
    pdf.roundRect(code_x, code_y, code_w, code_h, 6, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#d7e0eb"))
    pdf.setLineWidth(1)

    # Top bar of the code window
    pdf.setFillColor(HexColor("#e2e8f0"))
    pdf.roundRect(code_x + 1.8 * mm, code_h + code_y - 4 * mm, code_w - 3.6 * mm, 9 * mm, 4, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#ef4444"))
    pdf.circle(code_x + 5 * mm, code_y + code_h - 11 * mm, 2.2 * mm, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#fbbf24"))
    pdf.circle(code_x + 9 * mm, code_y + code_h - 11 * mm, 2.2 * mm, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#22c55e"))
    pdf.circle(code_x + 13 * mm, code_y + code_h - 11 * mm, 2.2 * mm, fill=1, stroke=0)

    code_text = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = wrap_code_lines(code_text)

    pdf.setFillColor(black)
    pdf.setFont("Courier-Bold", 8)
    line_height = 4.7 * mm
    start_x = code_x + 6 * mm
    start_y = code_y + code_h - 16 * mm

    for i, line in enumerate(lines[:90]):
        if start_y - (i * line_height) < code_y + 4 * mm:
            break
        pdf.drawString(start_x, start_y - i * line_height, line)

    if len(lines) > 90:
        pdf.setFillColor(HexColor("#6b7280"))
        pdf.setFont("Courier", 7)
        pdf.drawString(start_x, code_y + 7 * mm, "... more code ...")


def build_pdf():
    page_w, page_h = A4
    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)

    # Cover page with profile summary
    pdf.setFillColor(HexColor("#eef4ff"))
    pdf.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    draw_profile_header(pdf, page_w, page_h)

    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(25 * mm, page_h - 90 * mm, "C Programming Practice")

    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(HexColor("#374151"))
    pdf.drawString(25 * mm, page_h - 105 * mm, "Course: PPS Semester 1")
    pdf.drawString(25 * mm, page_h - 115 * mm, "Student: Arooshtausif24")
    pdf.drawString(25 * mm, page_h - 125 * mm, "Repository: Arooshtausif24/pps_sem1")

    pdf.setFillColor(HexColor("#1d4ed8"))
    pdf.roundRect(25 * mm, page_h - 150 * mm, 55 * mm, 9 * mm, 4, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(52.5 * mm, page_h - 145 * mm, "4 FILES")

    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(25 * mm, page_h - 180 * mm, "Included Programs:")
    pdf.setFont("Helvetica", 11)
    y = page_h - 195 * mm
    for name in [
        "sum and difference of two numbers.c",
        "bitwise operators.c",
        "Functions in C.c",
        "For loop in C.c",
    ]:
        pdf.drawString(30 * mm, y, "• " + name)
        y -= 8 * mm

    pdf.showPage()

    # Add each file as a screenshot-like page
    for idx, file_path in enumerate(CODE_FILES, start=1):
        if not file_path.exists():
            continue
        draw_code_page(pdf, file_path, idx)
        pdf.showPage()

    pdf.save()
    print(f"PDF created successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()
