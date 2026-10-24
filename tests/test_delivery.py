"""Slices 15 and 23: webhook deliveries and the call to the master (tech.md 6.1, 6.2, 8.24).

`respx` stands for the webhooks; the call provider is the stub.
"""

import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
import yaml
from conftest import FakeClock
from test_broadcast import AT, at, camera, drain, playing, started
from test_escalation import red
from test_jobs import _tune
from test_operator_views import event

from safewatch import config, services, store
from safewatch.config import CallConfig, Settings, WebhookConfig
from safewatch.hub import hub
from safewatch.types import ActionIn, Level, SystemView

LAMP = "http://10.0.0.5/alarm"
CHIME = "http://10.0.0.6/chime"
KEYS = {"event_id", "kind", "level", "scenario", "title", "sector", "camera", "zone", "text", "at"}


def hooks(
    monkeypatch: pytest.MonkeyPatch, core: Settings, *channels: tuple[str, str, list[Level]]
) -> None:
    webhooks = [WebhookConfig(name=n, url=u, levels=lv, timeout_s=3) for n, u, lv in channels]
    _tune(monkeypatch, core, delivery={"webhooks": webhooks, "calls": []})


def bodies(route: respx.Route) -> list[dict[str, Any]]:
    return [json.loads(call.request.content) for call in route.calls]


def queue(event_id: int, kind: str, level: str) -> None:
    """A queue row as the core writes it (tech.md 8.24)."""
    store.delivery_enqueue(event_id, kind, level, AT)


def deliveries() -> list[dict[str, Any]]:
    return [dict(r) for r in store.all("SELECT * FROM deliveries ORDER BY id")]


@respx.mock
async def test_webhook_sent_on_red(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    hooks(monkeypatch, core, ("lamp-1", LAMP, ["red"]), ("chime", CHIME, ["yellow"]))
    lamp = respx.post(LAMP).mock(return_value=httpx.Response(200))
    chime = respx.post(CHIME).mock(return_value=httpx.Response(200))
    # A red fall at 5 s and a yellow run escalated at 7 s.
    b = playing([
        {"scenario": "fall", "level_initial": "red", "level_max": "red"},
        {"level_max": "red", "escalate_ms": 7000},
    ])  # fmt: skip
    t0 = started(b)
    at(fake_clock, t0, 5000)
    services.broadcast_tick()
    assert await services.deliveries_flush() == 2  # red to the lamp, yellow to the chime
    [published] = bodies(lamp)
    assert set(published) == KEYS
    assert (published["kind"], published["level"], published["scenario"]) == (
        "published",
        "red",
        "fall",
    )
    assert (published["sector"], published["camera"], published["zone"]) == (
        "Сектор 5 · Склад",
        "Камера",
        None,
    )
    assert published["text"].startswith("Красная опасность · Сектор 5 · ")
    assert [b["kind"] for b in bodies(chime)] == ["published"]
    at(fake_clock, t0, 7000)
    services.broadcast_tick()
    assert await services.deliveries_flush() == 1
    assert [(b["kind"], b["level"]) for b in bodies(lamp)][1:] == [("escalated", "red")]
    # The operator hands a red event to the master: a delivery of its own kind.
    broadcast = store.broadcast(b)
    assert broadcast is not None
    red = event(broadcast["camera_id"], level="red", red_at="2026-10-24T08:00:00.000Z")
    services.event_action(red, ActionIn(action="send_to_master"), "operator", None)
    assert await services.deliveries_flush() == 1
    assert (bodies(lamp)[-1]["kind"], bodies(lamp)[-1]["event_id"]) == ("to_master", red)
    assert {(d["channel"], d["status"], d["http_status"]) for d in deliveries()} == {
        ("webhook:lamp-1", "sent", 200),
        ("webhook:chime", "sent", 200),
    }


@pytest.mark.parametrize(
    ("answer", "status", "error"),
    [(httpx.Response(500), 500, "ответ HTTP 500"), (httpx.ConnectTimeout("slow"), None, "таймаут")],
)
@respx.mock
async def test_webhook_failure_recorded_event_unaffected(
    core: Settings, monkeypatch: pytest.MonkeyPatch, answer: Any, status: int | None, error: str
) -> None:
    hooks(monkeypatch, core, ("lamp-1", LAMP, ["red"]))
    route = respx.post(LAMP)
    route.mock(side_effect=answer) if isinstance(answer, Exception) else route.mock(
        return_value=answer
    )
    event_id = event(camera(), level="red")
    before = dict(store.one("SELECT * FROM events WHERE id = ?", event_id) or {})
    queue(event_id, "published", "red")
    assert await services.deliveries_flush() == 1
    [row] = deliveries()
    assert (row["status"], row["http_status"], row["error"]) == ("failed", status, error)
    assert dict(store.one("SELECT * FROM events WHERE id = ?", event_id) or {}) == before
    assert len(store.event_actions(event_id)) == 1


@respx.mock
async def test_delivery_idempotent(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    hooks(monkeypatch, core, ("lamp-1", LAMP, ["red"]))
    route = respx.post(LAMP).mock(return_value=httpx.Response(200))
    event_id = event(camera(), level="red")
    queue(event_id, "published", "red")
    queue(event_id, "published", "red")
    assert await services.deliveries_flush() == 1
    queue(event_id, "published", "red")
    assert await services.deliveries_flush() == 0
    assert route.call_count == 1 and len(deliveries()) == 1
    with pytest.raises(sqlite3.IntegrityError):
        store.insert("deliveries", {k: v for k, v in deliveries()[0].items() if k != "id"})


async def test_channels_in_system_view(
    core: Settings, monkeypatch: pytest.MonkeyPatch, client: httpx.AsyncClient
) -> None:
    secret = "http://user:pass@10.0.0.5:8080/alarm?token=s"
    hooks(monkeypatch, core, ("lamp-1", secret, ["red", "yellow"]))
    view = SystemView.model_validate((await client.get("/api/system")).json())
    assert [c.model_dump() for c in view.channels] == [
        {
            "name": "lamp-1",
            "kind": "webhook",
            "target": "10.0.0.5:8080",
            "levels": ["red", "yellow"],
        }
    ]
    assert "pass" not in (await client.get("/api/system")).text
    event_id = event(camera(), level="red")
    assert (await client.get(f"/api/events/{event_id}")).json()["deliveries"] == []
    with respx.mock:
        respx.post(host="10.0.0.5").mock(return_value=httpx.Response(200))
        queue(event_id, "published", "red")
        await services.deliveries_flush()
    [attempt] = (await client.get(f"/api/events/{event_id}")).json()["deliveries"]
    assert (attempt["channel"], attempt["kind"], attempt["status"]) == (
        "webhook:lamp-1",
        "published",
        "sent",
    )


@pytest.mark.parametrize("url", ["http://[::1", "ftp://host/x", "lamp.local/x", "http://h:99999/"])
def test_bad_webhook_url_fails_at_load(url: str) -> None:
    with pytest.raises(ValueError, match="url must be"):
        WebhookConfig(name="lamp", url=url, levels=["red"], timeout_s=1.0)


# --- slice 23: the call to the master, the queue in the base (tech.md 8.24) -----------------
def calls(
    monkeypatch: pytest.MonkeyPatch,
    core: Settings,
    to: str = "",
    levels: list[Level] | None = None,
    webhooks: list[WebhookConfig] | None = None,
) -> None:
    call = CallConfig(name="master", to=to, levels=levels or ["red"], provider="stub")
    _tune(monkeypatch, core, delivery={"webhooks": webhooks or [], "calls": [call]})


async def test_call_stub_on_red_to_master(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls(monkeypatch, core)
    master = hub.connect("master")
    # The operator confirms a red event: the confirm hands it to the master.
    confirmed = red(fake_clock)
    services.event_action(confirmed, ActionIn(action="confirm"), "operator", None)
    drain(master)
    assert await services.deliveries_flush() == 1
    [row] = deliveries()
    assert (row["channel"], row["kind"], row["status"], row["http_status"], row["error"]) == (
        "call:master", "to_master", "sent", None, "",
    )  # fmt: skip
    assert row["delivered_at"] == row["at"]
    assert [d["id"] for kind, d in drain(master) if kind == "event.updated"] == [confirmed]
    [attempt] = services.event_detail(confirmed, "master").deliveries
    assert attempt.status_text == "Звонок доставлен (заглушка)"
    # The same on the escalation by timeout.
    late = red(fake_clock)
    fake_clock.advance(core.escalation.timeout_s)
    assert services.escalation_tick() == 1
    assert await services.deliveries_flush() == 1
    assert [(d["event_id"], d["channel"], d["kind"]) for d in deliveries()][1:] == [
        (late, "call:master", "to_master")
    ]
    # A red publication and its escalation are no call: the call goes only with `to_master`.
    published = red(fake_clock)
    queue(published, "published", "red")
    queue(published, "escalated", "red")
    assert await services.deliveries_flush() == 0
    assert len(deliveries()) == 2 and store.delivery_queue() == []


@pytest.mark.parametrize(("levels", "rings"), [(["red"], 0), (["red", "yellow"], 1)])
async def test_yellow_send_no_call(
    core: Settings, monkeypatch: pytest.MonkeyPatch, levels: list[Level], rings: int
) -> None:
    calls(monkeypatch, core, levels=levels)
    yellow = event(camera())
    services.event_action(yellow, ActionIn(action="send_to_master"), "operator", None)
    assert [(r["kind"], r["level"]) for r in store.delivery_queue()] == [("to_master", "yellow")]
    assert await services.deliveries_flush() == rings
    assert len(deliveries()) == rings and store.delivery_queue() == []


@respx.mock
async def test_queue_survives_restart(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    lamp_hook = WebhookConfig(name="lamp-1", url=LAMP, levels=["red"], timeout_s=3)
    calls(monkeypatch, core, webhooks=[lamp_hook])
    lamp = respx.post(LAMP).mock(return_value=httpx.Response(200))
    monkeypatch.setattr(store, "_conn", None)  # the server base: a file in data_dir
    try:
        handed = event(camera(), level="red", red_at=AT)
        services.event_action(handed, ActionIn(action="confirm"), "operator", None)
        store.conn().close()
        # A new server process: new singletons on the same file, the queue is still there.
        monkeypatch.setattr(store, "_conn", None)
        assert [r["event_id"] for r in store.delivery_queue()] == [handed]
        assert await services.deliveries_flush() == 2
        assert {d["channel"] for d in deliveries()} == {"webhook:lamp-1", "call:master"}
        assert lamp.call_count == 1 and store.delivery_queue() == []
        assert await services.deliveries_flush() == 0
        assert lamp.call_count == 1 and len(deliveries()) == 2
    finally:
        store.conn().close()


@respx.mock
async def test_level_fixed_at_enqueue(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    hooks(monkeypatch, core, ("lamp-1", LAMP, ["red"]), ("chime", CHIME, ["yellow"]))
    lamp = respx.post(LAMP).mock(return_value=httpx.Response(200))
    chime = respx.post(CHIME).mock(return_value=httpx.Response(200))
    # A yellow run published at 5 s turns red at 7 s, both before one flush.
    b = playing([{"level_max": "red", "escalate_ms": 7000}])
    t0 = started(b)
    at(fake_clock, t0, 5000)
    services.broadcast_tick()
    at(fake_clock, t0, 7000)
    services.broadcast_tick()
    assert [(r["kind"], r["level"]) for r in store.delivery_queue()] == [
        ("published", "yellow"),
        ("escalated", "red"),
    ]
    assert await services.deliveries_flush() == 2
    assert [(b["kind"], b["level"]) for b in bodies(chime)] == [("published", "yellow")]
    assert [(b["kind"], b["level"]) for b in bodies(lamp)] == [("escalated", "red")]


@pytest.mark.parametrize(
    ("webhooks", "fails"), [(["master"], True), (["lamp-1", "lamp-1"], True), (["lamp-1"], False)]
)
def test_duplicate_channel_names_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, webhooks: list[str], fails: bool
) -> None:
    # Tests never read user.yaml (conftest): the owner's file goes in place of user.example.yaml.
    shutil.copy(config.CONFIG_DIR / "default.yaml", tmp_path / "default.yaml")
    hook = {"url": LAMP, "levels": ["red"], "timeout_s": 3}
    user = {"delivery": {"webhooks": [{"name": n, **hook} for n in webhooks]}}
    (tmp_path / "user.example.yaml").write_text(yaml.safe_dump(user), encoding="utf-8")
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    if not fails:  # the default call `master` and a webhook of another name load
        assert [w.name for w in config.get_settings.__wrapped__().delivery.webhooks] == webhooks
        return
    with pytest.raises(ValueError, match="delivery: channel names must be unique"):
        config.get_settings.__wrapped__()


@pytest.mark.parametrize(
    ("to", "target"),
    [("+7 (900) 123-45-12", "+7 900 ***-**-12"), ("900-12", "***-**-12"), ("", "заглушка")],
)
async def test_call_channel_in_system_view(
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    client: httpx.AsyncClient,
    to: str,
    target: str,
) -> None:
    calls(monkeypatch, core, to=to)
    view = SystemView.model_validate((await client.get("/api/system")).json())
    assert [c.model_dump() for c in view.channels] == [
        {"name": "master", "kind": "call", "target": target, "levels": ["red"]}
    ]
    handed = event(camera(), level="red")
    services.event_action(handed, ActionIn(action="send_to_master"), "operator", None)
    await services.deliveries_flush()
    [row] = (await client.get(f"/api/events/{handed}")).json()["deliveries"]
    assert (row["channel"], row["kind"], row["status"], row["status_text"]) == (
        "call:master", "to_master", "sent", "Звонок доставлен (заглушка)",
    )  # fmt: skip
    assert row["delivered_at"] == row["at"]
    # A call row without `delivered_at` (a provider that only dials) reads «Звонок отправлен».
    store.run("UPDATE deliveries SET delivered_at = NULL")
    [row] = (await client.get(f"/api/events/{handed}")).json()["deliveries"]
    assert (row["delivered_at"], row["status_text"]) == (None, "Звонок отправлен")
