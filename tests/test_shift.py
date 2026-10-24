"""Slice 8: the shift summary of the master (tech.md 8.14, shifts in `config/default.yaml`)."""

from datetime import UTC, datetime

import httpx
import pytest
from test_broadcast import camera
from test_operator_views import event

from safewatch import config, services
from safewatch.config import Settings
from safewatch.types import ShiftSummary


def utc(day: int, hour: int, minute: int = 0, second: int = 0) -> datetime:
    return datetime(2026, 10, day, hour, minute, second, tzinfo=UTC)


@pytest.mark.parametrize(
    ("at", "shift", "start", "end"),
    [
        (utc(24, 4, 59, 59), "night", utc(23, 17), utc(24, 5)),  # 07:59:59 MSK
        (utc(24, 5), "day", utc(24, 5), utc(24, 17)),  # 08:00:00 MSK
        (utc(24, 16, 59, 59), "day", utc(24, 5), utc(24, 17)),  # 19:59:59 MSK
        (utc(24, 17), "night", utc(24, 17), utc(25, 5)),  # 20:00:00 MSK
        (utc(24, 21, 30), "night", utc(24, 17), utc(25, 5)),  # 00:30 MSK, after midnight
    ],
)
def test_shift_window_boundaries(
    core: Settings, at: datetime, shift: str, start: datetime, end: datetime
) -> None:
    found = services.shift_summary_view(at)
    assert (found.shift_id, found.start, found.end) == (shift, start, end)
    assert found.title == {"day": "Дневная смена", "night": "Ночная смена"}[shift]


def test_other_timezone_moves_the_window(
    core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    utc_zone = core.model_copy(update={"timezone": "UTC"})
    monkeypatch.setattr(config, "get_settings", lambda: utc_zone)
    found = services.shift_summary_view(utc(24, 5))  # 05:00 UTC is still the night there
    assert (found.shift_id, found.start, found.end) == ("night", utc(23, 20), utc(24, 8))


async def test_shift_summary_counts(client: httpx.AsyncClient) -> None:
    fifth, seventh = camera(), camera("Сектор 7 · Цех")
    inside = "2026-10-24T06:00:00.000Z"
    run_ok = event(fifth, started_at=inside, operator_verdict="confirmed", status="confirmed")
    event(fifth, started_at=inside, operator_verdict="false_alarm", status="false_alarm")
    fall_ok = event(
        seventh, started_at="2026-10-24T05:00:00.000Z", scenario="fall", level="red",
        title="Падение и неподвижность", operator_verdict="confirmed", status="resolved",
    )  # fmt: skip
    event(seventh, started_at=inside)  # no verdict yet
    event(fifth, started_at="2026-10-24T04:59:59.999Z", operator_verdict="confirmed")  # night
    event(fifth, started_at="2026-10-24T17:00:00.000Z", operator_verdict="confirmed")  # night
    event(fifth, started_at=inside, status="superseded")
    r = await client.get("/api/master/shift", params={"at": "2026-10-24T09:00:00Z"})
    assert r.status_code == 200, r.text
    found = ShiftSummary.model_validate(r.json())
    assert (found.shift_id, found.total) == ("day", 4)
    sectors = [(c.title, c.count, c.confirmed, c.false_alarm) for c in found.by_sector]
    assert sectors == [("Сектор 5 · Склад", 2, 1, 1), ("Сектор 7 · Цех", 2, 1, 0)]
    scenarios = [(c.key, c.title, c.count, c.confirmed) for c in found.by_scenario]
    assert scenarios == [
        ("running", "Бег и резкие перемещения", 3, 1),
        ("fall", "Падение и неподвижность", 1, 1),
    ]
    assert [e.id for e in found.events] == [fall_ok, run_ok]
    bad = await client.get("/api/master/shift", params={"at": "вчера"})
    assert (bad.status_code, bad.json()["code"]) == (422, "validation")
