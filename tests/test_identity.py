"""Slice 26: manual identification of the violator (tech.md 8.27)."""

from typing import Any

import httpx
from test_broadcast import camera, drain
from test_event_actions import row
from test_operator_views import event
from test_stats_ohs import DAY, cameras, counts

from safewatch import store
from safewatch.hub import hub
from safewatch.types import EventDetail, PeopleStats

OHS = {"X-Role": "ohs", "X-Actor": "petrova"}


def history(event_id: int) -> list[tuple[str, str, str, str, str]]:
    rows = store.all("SELECT * FROM event_actions WHERE event_id = ? ORDER BY id", event_id)
    return [
        (r["actor_role"], r["action"], r["from_status"], r["to_status"], r["comment"])
        for r in rows[1:]
    ]


async def identify(
    client: httpx.AsyncClient, event_id: int, headers: dict[str, str] = OHS, **body: Any
) -> httpx.Response:
    return await client.patch(f"/api/events/{event_id}/identity", json=body, headers=headers)


async def test_identify_writes_fields_and_history(client: httpx.AsyncClient) -> None:
    event_id = event(camera(), status="sent_to_master")
    ws = hub.connect("operator")
    body = {"person_name": "  Сидоров Пётр ", "person_position": "стропальщик", "crew": " 3 "}
    r = await identify(client, event_id, **body)
    assert r.status_code == 200, r.text
    detail = EventDetail.model_validate(r.json())
    assert (detail.event.person_name, detail.event.person_position, detail.event.crew) == (
        "Сидоров Пётр",
        "стропальщик",
        "3",
    )
    assert detail.event.status == "sent_to_master" and detail.can_identify
    found = row(event_id)
    assert (found["person_name"], found["person_position"], found["crew"]) == (
        "Сидоров Пётр",
        "стропальщик",
        "3",
    )
    assert found["status"] == "sent_to_master"
    comment = "ФИО: Сидоров Пётр; должность: стропальщик; бригада: 3"
    assert history(event_id) == [("ohs", "identified", "sent_to_master", "sent_to_master", comment)]
    updated = [(d["id"], d["person_name"]) for kind, d in drain(ws) if kind == "event.updated"]
    assert updated == [(event_id, "Сидоров Пётр")]
    # The same values after the trim: 200, no new row, no message.
    r = await identify(client, event_id, **body)
    assert r.status_code == 200 and len(history(event_id)) == 1 and drain(ws) == []
    # A terminal event is identified too; empty strings clear the fields.
    store.event_update(event_id, {"status": "resolved"})
    r = await identify(client, event_id, person_name=" ", person_position="", crew="")
    assert r.status_code == 200
    assert (row(event_id)["person_name"], row(event_id)["crew"]) == ("", "")
    assert history(event_id)[-1] == (
        "ohs", "identified", "resolved", "resolved", "Идентификация очищена"
    )  # fmt: skip
    assert row(event_id)["status"] == "resolved"


async def test_identify_roles(client: httpx.AsyncClient) -> None:
    event_id = event(camera())
    r = await identify(client, event_id, headers={"X-Role": "operator"}, person_name="Сидоров")
    assert (r.status_code, r.json()["code"]) == (403, "forbidden_role")
    r = await identify(client, event_id, headers={}, person_name="Сидоров")
    assert (r.status_code, r.json()["code"]) == (400, "role_required")
    assert row(event_id)["person_name"] == "" and history(event_id) == []
    r = await identify(client, event_id, headers={"X-Role": "management"}, crew="5")
    assert r.status_code == 200 and EventDetail.model_validate(r.json()).can_identify
    assert history(event_id) == [
        ("management", "identified", "new", "new", "ФИО: —; должность: —; бригада: 5")
    ]
    for role, allowed in [("ohs", True), ("management", True), ("operator", False), (None, False)]:
        headers = {} if role is None else {"X-Role": role}
        r = await client.get(f"/api/events/{event_id}", headers=headers)
        assert EventDetail.model_validate(r.json()).can_identify is allowed, role


async def test_identify_limits(client: httpx.AsyncClient) -> None:
    event_id = event(camera())
    r = await identify(client, event_id, person_name=" " + "Я" * 80 + " ")
    assert r.status_code == 200 and row(event_id)["person_name"] == "Я" * 80
    for field in ("person_name", "person_position", "crew"):
        r = await identify(client, event_id, **{field: "Я" * 81})
        assert (r.status_code, r.json()["message"]) == (422, "Поле: до 80 символов"), field
        assert r.json()["details"]["field"] == field
    assert len(history(event_id)) == 1
    r = await identify(client, 999, person_name="Сидоров")
    assert r.status_code == 404


async def test_people_stats_only_filled(client: httpx.AsyncClient) -> None:
    c = cameras()
    for values in [
        {"person_name": "Сидоров П.", "crew": "3", "operator_verdict": "confirmed"},
        {"person_name": "Сидоров П.", "crew": "3"},
        {"person_name": "Кузнецов А."},
        {"crew": "5", "operator_verdict": "false_alarm"},
        {"person_position": "сварщик"},  # a position alone does not identify
        {},
    ]:
        event(c["north"], **values)
    event(c["south"], person_name="Кузнецов А.", started_at="2026-10-23T08:00:00.000Z")
    r = await client.get("/api/stats/people", params=DAY)
    assert r.status_code == 200, r.text
    stats = PeopleStats.model_validate(r.json())
    assert (stats.total, stats.identified) == (6, 4)
    assert [p.key for p in stats.by_person] == ["Сидоров П.", "Кузнецов А."]
    assert counts(stats.by_person) == {"Сидоров П.": (2, 1, 0), "Кузнецов А.": (1, 0, 0)}
    assert counts(stats.by_crew) == {"3": (2, 1, 0), "5": (1, 0, 1)}
    wrong = {"date_from": DAY["date_to"], "date_to": DAY["date_from"]}
    r = await client.get("/api/stats/people", params=wrong)
    assert (r.status_code, r.json()["message"]) == (422, "Неверный период")
