"""Slice 15: webhook deliveries to outside systems (tech.md 6.1, 6.2); `respx` stands for them."""

import json
import sqlite3
from typing import Any

import httpx
import pytest
import respx
from conftest import FakeClock
from test_broadcast import at, camera, playing, started
from test_jobs import _tune
from test_operator_views import event

from safewatch import services, store
from safewatch.config import Settings, WebhookConfig
from safewatch.types import ActionIn, Level, SystemView

LAMP = "http://10.0.0.5/alarm"
CHIME = "http://10.0.0.6/chime"
KEYS = {"event_id", "kind", "level", "scenario", "title", "sector", "camera", "zone", "text", "at"}


def hooks(
    monkeypatch: pytest.MonkeyPatch, core: Settings, *channels: tuple[str, str, list[Level]]
) -> None:
    webhooks = [WebhookConfig(name=n, url=u, levels=lv, timeout_s=3) for n, u, lv in channels]
    _tune(monkeypatch, core, delivery={"webhooks": webhooks})


def bodies(route: respx.Route) -> list[dict[str, Any]]:
    return [json.loads(call.request.content) for call in route.calls]


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
    services._deliveries.append((event_id, "published"))
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
    services._deliveries.extend([(event_id, "published"), (event_id, "published")])
    assert await services.deliveries_flush() == 1
    services._deliveries.append((event_id, "published"))
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
        services._deliveries.append((event_id, "published"))
        await services.deliveries_flush()
    [attempt] = (await client.get(f"/api/events/{event_id}")).json()["deliveries"]
    assert (attempt["channel"], attempt["kind"], attempt["status"]) == (
        "webhook:lamp-1",
        "published",
        "sent",
    )
