"""Slice 13: OHS statistics (tech.md 8.13, 9)."""

from datetime import timedelta
from typing import Any

import httpx
from test_broadcast import AT
from test_operator_views import event

from safewatch import clock, services, store
from safewatch.config import Settings
from safewatch.types import ApiError, CameraIn, CountRow, OhsStats, SectorIn

DAY = {"date_from": "2026-10-24T00:00:00Z", "date_to": "2026-10-25T00:00:00Z"}


def cameras() -> dict[str, int]:
    north_sector = services.sector_create(SectorIn(name="Сектор 1 · Цех"), "admin").id
    south_sector = services.sector_create(SectorIn(name="Сектор 2 · Склад"), "admin").id
    north = services.camera_create(CameraIn(sector_id=north_sector, name="Камера Север"), "admin")
    south = services.camera_create(CameraIn(sector_id=south_sector, name="Камера Юг"), "admin")
    return {"north_sector": north_sector, "south_sector": south_sector, "north": north.id,
            "south": south.id}  # fmt: skip


def act(event_id: int, seconds: float, role: str, action: str) -> None:
    """An action `seconds` after the publication at `AT`."""
    at = clock.iso(clock.parse(AT) + timedelta(seconds=seconds))
    store.insert("event_actions", {
        "event_id": event_id, "at": at, "actor_role": role, "actor_name": role, "action": action,
    })  # fmt: skip


def counts(rows: list[CountRow]) -> dict[str, tuple[int, int, int]]:
    return {r.title: (r.count, r.confirmed, r.false_alarm) for r in rows}


async def stats(client: httpx.AsyncClient, **params: Any) -> OhsStats:
    r = await client.get("/api/stats/ohs", params=params)
    assert r.status_code == 200, r.text
    return OhsStats.model_validate(r.json())


async def test_counts_by_dimensions(client: httpx.AsyncClient) -> None:
    c = cameras()
    event(c["north"])
    event(
        c["north"], scenario="fall", title="Падение и неподвижность", level="red",
        status="resolved", operator_verdict="confirmed",
    )  # fmt: skip
    event(
        c["south"], scenario="phone", title="Телефон при работе", status="false_alarm",
        operator_verdict="false_alarm",
    )  # fmt: skip
    event(c["south"], level="red", status="superseded")
    event(c["north"], status="confirmed", operator_verdict="confirmed", is_demo=1)
    event(c["north"], started_at="2026-10-25T00:00:00.000Z")  # date_to is not included

    found = await stats(client, **DAY)
    assert found.total == 4
    assert counts(found.by_status) == {
        "Новое": (1, 0, 0), "Решено": (1, 1, 0), "Ложное срабатывание": (1, 0, 1),
        "Подтверждено": (1, 1, 0),
    }  # fmt: skip
    assert counts(found.by_scenario) == {
        "Бег и резкие перемещения": (2, 1, 0), "Падение и неподвижность": (1, 1, 0),
        "Телефон при работе": (1, 0, 1),
    }  # fmt: skip
    assert counts(found.by_sector) == {"Сектор 1 · Цех": (3, 2, 0), "Сектор 2 · Склад": (1, 0, 1)}
    assert counts(found.by_camera) == {"Камера Север": (3, 2, 0), "Камера Юг": (1, 0, 1)}

    no_demo = await stats(client, **DAY, include_demo="false")
    assert (no_demo.total, no_demo.include_demo) == (3, False)
    assert counts(no_demo.by_sector)["Сектор 1 · Цех"] == (2, 1, 0)
    assert (await stats(client, **DAY, sector_id=c["south_sector"])).total == 1
    assert (await stats(client, **DAY, camera_id=c["north"])).total == 3


async def test_period_invalid(client: httpx.AsyncClient) -> None:
    same = await stats(client, date_from=DAY["date_from"], date_to=DAY["date_from"])
    assert same.total == 0
    r = await client.get(
        "/api/stats/ohs", params={"date_from": DAY["date_to"], "date_to": DAY["date_from"]}
    )
    assert r.status_code == 422
    assert ApiError.model_validate(r.json()).message == "Неверный период"


def test_shift_and_hour_grouping_msk(core: Settings) -> None:
    c = cameras()
    for at in (
        "2026-10-23T20:59:00.000Z",
        "2026-10-23T21:00:00.000Z",  # 23:59 and 00:00 MSK
        "2026-10-24T04:59:00.000Z",
        "2026-10-24T05:00:00.000Z",
    ):  # 07:59 and 08:00 MSK
        event(c["north"], started_at=at)  # fmt: skip
    found = services.ohs_stats_view(
        clock.parse("2026-10-23T00:00:00Z"), clock.parse("2026-10-25T00:00:00Z")
    )
    assert [(d.date, d.yellow) for d in found.by_day] == [
        ("2026-10-23", 1), ("2026-10-24", 3), ("2026-10-25", 0),
    ]  # fmt: skip
    hours = {r.key: r.count for r in found.by_hour}
    assert len(hours) == 24
    assert (hours["23"], hours["00"], hours["07"], hours["08"], hours["20"]) == (1, 1, 1, 1, 0)
    # The night shift runs over midnight: 23:59, 00:00 and 07:59 MSK are all in it.
    assert counts(found.by_shift) == {"Дневная смена": (1, 0, 0), "Ночная смена": (3, 0, 0)}


def test_false_share_and_coverage(core: Settings) -> None:
    c = cameras()
    empty = services.ohs_stats_view(clock.parse(DAY["date_from"]), clock.parse(DAY["date_to"]))
    assert (empty.reviewed, empty.false_alarm_share, empty.review_coverage) == (0, None, None)
    for verdict in ("confirmed", "confirmed", "false_alarm", "none"):
        event(c["north"], operator_verdict=verdict)
    found = services.ohs_stats_view(clock.parse(DAY["date_from"]), clock.parse(DAY["date_to"]))
    assert (found.reviewed, found.false_alarm_share, found.review_coverage) == (3, 1 / 3, 3 / 4)


def test_reaction_percentiles_nearest_rank(core: Settings) -> None:
    c = cameras()

    def made(status: str) -> int:
        return event(c["north"], status=status)

    empty = services.ohs_stats_view(clock.parse(DAY["date_from"]), clock.parse(DAY["date_to"]))
    assert (empty.operator_reaction_s.n, empty.operator_reaction_s.p50) == (0, None)
    act(made("confirmed"), 5, "operator", "confirmed")
    fa = made("false_alarm")
    act(fa, 0.5, "operator", "viewed")  # a view is not a decision
    act(fa, 1, "operator", "false_alarm")
    act(made("confirmed"), 4, "operator", "confirmed")
    resolved = made("resolved")
    act(resolved, 2, "operator", "sent_to_master")
    act(resolved, 12, "master", "master_accepted")
    act(resolved, 72, "master", "resolved")
    accepted = made("master_accepted")
    act(accepted, 3, "operator", "sent_to_master")
    act(accepted, 33, "master", "master_accepted")
    made("new")  # open, no decision yet
    made("auto_finished")  # closed without a decision: not pending
    act(made("sent_to_master"), 60, "system", "timeout_escalated")

    found = services.ohs_stats_view(clock.parse(DAY["date_from"]), clock.parse(DAY["date_to"]))
    op = found.operator_reaction_s
    assert (op.n, op.pending, op.p50, op.p95) == (5, 2, 3.0, 5.0)  # third and fifth of 5
    accept = found.master_accept_s
    assert (accept.n, accept.pending, accept.p50, accept.p95) == (2, 1, 10.0, 30.0)
    resolve = found.master_resolve_s
    assert (resolve.n, resolve.pending, resolve.p50, resolve.p95) == (1, 1, 60.0, 60.0)
