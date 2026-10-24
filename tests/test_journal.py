"""Slice 12: the OHS journal, its filters, search, cursor and facets (tech.md 9, 16)."""

from typing import Any

import httpx
from test_operator_views import event

from safewatch import services
from safewatch.types import ApiError, CameraIn, EventPage, JournalFacets, SectorIn, ZoneIn


def world() -> dict[str, int]:
    """Two sectors, two cameras, a zone and events of every kind the filters tell apart."""
    north_sector = services.sector_create(SectorIn(name="Сектор 1 · Цех"), "admin").id
    south_sector = services.sector_create(SectorIn(name="Сектор 2 · Склад"), "admin").id
    north = services.camera_create(CameraIn(sector_id=north_sector, name="Камера Север"), "admin")
    south = services.camera_create(CameraIn(sector_id=south_sector, name="Камера Юг"), "admin")
    zone = services.zone_create(
        north.id, ZoneIn(kind="fence", name="Проход", points=[(0.1, 0.1), (0.5, 0.1)]), "ohs"
    )
    ids = {
        "north_sector": north_sector,
        "south_sector": south_sector,
        "north": north.id,
        "south": south.id,
        "zone": zone.id,
    }

    def at(hour: int) -> str:
        return f"2026-10-24T{hour:02d}:00:00.000Z"

    ids["run"] = event(north.id, started_at=at(8))
    ids["fall"] = event(
        north.id, scenario="fall", title="Падение и неподвижность", level="red",
        status="resolved", zone_id=zone.id, reason_text="Зафиксировано падение", started_at=at(9),
    )  # fmt: skip
    ids["phone"] = event(
        south.id, scenario="phone", title="Телефон при работе", status="false_alarm",
        reason_text="Телефон в руке 5 с", started_at=at(10),
    )  # fmt: skip
    ids["old"] = event(south.id, level="red", status="superseded", started_at=at(11))
    ids["demo"] = event(north.id, status="confirmed", is_demo=1, started_at=at(12))
    ids["odd"] = event(north.id, reason_text="Загрузка 50% · код a_b", started_at=at(12))
    return ids


async def page(client: httpx.AsyncClient, **params: Any) -> EventPage:
    r = await client.get("/api/events", params=params)
    assert r.status_code == 200, r.text
    return EventPage.model_validate(r.json())


async def found(client: httpx.AsyncClient, **params: Any) -> set[int]:
    return {e.id for e in (await page(client, **params)).items}


async def test_filters_each_dimension(client: httpx.AsyncClient) -> None:
    w = world()
    cases: list[tuple[dict[str, Any], set[int]]] = [
        ({"level": "red"}, {w["fall"]}),
        ({"scenario": "phone"}, {w["phone"]}),
        ({"status": "resolved"}, {w["fall"]}),
        ({"sector_id": w["south_sector"]}, {w["phone"]}),
        ({"camera_id": w["north"]}, {w["run"], w["fall"], w["demo"], w["odd"]}),
        ({"zone_id": w["zone"]}, {w["fall"]}),
        # date_from is included, date_to is not.
        ({"date_from": "2026-10-24T09:00:00Z", "date_to": "2026-10-24T10:00:00Z"}, {w["fall"]}),
    ]
    for params, expected in cases:
        assert await found(client, **params) == expected, params
    assert await found(client) == {w["run"], w["fall"], w["phone"], w["demo"], w["odd"]}


async def test_search_cyrillic_case_insensitive(client: httpx.AsyncClient) -> None:
    w = world()
    assert await found(client, q="ПАДЕНИЕ") == {w["fall"]}  # title and reason
    assert await found(client, q="юг") == {w["phone"]}  # camera name, superseded hidden
    assert await found(client, q="%") == {w["odd"]}
    assert await found(client, q="_") == {w["odd"]}
    assert await found(client, q="50%") == {w["odd"]}
    assert await found(client, q="a%b") == set()
    assert await found(client, q="\\") == set()


async def test_cursor_pagination(client: httpx.AsyncClient) -> None:
    world()
    seen: list[int] = []
    cursor: str | None = None
    for _ in range(10):
        params: dict[str, Any] = {"limit": 2} | ({"cursor": cursor} if cursor else {})
        p = await page(client, **params)
        assert p.total == 5 and len(p.items) <= 2
        seen += [e.id for e in p.items]
        cursor = p.next_cursor
        if cursor is None:
            break
    assert len(seen) == len(set(seen)) == 5
    full = await page(client, limit=200)
    assert [e.id for e in full.items] == seen  # newest start first, same order across pages


async def test_superseded_and_demo_flags(client: httpx.AsyncClient) -> None:
    w = world()
    everything = {w["run"], w["fall"], w["phone"], w["demo"], w["odd"]}
    assert await found(client) == everything
    assert await found(client, include_demo="false") == everything - {w["demo"]}
    assert await found(client, include_superseded="true") == everything | {w["old"]}


async def test_filter_validation(client: httpx.AsyncClient) -> None:
    world()
    bad = [
        {"limit": 0},
        {"limit": 201},
        {"q": "я" * 101},
        {"date_from": "2026-10-24T10:00:00Z", "date_to": "2026-10-24T09:00:00Z"},
        {"cursor": "abc"},
    ]
    for params in bad:
        r = await client.get("/api/events", params=params)
        assert r.status_code == 422, params
        assert ApiError.model_validate(r.json()).message.startswith("Неверный фильтр: ")
    r = await client.get("/api/events/export.csv", params={"limit": 0})
    assert r.status_code == 422
    assert len((await page(client, limit=200)).items) == 5
    await page(client, q="я" * 100)
    same = "2026-10-24T09:00:00Z"
    assert (await page(client, date_from=same, date_to=same)).items == []


async def test_facets_lists(client: httpx.AsyncClient) -> None:
    world()
    r = await client.get("/api/journal/facets")
    assert r.status_code == 200
    f = JournalFacets.model_validate(r.json())
    assert {"running", "fall", "phone"} <= {i.id for i in f.scenarios}
    assert [(i.id, i.title) for i in f.levels] == [
        ("yellow", "Жёлтая опасность"),
        ("red", "Красная опасность"),
    ]
    assert ("superseded", "Пересчитано") in [(i.id, i.title) for i in f.statuses]
    assert [i.title for i in f.sectors] == ["Сектор 1 · Цех", "Сектор 2 · Склад"]
    assert sorted(i.title for i in f.cameras) == ["Камера Север", "Камера Юг"]
    assert [i.title for i in f.zones] == ["Камера Север · Проход"]
