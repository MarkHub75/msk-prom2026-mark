"""Slice 8: the master inbox and notifications to the master (tech.md 8.6, 8.8)."""

from typing import Any

import httpx
import pytest
from conftest import FakeClock
from test_broadcast import EPISODE, at, camera, drain, playing, started
from test_event_actions import row
from test_jobs import _tune
from test_operator_views import event

from safewatch import clock, services, store
from safewatch.config import Settings
from safewatch.hub import hub
from safewatch.types import ActionIn, MasterInbox

MASTER, OPERATOR = {"X-Role": "master"}, {"X-Role": "operator"}
STATUSES = [
    "new", "viewed", "confirmed", "false_alarm", "sent_to_master", "master_accepted", "resolved",
    "auto_finished", "superseded",
]  # fmt: skip


def handed(event_id: int, action: str, at: str) -> None:
    """A journal row of the hand-over (or the resolution) of the event at `at`."""
    store.insert("event_actions", {
        "event_id": event_id, "at": at, "actor_role": "system", "actor_name": "система",
        "action": action, "from_status": "new", "to_status": "sent_to_master",
    })  # fmt: skip


def stamp(minute: int) -> str:
    return f"2026-10-24T08:{minute:02d}:00.000Z"


async def inbox(client: httpx.AsyncClient) -> MasterInbox:
    r = await client.get("/api/master/inbox")
    assert r.status_code == 200, r.text
    return MasterInbox.model_validate(r.json())


async def test_inbox_contains_only_master_statuses(client: httpx.AsyncClient) -> None:
    camera_id = camera()
    by_status = {s: event(camera_id, status=s) for s in STATUSES}
    handed(by_status["sent_to_master"], "sent_to_master", stamp(1))
    handed(by_status["master_accepted"], "sent_to_master", stamp(5))
    late_red = event(camera_id, level="red", status="sent_to_master", escalated_by_timeout=1)
    handed(late_red, "timeout_escalated", stamp(2))
    early_red = event(camera_id, level="red", status="master_accepted")
    handed(early_red, "sent_to_master", stamp(0))
    found = await inbox(client)
    # Red first, then the latest hand-over first; a timeout counts as a hand-over.
    assert [e.id for e in found.active] == [
        late_red,
        early_red,
        by_status["master_accepted"],
        by_status["sent_to_master"],
    ]
    assert [e.id for e in found.recent_resolved] == [by_status["resolved"]]
    assert found.server_now.tzinfo is not None


async def test_recent_resolved_limit(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    camera_id = camera()
    resolved = []
    for minute in range(21):
        resolved.append(event(camera_id, status="resolved"))
        handed(resolved[-1], "resolved", stamp(minute))
    newest = list(reversed(resolved))
    assert [e.id for e in (await inbox(client)).recent_resolved] == newest[:20]
    _tune(monkeypatch, core, master={"recent_resolved": 3})
    assert [e.id for e in (await inbox(client)).recent_resolved] == newest[:3]


def _alerts(messages: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    return [data for kind, data in messages if kind == "notification"]


def test_master_notification_on_send_and_timeout(core: Settings, fake_clock: FakeClock) -> None:
    operator, master = hub.connect("operator"), hub.connect("master")
    # By the operator.
    sent = event(camera(), status="viewed")
    services.event_action(sent, ActionIn(action="send_to_master"), "operator", None)
    (alert,) = _alerts(drain(master))
    assert (alert["id"], alert["audience"], alert["sound"]) == (
        f"e{sent}:to_master",
        ["master"],
        "chime",
    )
    assert alert["takeover"] is False and _alerts(drain(operator)) == []
    # By timeout, with the note for the master.
    now = clock.iso(fake_clock.now())
    late = event(camera(), level="red", red_at=now, published_at=now)
    fake_clock.advance(core.escalation.timeout_s)
    assert services.escalation_tick() == 1
    (alert,) = _alerts(drain(master))
    assert (alert["id"], alert["sound"]) == (f"e{late}:to_master", "chime")
    assert alert["text"].endswith(" · Не подтверждено оператором")
    assert _alerts(drain(operator)) == []
    # A view or a yellow confirm keeps the event with the operator: no message to the master.
    kept = event(camera())
    services.event_action(kept, ActionIn(action="view"), "operator", None)
    services.event_action(kept, ActionIn(action="confirm"), "operator", None)
    assert _alerts(drain(master)) == []


def test_master_notified_when_his_event_turns_red(core: Settings, fake_clock: FakeClock) -> None:
    """Row 4 of tech.md 8.8: a yellow event with the master escalates to red."""
    episode = {**EPISODE, "escalate_ms": 7000, "level_max": "red", "end_ms": 15_000}
    with_master, with_operator = playing([episode]), playing([episode])
    master = hub.connect("master")
    at(fake_clock, started(with_master), 5000)
    services.broadcast_tick()
    first, second = (
        store.all("SELECT id FROM events WHERE broadcast_id = ?", b)[0]["id"]
        for b in (with_master, with_operator)
    )
    # The detail of a broadcast event needs a full analysis: the status is set directly.
    store.event_update(first, {"status": "master_accepted", "operator_verdict": "confirmed"})
    drain(master)
    fake_clock.advance(2.0)
    services.broadcast_tick()
    assert row(first)["level"] == "red" and row(second)["level"] == "red"
    (alert,) = _alerts(drain(master))
    assert (alert["id"], alert["level"], alert["sound"]) == (
        f"e{first}:master_escalated",
        "red",
        "chime",
    )
    assert alert["takeover"] is False
