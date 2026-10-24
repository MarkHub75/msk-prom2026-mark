"""Slice 30: the shift summary as a PDF (tech.md 8.31)."""

import io

import httpx
from pypdf import PdfReader
from test_broadcast import camera
from test_operator_views import event
from test_shift import utc

from safewatch import services
from safewatch.config import Settings

INSIDE = "2026-10-24T06:00:00.000Z"  # 09:00 MSK, the day shift


def _text(data: bytes) -> str:
    """Page text; the line breaks of wrapped table cells fold into spaces."""
    pages = PdfReader(io.BytesIO(data)).pages
    return " ".join(" ".join(page.extract_text() for page in pages).split())


async def test_pdf_has_cyrillic_summary(core: Settings) -> None:
    fifth = camera()
    event(
        fifth, started_at=INSIDE, operator_verdict="confirmed", status="confirmed",
        reason_text="Человек в зоне «Проезд погрузчиков»",
    )  # fmt: skip
    event(fifth, started_at=INSIDE, operator_verdict="false_alarm", status="false_alarm")
    data = await services.shift_report_pdf(utc(24, 9))
    assert data.startswith(b"%PDF")
    text = _text(data)
    for line in (
        "Argus · Сводка смены",
        "Смена: Дневная смена",
        "Период: с 24.10.2026 08:00 до 24.10.2026 20:00 (МСК)",
        "Всего событий: 2",
        "Сектор 5 · Склад",
        "Бег и резкие перемещения",
        "Подтверждённые события",
        "Человек в зоне «Проезд погрузчиков»",
    ):
        assert line in text, line
    assert "Бег 2,4 роста/с" not in text  # the false alarm is counted, not listed


async def test_pdf_route_and_bad_at(client: httpx.AsyncClient) -> None:
    event(camera(), started_at=INSIDE, operator_verdict="confirmed", status="confirmed")
    r = await client.get("/api/master/shift.pdf", params={"at": "2026-10-24T21:30:00Z"})
    assert r.status_code == 200, r.text
    assert r.headers["content-type"] == "application/pdf"
    # 00:30 MSK of the 25th belongs to the night shift that started on the 24th.
    assert r.headers["content-disposition"] == 'attachment; filename="shift-2026-10-24-night.pdf"'
    assert r.content.startswith(b"%PDF") and "Ночная смена" in _text(r.content)
    now = await client.get("/api/master/shift.pdf")
    assert now.status_code == 200 and now.content.startswith(b"%PDF")
    bad = await client.get("/api/master/shift.pdf", params={"at": "мусор"})
    assert (bad.status_code, bad.json()["code"]) == (422, "validation")
