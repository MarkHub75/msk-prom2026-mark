from datetime import UTC, datetime, timedelta, timezone

from safewatch import clock
from safewatch.texts import fmt_num


def test_iso_roundtrip_utc_millis() -> None:
    moscow = timezone(timedelta(hours=3))
    dt = datetime(2026, 10, 24, 12, 30, 15, 123456, tzinfo=moscow)
    text = clock.iso(dt)
    assert text == "2026-10-24T09:30:15.123Z"
    back = clock.parse(text)
    assert back == datetime(2026, 10, 24, 9, 30, 15, 123000, tzinfo=UTC)
    assert clock.iso(back) == text
    assert clock.now().tzinfo is UTC
    assert clock.local(back, "Europe/Moscow").hour == 12


def test_fmt_num_uses_comma() -> None:
    assert fmt_num(3.14) == "3,1"
    assert fmt_num(2) == "2,0"
