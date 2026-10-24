"""Slice 6: the broadcast of tech.md 8.5 on the fake clock; ticks are called directly."""

import json
from datetime import timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest
from conftest import FakeClock
from test_jobs import _tune, _video

from safewatch import clock, services, store
from safewatch.config import Settings
from safewatch.hub import Client, hub
from safewatch.types import ApiError, Broadcast, BroadcastIn, CameraIn, SectorIn

ADMIN, OPERATOR = {"X-Role": "admin"}, {"X-Role": "operator"}
AT = "2026-10-24T08:00:00.000Z"

EPISODE: dict[str, Any] = {
    "scenario": "running",
    "subject": "track:1",
    "level_initial": "yellow",
    "level_max": "yellow",
    "start_ms": 3000,
    "confirm_ms": 5000,
    "escalate_ms": None,
    "end_ms": 9000,
    "end_reason": "observed_exit",
    "reason_code": "running",
    "reason_text": "Бег 2,4 роста/с",
    "method": "relative",
    "confidence": 0.9,
    "metrics_json": "{}",
}


def ready_video(camera_id: int, episodes: list[dict[str, Any]], duration_ms: int = 20_000) -> int:
    """A ready video of the camera with an active analysis holding `episodes`."""
    with store.tx():
        n = store.one("SELECT count(*) FROM videos")[0]  # type: ignore[index]
        video = store.insert("videos", {
            "camera_id": camera_id, "filename": "a.mp4", "sha256": f"h{n}",
            "path": f"uploads/h{n}.mp4", "size_bytes": 1, "width": 2, "height": 2, "fps": 10,
            "frame_count": duration_ms // 100, "duration_ms": duration_ms, "codec": "avc1",
            "browser_playable": 1, "status": "ready", "created_at": AT,
        })  # fmt: skip
        artifact = store.insert("artifacts", {
            "cache_key": f"k{n}", "video_sha256": f"h{n}", "model_id": "m", "model_version": "v",
            "task": "detect", "input_size": 640, "step": 1, "backend": "linq", "fake": 1,
            "path": "p", "frames": 1, "metrics_json": "{}", "created_at": AT,
        })  # fmt: skip
        analysis = store.insert("analyses", {
            "video_id": video, "version": 1, "det_artifact_id": artifact, "config_json": "{}",
            "hud_path": "h", "gaps_json": "[]", "duration_ms": duration_ms, "created_at": AT,
        })  # fmt: skip
        for ep in episodes:
            store.insert("episodes", {**EPISODE, **ep, "analysis_id": analysis})
        store.video_update(video, {"active_analysis_id": analysis})
    return video


def camera(sector: str = "Сектор 5 · Склад") -> int:
    found = [s for s in services.sectors_list() if s.name == sector]
    sector_id = found[0].id if found else services.sector_create(SectorIn(name=sector), "admin").id
    return services.camera_create(CameraIn(sector_id=sector_id, name="Камера"), "admin").id


def playing(episodes: list[dict[str, Any]], loop: bool = False, duration_ms: int = 20_000) -> int:
    camera_id = camera()
    ready_video(camera_id, episodes, duration_ms)
    return services.broadcast_start(camera_id, BroadcastIn(loop=loop), "admin").id


def drain(client: Client) -> list[tuple[str, dict[str, Any]]]:
    out = []
    while not client.queue.empty():
        message = json.loads(client.queue.get_nowait() or "{}")
        out.append((message["type"], message["data"]))
    return out


def events() -> list[dict[str, Any]]:
    return [dict(r) for r in store.all("SELECT * FROM events ORDER BY id")]


def actions(event_id: int) -> list[tuple[str, str, str | None, str | None]]:
    rows = store.all("SELECT * FROM event_actions WHERE event_id = ? ORDER BY id", event_id)
    return [(r["actor_role"], r["action"], r["from_status"], r["to_status"]) for r in rows]


def at(fake_clock: FakeClock, start: str, ms: int) -> None:
    fake_clock.current = clock.parse(start) + timedelta(milliseconds=ms)


def started(broadcast_id: int) -> str:
    row = store.broadcast(broadcast_id)
    assert row is not None
    return str(row["started_at"])


@pytest.mark.parametrize(("initial", "sound"), [("yellow", "chime"), ("red", "siren")])
def test_publish_at_confirm_time_not_before(
    core: Settings, fake_clock: FakeClock, initial: str, sound: str
) -> None:
    b = playing([{"level_initial": initial, "level_max": initial}])
    t0 = started(b)
    ws = hub.connect("operator")
    at(fake_clock, t0, 4999)
    assert services.broadcast_tick() == 0 and events() == []
    drain(ws)
    at(fake_clock, t0, 5000)
    assert services.broadcast_tick() == 1
    (event,) = events()
    assert (event["status"], event["level"], event["cycle"]) == ("new", initial, 0)
    assert event["pub_key"] == f"b{b}:c0:e{event['episode_id']}"
    assert event["started_at"] == clock.iso(clock.parse(t0) + timedelta(seconds=3))
    assert event["published_at"] == clock.iso(fake_clock.now())
    assert event["red_at"] == (clock.iso(fake_clock.now()) if initial == "red" else None)
    assert event["ended_at"] is None
    assert actions(event["id"]) == [("system", "published", None, "new")]
    sent = drain(ws)
    kinds = [kind for kind, _ in sent]
    assert kinds[:2] == ["event.created", "notification"]
    assert sent[0][1]["id"] == event["id"] and sent[0][1]["level"] == initial
    note = sent[1][1]
    assert (note["sound"], note["takeover"], note["audience"]) == (
        sound,
        initial == "red",
        ["operator"],
    )


def test_tick_is_idempotent_across_restart(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    b = playing([{}])
    t0 = started(b)
    at(fake_clock, t0, 5000)
    assert services.broadcast_tick() == 1
    assert services.broadcast_tick() == 0
    # A restart: the lazy singletons of services start empty, the database stays.
    for name in ("_camera_seen", "_sector_seen", "_preview_cache"):
        monkeypatch.setattr(services, name, {})
    assert services.broadcast_tick() == 0
    at(fake_clock, t0, 6000)
    assert services.broadcast_tick() == 0
    assert len(events()) == 1 and started(b) == t0


def test_escalation_updates_same_event(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([{"escalate_ms": 7000, "level_max": "red", "end_ms": 12_000}])
    t0 = started(b)
    at(fake_clock, t0, 5000)
    services.broadcast_tick()
    (yellow,) = events()
    ws = hub.connect("operator")
    at(fake_clock, t0, 6999)
    assert services.broadcast_tick() == 0 and events()[0]["level"] == "yellow"
    at(fake_clock, t0, 7000)
    assert services.broadcast_tick() == 1
    (red,) = events()
    assert (red["id"], red["level"], red["status"]) == (yellow["id"], "red", "new")
    assert red["red_at"] == clock.iso(fake_clock.now())
    assert actions(red["id"])[-1] == ("system", "level_escalated", "new", "new")
    sent = drain(ws)
    assert [k for k, _ in sent][:2] == ["event.escalated", "notification"]
    note = sent[1][1]
    assert (note["level"], note["sound"], note["takeover"]) == ("red", "siren", True)
    # Published after the escalation moment: red at once, one action.
    late = playing([{"escalate_ms": 7000, "level_max": "red", "end_ms": 12_000}])
    at(fake_clock, started(late), 8000)
    services.broadcast_tick()
    (event,) = [e for e in events() if e["broadcast_id"] == late]
    assert event["level"] == "red" and actions(event["id"]) == [
        ("system", "published", None, "new")
    ]


@pytest.mark.parametrize(
    ("before", "after"),
    [("new", "auto_finished"), ("viewed", "auto_finished"), ("confirmed", "confirmed")],
)
def test_yellow_auto_finishes_red_stays(
    core: Settings, fake_clock: FakeClock, before: str, after: str
) -> None:
    red = {"level_initial": "red", "level_max": "red", "confirm_ms": 6000, "end_ms": 12_000}
    b = playing([{}, red])
    t0 = started(b)
    at(fake_clock, t0, 6000)
    services.broadcast_tick()
    yellow_id, red_id = (e["id"] for e in events())
    store.event_update(yellow_id, {"status": before})
    ws = hub.connect("operator")
    at(fake_clock, t0, 8999)
    services.broadcast_tick()
    assert events()[0]["ended_at"] is None
    at(fake_clock, t0, 9000)
    services.broadcast_tick()
    yellow = events()[0]
    assert yellow["ended_at"] == clock.iso(clock.parse(t0) + timedelta(seconds=9))
    assert yellow["status"] == after
    finished = [a for a in actions(yellow_id) if a[1] == "auto_finished"]
    assert finished == ([("system", "auto_finished", before, after)] if after != before else [])
    assert ("event.updated", yellow_id) in [(k, d.get("id")) for k, d in drain(ws)]
    at(fake_clock, t0, 12_000)
    services.broadcast_tick()
    red_row = events()[1]
    assert red_row["ended_at"] is not None and red_row["status"] == "new"
    assert [a[1] for a in actions(red_id)] == ["published"]


def test_loop_cycle_republishes(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([{}], loop=True, duration_ms=10_000)
    t0 = started(b)
    ws = hub.connect("operator")
    at(fake_clock, t0, 5000)
    services.broadcast_tick()
    at(fake_clock, t0, 14_999)
    services.broadcast_tick()
    assert [e["cycle"] for e in events()] == [0]
    assert events()[0]["ended_at"] is not None  # cycle 0 played out to D
    states = [d for k, d in drain(ws) if k == "broadcast.state"]
    assert [(s["cycle"], s["status"]) for s in states] == [(1, "playing")]
    at(fake_clock, t0, 15_000)
    services.broadcast_tick()
    second = events()[1]
    assert (second["cycle"], second["pub_key"]) == (1, f"b{b}:c1:e{second['episode_id']}")
    assert second["started_at"] == clock.iso(clock.parse(t0) + timedelta(seconds=13))
    # The server was off for whole cycles: 2 and 3 are skipped, 1 finishes, 4 plays.
    at(fake_clock, t0, 45_000)
    services.broadcast_tick()
    assert [e["cycle"] for e in events()] == [0, 1, 4]


def test_loop_off_ends_broadcast(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([{}], loop=False, duration_ms=10_000)
    t0 = started(b)
    camera_id = camera_by_broadcast(b)
    at(fake_clock, t0, 9999)
    services.broadcast_tick()
    assert store.broadcast(b)["status"] == "playing"  # type: ignore[index]
    at(fake_clock, t0, 10_000)
    services.broadcast_tick()
    row = store.broadcast(b)
    assert row is not None and (row["status"], row["position_ms"]) == ("ended", 10_000)
    (state,) = [s for s in services.camera_states() if s.camera_id == camera_id]
    assert (state.state, state.reason, state.reason_text) == (
        "no_observation",
        "ended",
        "Запись закончилась",
    )
    at(fake_clock, t0, 15_000)
    assert services.broadcast_tick() == 0 and len(events()) == 1


def camera_by_broadcast(broadcast_id: int) -> int:
    row = store.broadcast(broadcast_id)
    assert row is not None
    return int(row["camera_id"])


def test_stop_halts_publication(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([{}])
    t0 = started(b)
    camera_id = camera_by_broadcast(b)
    ws = hub.connect("operator")
    services.broadcast_stop(camera_id, "admin")
    row = store.broadcast(b)
    assert row is not None and row["status"] == "stopped" and row["stopped_at"]
    assert [(k, d["status"]) for k, d in drain(ws)] == [("broadcast.state", "stopped")]
    at(fake_clock, t0, 6000)
    assert services.broadcast_tick() == 0 and events() == []


async def test_autostart_after_job(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    video_id = _video(tmp_path, make_video)
    camera_id = services.video_get(video_id).camera_id
    ws = hub.connect("admin")
    await services.run_next_job()
    first = services.broadcast_get(camera_id)
    assert first is not None and (first.video_id, first.status) == (video_id, "playing")
    assert first.loop is fake_core.broadcast.loop_default
    assert ("broadcast.state", first.id) in [(k, d.get("id")) for k, d in drain(ws)]
    # A playing broadcast is kept when another video of the camera gets processed.
    clip = make_video(tmp_path, 2, 25, name="second.mp4")
    services.video_import(camera_id, clip)
    await services.run_next_job()
    kept = services.broadcast_get(camera_id)
    assert kept is not None and (kept.id, kept.video_id, kept.status) == (
        first.id,
        video_id,
        "playing",
    )
    # Autostart off: no broadcast for a camera without one.
    _tune(monkeypatch, fake_core, broadcast={"autostart": False})
    (tmp_path / "other").mkdir()
    other = _video(tmp_path / "other", make_video, camera="Камера 2")
    other_camera = services.video_get(other).camera_id
    await services.run_next_job()
    assert services.video_get(other).status == "ready"
    assert services.broadcast_get(other_camera) is None


def _error(r: httpx.Response, status: int, code: str) -> None:
    assert r.status_code == status, r.text
    assert ApiError.model_validate(r.json()).code == code


async def test_start_stop_conflicts_and_messages(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    camera_id = camera()
    url = f"/api/cameras/{camera_id}/broadcast"
    assert (await client.get(url)).json() is None
    _error(await client.post(url, json={}, headers=ADMIN), 409, "no_ready_video")
    pending = ready_video(camera_id, [])
    store.video_update(pending, {"status": "processing"})
    body = {"video_id": pending}
    _error(await client.post(url, json=body, headers=ADMIN), 409, "video_not_ready")
    store.video_update(pending, {"status": "ready"})
    _error(await client.post(url, json={}, headers=OPERATOR), 403, "forbidden_role")
    _error(await client.post(url, json={}), 400, "role_required")
    _error(
        await client.post("/api/cameras/999/broadcast", json={}, headers=ADMIN), 404, "not_found"
    )
    _error(await client.get("/api/cameras/999/broadcast"), 404, "not_found")
    _error(await client.delete(url, headers=OPERATOR), 403, "forbidden_role")

    ws = hub.connect("operator")
    r = await client.post(url, json={}, headers=ADMIN)
    assert r.status_code == 201
    first = Broadcast.model_validate(r.json())
    assert (first.video_id, first.status, first.loop) == (pending, "playing", True)
    assert Broadcast.model_validate((await client.get(url)).json()).id == first.id
    assert [(k, d["id"], d["status"]) for k, d in drain(ws)] == [
        ("broadcast.state", first.id, "playing")
    ]
    # loop follows broadcast.loop_default when the request leaves it out.
    _tune(monkeypatch, core, broadcast={"loop_default": False})
    second = Broadcast.model_validate((await client.post(url, json={}, headers=ADMIN)).json())
    assert (second.status, second.loop) == ("playing", False)
    assert store.broadcast(first.id)["status"] == "stopped"  # type: ignore[index]
    assert [(k, d["id"], d["status"]) for k, d in drain(ws)] == [
        ("broadcast.state", first.id, "stopped"),
        ("broadcast.state", second.id, "playing"),
    ]
    assert (await client.delete(url, headers=ADMIN)).status_code == 204
    assert [(k, d["status"]) for k, d in drain(ws)] == [("broadcast.state", "stopped")]
    # camera_delete stops a playing broadcast and says so over WS (note R10 of S1).
    third = Broadcast.model_validate((await client.post(url, json={}, headers=ADMIN)).json())
    drain(ws)
    assert (await client.delete(f"/api/cameras/{camera_id}", headers=ADMIN)).status_code == 204
    assert [(k, d["id"], d["status"]) for k, d in drain(ws)] == [
        ("broadcast.state", third.id, "stopped")
    ]
