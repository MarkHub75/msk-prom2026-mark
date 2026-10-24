"""PDF of the shift summary (tech.md 8.31): A4, tables only, DejaVu Sans for Cyrillic."""

from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from fpdf.fonts import FontFace

from safewatch import clock, texts
from safewatch.types import CountRow, ShiftSummary

FONT = "DejaVuSans.ttf"
_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / FONT
_FAMILY = "dejavu"
# One regular face only: the default bold headings of fpdf2 tables would need a second file.
_PLAIN = FontFace(emphasis="")


def _local(dt: datetime, tz: str, fmt: str = "%d.%m.%Y %H:%M") -> str:
    return clock.local(dt, tz).strftime(fmt)


def _counts(pdf: FPDF, title: str, head: str, rows: list[CountRow]) -> None:
    pdf.ln(4)
    pdf.set_font(_FAMILY, size=13)
    pdf.cell(text=title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(_FAMILY, size=10)
    with pdf.table(col_widths=(85, 35, 35, 35), headings_style=_PLAIN) as table:
        table.row([head, *texts.PDF_COUNT_HEAD])
        for r in rows:
            table.row([r.title, str(r.count), str(r.confirmed), str(r.false_alarm)])


def shift_pdf(summary: ShiftSummary, product_name: str, tz: str) -> bytes:
    pdf = FPDF(format="A4")
    pdf.add_font(_FAMILY, fname=_FONT_PATH)
    pdf.add_page()
    pdf.set_font(_FAMILY, size=16)
    pdf.cell(text=texts.PDF_TITLE.format(product=product_name), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(_FAMILY, size=11)
    start, end = _local(summary.start, tz), _local(summary.end, tz)
    for line in (
        texts.PDF_SHIFT.format(title=summary.title),
        texts.PDF_PERIOD.format(start=start, end=end),
        texts.PDF_TOTAL.format(n=summary.total),
    ):
        pdf.cell(text=line, new_x="LMARGIN", new_y="NEXT")
    _counts(pdf, texts.PDF_BY_SECTOR, texts.PDF_SECTOR, summary.by_sector)
    _counts(pdf, texts.PDF_BY_SCENARIO, texts.PDF_SCENARIO, summary.by_scenario)
    pdf.ln(4)
    pdf.set_font(_FAMILY, size=13)
    pdf.cell(text=texts.PDF_CONFIRMED, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(_FAMILY, size=9)
    with pdf.table(col_widths=(25, 35, 35, 65, 30), headings_style=_PLAIN) as table:
        table.row(list(texts.PDF_EVENTS_HEAD))
        for e in summary.events:
            when = _local(e.started_at, tz, "%d.%m %H:%M")
            table.row([when, e.sector_name, e.camera_name, e.reason_text, e.status_title])
    return bytes(pdf.output())
