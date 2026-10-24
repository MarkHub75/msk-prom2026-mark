"""Slice 7: operator and master decisions on an event (tech.md 8.6, 9)."""

from typing import Any, get_args
from urllib.parse import quote

import httpx
import pytest
from test_broadcast import camera, drain
from test_operator_views import event

from safewatch import services, store, texts
from safewatch.config import Settings
from safewatch.errors import Conflict
from safewatch.hub import hub
from safewatch.types import ActionIn, ApiError, EventDetail, EventStatus, HumanAction, Role

OPERATOR, MASTER = {"X-Role": "operator"}, {"X-Role": "master"}
LATE = {"status": "sent_to_master", "escalated_by_timeout": 1, "red_at": "2026-10-24T08:00:00.000Z"}

# Human rows of the table in tech.md 8.6, in its order: role, action, event before, status
# after, verdict after, journal rows (action, from, to) the action writes.
ROWS: list[tuple[Role, HumanAction, dict[str, Any], EventStatus, str, list[tuple[str, ...]]]] = [
    ("operator", "view", {"level": "yellow"}, "viewed", "none", [("viewed", "new", "viewed")]),
    ("operator", "view", {"level": "red"}, "viewed", "none", [("viewed", "new", "viewed")]),
    ("operator", "confirm", {}, "confirmed", "confirmed", [("confirmed", "new", "confirmed")]),
    ("operator", "confirm", {"status": "viewed"}, "confirmed", "confirmed",
     [("confirmed", "viewed", "confirmed")]),
    *[
        ("operator", "confirm", {"level": "red", "status": s}, "sent_to_master", "confirmed",
         [("confirmed", s, "confirmed"), ("sent_to_master", "confirmed", "sent_to_master")])
        for s in ("new", "viewed", "confirmed")
    ],
    ("operator", "confirm", {"level": "red", **LATE}, "sent_to_master", "confirmed",
     [("confirmed", "sent_to_master", "sent_to_master")]),
    *[
        ("operator", "false_alarm", {"level": level, "status": s}, "false_alarm", "false_alarm",
         [("false_alarm", s, "false_alarm")])
        for level in ("yellow", "red")
        for s in ("new", "viewed", "confirmed")
    ],
    ("operator", "false_alarm", {"level": "red", **LATE}, "false_alarm", "false_alarm",
     [("false_alarm", "sent_to_master", "false_alarm")]),
    *[
        ("operator", "send_to_master", {"level": level, "status": s}, "sent_to_master",
         "confirmed", [("sent_to_master", s, "sent_to_master")])
        for level in ("yellow", "red")
        for s in ("new", "viewed", "confirmed")
    ],
    ("master", "accept", {"status": "sent_to_master"}, "master_accepted", "none",
     [("master_accepted", "sent_to_master", "master_accepted")]),
    ("master", "resolve", {"status": "master_accepted"}, "resolved", "none",
     [("resolved", "master_accepted", "resolved")]),
]  # fmt: skip


def journal(event_id: int) -> list[tuple[str, ...]]:
    rows = store.all("SELECT * FROM event_actions WHERE event_id = ? ORDER BY id", event_id)
    return [(r["actor_role"], r["action"], r["from_status"], r["to_status"]) for r in rows[1:]]


def row(event_id: int) -> dict[str, Any]:
    found = store.event(event_id)
    assert found is not None
    return dict(found)


@pytest.mark.parametrize(("role", "action", "before", "after", "verdict", "logged"), ROWS)
def test_transition_table(
    core: Settings,
    role: Role,
    action: HumanAction,
    before: dict[str, Any],
    after: str,
    verdict: str,
    logged: list[tuple[str, ...]],
) -> None:
    event_id = event(camera(), **before)
    operator, master = hub.connect("operator"), hub.connect("master")
    detail = services.event_action(event_id, ActionIn(action=action, comment="Меры"), role, None)
    assert isinstance(detail, EventDetail)
    found = row(event_id)
    assert (found["status"], found["operator_verdict"]) == (after, verdict)
    assert journal(event_id) == [(role, *entry) for entry in logged]
    assert detail.event.status == after
    updated = [(d["id"], d["status"]) for kind, d in drain(operator) if kind == "event.updated"]
    assert updated == [(event_id, after)]
    # The master hears of an event only when it comes to him (tech.md 8.8, row 3).
    to_master = after == "sent_to_master" and before.get("status") != "sent_to_master"
    notes = [d for kind, d in drain(master) if kind == "notification"]
    assert [(n["audience"], n["sound"], n["takeover"]) for n in notes] == (
        [(["master"], "chime", False)] if to_master else []
    )


def _allowed(action: HumanAction, level: str, status: str, late: bool) -> bool:
    """The (action, level, status) cells of the 8.6 table, written apart from the code."""
    open_ = status in ("new", "viewed", "confirmed")
    return {
        "view": status == "new",
        "confirm": (level == "red" and (open_ or late))
        or (level == "yellow" and status in ("new", "viewed")),
        "false_alarm": open_ or late,
        "send_to_master": open_,
        "accept": status == "sent_to_master",
        "resolve": status == "master_accepted",
    }[action]


def test_forbidden_transitions_conflict(core: Settings) -> None:
    camera_id, checked = camera(), 0
    roles = {a: r for r, actions in services.ROLE_ACTIONS.items() for a in actions}
    variants = [(s, {}) for s in get_args(EventStatus)] + [
        ("sent_to_master", {"escalated_by_timeout": 1, "operator_verdict": "confirmed"}),
        ("sent_to_master", {"escalated_by_timeout": 1}),
    ]
    for action, role in roles.items():
        for level in ("yellow", "red"):
            for status, extra in variants:
                late = extra == {"escalated_by_timeout": 1}
                if _allowed(action, level, status, late):
                    continue
                event_id = event(camera_id, level=level, status=status, **extra)
                with pytest.raises(Conflict) as caught:
                    services.event_action(
                        event_id, ActionIn(action=action, comment="x"), role, None
                    )
                assert caught.value.code == "invalid_transition"
                assert row(event_id)["status"] == status and journal(event_id) == []
                checked += 1
    assert checked > 80


async def test_roles_enforced(client: httpx.AsyncClient) -> None:
    event_id = event(camera())
    url = f"/api/events/{event_id}/actions"
    r = await client.post(url, json={"action": "confirm"}, headers=MASTER)
    assert (r.status_code, r.json()["code"]) == (403, "forbidden_role")
    r = await client.post(url, json={"action": "accept"}, headers=OPERATOR)
    assert (r.status_code, r.json()["code"]) == (403, "forbidden_role")
    r = await client.post(url, json={"action": "view"}, headers={"X-Role": "ohs"})
    assert r.status_code == 403
    r = await client.post(url, json={"action": "view"})
    assert (r.status_code, r.json()["code"]) == (400, "role_required")
    assert row(event_id)["status"] == "new" and journal(event_id) == []
    r = await client.post(url, json={"action": "view"}, headers=OPERATOR)
    assert (r.status_code, EventDetail.model_validate(r.json()).event.status) == (200, "viewed")
    r = await client.post(url, json={"action": "view"}, headers=OPERATOR)
    assert (r.status_code, r.json()["code"]) == (409, "invalid_transition")
    r = await client.post("/api/events/999/actions", json={"action": "view"}, headers=OPERATOR)
    assert r.status_code == 404


async def test_resolve_requires_comment(client: httpx.AsyncClient) -> None:
    camera_id = camera()

    async def resolve(comment: str) -> tuple[int, int, dict[str, Any]]:
        event_id = event(camera_id, status="master_accepted")
        body = {"action": "resolve", "comment": comment}
        r = await client.post(f"/api/events/{event_id}/actions", json=body, headers=MASTER)
        return r.status_code, event_id, r.json()

    for comment in ("", "   "):
        code, event_id, body = await resolve(comment)
        assert (code, ApiError.model_validate(body).message) == (422, texts.COMMENT_REQUIRED)
        assert row(event_id)["status"] == "master_accepted"
    code, event_id, _ = await resolve("я" * services.COMMENT_MAX)
    assert code == 200 and row(event_id)["status"] == "resolved"
    (saved,) = store.all("SELECT comment FROM event_actions WHERE action = 'resolved'")
    assert saved["comment"] == "я" * 500
    code, event_id, body = await resolve("я" * 501)
    assert (code, body["code"]) == (422, "validation")
    assert row(event_id)["status"] == "master_accepted"


async def test_actor_header_limits(client: httpx.AsyncClient) -> None:
    camera_id = camera()

    async def view(actor: str | None) -> tuple[int, int]:
        event_id = event(camera_id)
        headers = OPERATOR if actor is None else OPERATOR | {"X-Actor": quote(actor)}
        r = await client.post(
            f"/api/events/{event_id}/actions", json={"action": "view"}, headers=headers
        )
        return r.status_code, event_id

    def actor_name(event_id: int) -> str:
        found = store.one(
            "SELECT actor_name FROM event_actions WHERE action = 'viewed' AND event_id = ?",
            event_id,
        )
        assert found is not None
        return str(found["actor_name"])

    code, event_id = await view("Иван Петров")
    assert code == 200 and actor_name(event_id) == "Иван Петров"
    code, event_id = await view("Ж" * services.ACTOR_MAX)
    assert code == 200 and actor_name(event_id) == "Ж" * 60
    code, event_id = await view("Ж" * 61)
    assert code == 422 and row(event_id)["status"] == "new"
    code, event_id = await view(None)
    assert code == 200 and actor_name(event_id) == texts.DEMO_ACTOR["operator"]
