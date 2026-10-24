"""Slice 13: management statistics (tech.md 8.13, 9). `fake_clock`: Saturday 2026-10-24
12:00 MSK, the current week starts on Monday 2026-10-19 00:00 MSK (2026-10-18 21:00 UTC)."""

import httpx
import pytest
from conftest import FakeClock
from test_operator_views import event

from safewatch import services
from safewatch.config import Settings
from safewatch.types import ApiError, CameraIn, ManagementStats, SectorIn


def sector(name: str, cameras: int) -> tuple[int, list[int]]:
    sector_id = services.sector_create(SectorIn(name=name), "admin").id
    ids = [
        services.camera_create(CameraIn(sector_id=sector_id, name=f"{name} {i}"), "admin").id
        for i in range(cameras)
    ]
    return sector_id, ids


def test_weeks_and_top_sectors_per_camera(core: Settings, fake_clock: FakeClock) -> None:
    _, (a1, a2) = sector("Сектор А", 2)
    _, (b1,) = sector("Сектор Б", 1)
    sector("Сектор В", 0)
    confirmed = {"status": "confirmed", "operator_verdict": "confirmed"}
    event(a1, started_at="2026-10-18T20:59:00.000Z", **confirmed)  # Sunday 23:59 MSK
    event(a2, started_at="2026-10-18T21:00:00.000Z", **confirmed)  # Monday 00:00 MSK
    event(a1, started_at="2026-10-06T09:00:00.000Z", level="red", **confirmed)
    event(b1, started_at="2026-10-20T09:00:00.000Z", **confirmed)
    event(b1, started_at="2026-10-13T09:00:00.000Z", status="false_alarm",
          operator_verdict="false_alarm")  # fmt: skip
    event(b1, started_at="2026-10-14T09:00:00.000Z", **confirmed)
    event(b1, started_at="2026-10-20T10:00:00.000Z", status="superseded",
          operator_verdict="confirmed")  # fmt: skip
    event(a1, started_at="2026-09-01T09:00:00.000Z", **confirmed)  # before the trend weeks

    found = services.management_view(3)
    assert [(w.week_start, w.yellow, w.red, w.confirmed, w.false_alarm) for w in found.weeks] == [
        ("2026-10-05", 0, 1, 1, 0), ("2026-10-12", 3, 0, 2, 1), ("2026-10-19", 2, 0, 2, 0),
    ]  # fmt: skip
    # Last 4 weeks (trend_weeks), confirmed per camera: Б 2 of 1 camera before А 3 of 2.
    top = [(r.title, r.cameras, r.confirmed, r.per_camera) for r in found.top_sectors]
    assert top == [("Сектор Б", 1, 2, 2.0), ("Сектор А", 2, 3, 1.5), ("Сектор В", 0, 0, None)]
    assert {r.key: r.count for r in found.top_scenarios} == {"running": 6}
    assert len(services.management_view().weeks) == core.stats.weeks_default


async def test_weeks_validation(client: httpx.AsyncClient) -> None:
    for weeks in (1, 52):
        r = await client.get("/api/stats/management", params={"weeks": weeks})
        assert r.status_code == 200, r.text
        assert len(ManagementStats.model_validate(r.json()).weeks) == weeks
    for weeks in (0, 53):
        r = await client.get("/api/stats/management", params={"weeks": weeks})
        assert r.status_code == 422
        assert ApiError.model_validate(r.json()).message == "Неверный период"


# Recent: 4 full weeks before 2026-10-19 MSK; previous: the 4 weeks before them.
RECENT, PREVIOUS = "2026-10-01T09:00:00.000Z", "2026-09-01T09:00:00.000Z"


@pytest.mark.parametrize(
    ("previous", "recent", "change", "text"),
    [
        (4, 3, -25.0, "Жёлтых нарушений стало меньше на 25 % (4 недели к 4 неделям). "
                      "Сравнение до и после не доказывает причину."),
        (2, 3, 50.0, "Жёлтых нарушений стало больше на 50 % (4 недели к 4 неделям). "
                     "Сравнение до и после не доказывает причину."),
        (2, 2, 0.0, "Жёлтых нарушений без изменений (4 недели к 4 неделям). "
                    "Сравнение до и после не доказывает причину."),
        (0, 2, None, "Недостаточно данных для сравнения"),
    ],
)  # fmt: skip
def test_yellow_trend_text(
    core: Settings,
    fake_clock: FakeClock,
    previous: int,
    recent: int,
    change: float | None,
    text: str,
) -> None:
    _, (cam,) = sector("Сектор А", 1)
    for at, n in ((PREVIOUS, previous), (RECENT, recent)):
        for _ in range(n):
            event(cam, started_at=at)
    event(cam, started_at=RECENT, status="false_alarm", operator_verdict="false_alarm")
    event(cam, started_at=RECENT, level="red")
    event(cam, started_at="2026-10-20T09:00:00.000Z")  # the current week is not full
    event(cam, started_at="2026-08-01T09:00:00.000Z")  # before the previous weeks
    trend = services.management_view().yellow_trend
    assert (trend.previous, trend.recent, trend.change_pct, trend.text) == (
        previous, recent, change, text,
    )  # fmt: skip
