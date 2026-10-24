"""Slice 7: automatic escalation of a red event left by the operator (tech.md 8.7)."""

from datetime import timedelta
from typing import Any

import pytest
from conftest import FakeClock
from test_broadcast import camera, drain
from test_event_actions import journal, row
from test_jobs import _tune
from test_operator_views import event

from safewatch import clock, services, store, texts
from safewatch.config import Settings
from safewatch.hub import hub
from safewatch.types import ActionIn, HumanAction

TIMEOUT = [("system", "timeout_escalated", "new", "sent_to_master")]


def red(fake_clock: FakeClock, **values: Any) -> int:
    """A red event that turned red now."""
    now = clock.iso(fake_clock.now())
    return event(camera(), level="red", red_at=now, published_at=now, **values)


def operator_did(event_id: int, action: str, at_ms: int) -> None:
    """An operator journal row `at_ms` after `red_at`, written as the API would."""
    red_at = row(event_id)["red_at"]
    when = clock.iso(clock.parse(red_at) + timedelta(milliseconds=at_ms))
    store.insert("event_actions", {
        "event_id": event_id, "at": when, "actor_role": "operator", "actor_name": "Оператор",
        "action": action, "from_status": "confirmed", "to_status": "confirmed",
    })  # fmt: skip


@pytest.mark.parametrize("status", ["new", "viewed", "confirmed"])
def test_timeout_boundary_45s(core: Settings, fake_clock: FakeClock, status: str) -> None:
    event_id = red(fake_clock, status=status)
    # Not the operator's any more, or not red: the tick leaves them alone.
    others = [
        red(fake_clock, status=s) for s in ("sent_to_master", "master_accepted", "false_alarm")
    ] + [event(camera(), level="yellow", status="new")]
    operator, master = hub.connect("operator"), hub.connect("master")
    fake_clock.advance(44.9)
    assert services.escalation_tick() == 0 and row(event_id)["status"] == status
    fake_clock.advance(0.1)
    assert services.escalation_tick() == 1
    found = row(event_id)
    assert (found["status"], found["escalated_by_timeout"]) == ("sent_to_master", 1)
    assert journal(event_id) == [("system", "timeout_escalated", status, "sent_to_master")]
    notes = [d for kind, d in drain(master) if kind == "notification"]
    assert [(n["event_id"], n["audience"], n["sound"], n["takeover"]) for n in notes] == [
        (event_id, ["master"], "chime", False)
    ]
    assert notes[0]["text"].endswith(texts.NOT_CONFIRMED_SUFFIX)
    seen = drain(operator)
    assert [kind for kind, _ in seen] == ["event.updated"]
    assert seen[0][1]["escalated_by_timeout"] is True
    assert services.escalation_tick() == 0  # once
    assert [row(i)["status"] for i in others] == [
        "sent_to_master",
        "master_accepted",
        "false_alarm",
        "new",
    ]


def test_flag_off_no_escalation(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    _tune(monkeypatch, core, escalation={"enabled": False})
    event_id = red(fake_clock)
    fake_clock.advance(100)
    assert services.escalation_tick() == 0
    assert row(event_id)["status"] == "new" and journal(event_id) == []


def test_timeout_key_changes_behavior(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    _tune(monkeypatch, core, escalation={"timeout_s": 10})
    event_id = red(fake_clock)
    fake_clock.advance(9.9)
    assert services.escalation_tick() == 0
    fake_clock.advance(0.1)
    assert services.escalation_tick() == 1 and journal(event_id) == TIMEOUT


@pytest.mark.parametrize(
    ("action", "status"),
    [("confirm", "sent_to_master"), ("false_alarm", "false_alarm"),
     ("send_to_master", "sent_to_master"), ("view", "sent_to_master")],
)  # fmt: skip
def test_operator_action_before_deadline_prevents(
    core: Settings, fake_clock: FakeClock, action: HumanAction, status: str
) -> None:
    event_id = red(fake_clock)
    fake_clock.advance(10)
    services.event_action(event_id, ActionIn(action=action), "operator", None)
    fake_clock.advance(35)
    escalated = services.escalation_tick()
    found = row(event_id)
    assert (found["status"], found["escalated_by_timeout"]) == (status, int(action == "view"))
    assert escalated == int(action == "view")


@pytest.mark.parametrize(
    ("action", "at_ms", "escalates"),
    [("confirmed", 1, False), ("confirmed", 0, False), ("confirmed", -1, True),
     ("viewed", 1, True), ("false_alarm", 1, False), ("sent_to_master", 1, False)],
)  # fmt: skip
def test_decision_counts_only_after_red_at(
    core: Settings, fake_clock: FakeClock, action: str, at_ms: int, escalates: bool
) -> None:
    """A yellow confirmed before it turned red is no decision on the red (tech.md 8.7)."""
    event_id = red(fake_clock, status="confirmed")
    operator_did(event_id, action, at_ms)
    fake_clock.advance(45)
    assert services.escalation_tick() == int(escalates)


def test_operator_decision_after_escalation(core: Settings, fake_clock: FakeClock) -> None:
    confirmed, rejected = red(fake_clock), red(fake_clock)
    fake_clock.advance(45)
    assert services.escalation_tick() == 2
    operator, master = hub.connect("operator"), hub.connect("master")
    services.event_action(confirmed, ActionIn(action="confirm"), "operator", None)
    found = row(confirmed)
    assert (found["status"], found["operator_verdict"]) == ("sent_to_master", "confirmed")
    services.event_action(rejected, ActionIn(action="false_alarm"), "operator", None)
    found = row(rejected)
    assert (found["status"], found["operator_verdict"]) == ("false_alarm", "false_alarm")
    for client in (operator, master):  # the master card changes in place, no new alert
        seen = drain(client)
        assert [(kind, d["id"], d["status"]) for kind, d in seen] == [
            ("event.updated", confirmed, "sent_to_master"),
            ("event.updated", rejected, "false_alarm"),
        ]
    detail = services.event_detail(confirmed, "operator")
    assert detail.allowed_actions == []
