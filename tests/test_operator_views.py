"""Slice 6: camera and sector states (tech.md 8.9), the feed (8.8), operator screens, preview."""

from datetime import timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest
from conftest import FakeClock
from test_broadcast import AT, at, camera, drain, hud_file, playing, ready_video, started
from test_jobs import _tune

from safewatch import clock, media, services, store
from safewatch.config import Settings
from safewatch.hub import hub
from safewatch.types import (
    BroadcastIn,
    CameraIn,
    CameraLiveView,
    OperatorDashboard,
    SectorIn,
    SectorView,
)


def event(camera_id: int, **values: Any) -> int:
    """An event row of the camera; `last_action_at` dates its only action."""
    row = store.one("SELECT sector_id FROM cameras WHERE id = ?", camera_id)
    assert row is not None
    last = values.pop("last_action_at", AT)
    n = store.one("SELECT count(*) FROM events")[0]  # type: ignore[index]
    base = {
        "pub_key": f"t:{n}",
        "camera_id": camera_id,
        "sector_id": row["sector_id"],
        "scenario": "running",
        "title": "Бег и резкие перемещения",
        "reason_text": "Бег 2,4 роста/с",
        "level": "yellow",
        "status": "new",
        "started_at": AT,
        "published_at": AT,
    }
    with store.tx():
        event_id = store.insert("events", base | values)
        store.insert("event_actions", {
            "event_id": event_id, "at": last, "actor_role": "system", "actor_name": "система",
            "action": "published", "to_status": "new",
        })  # fmt: skip
    return event_id


def job(camera_id: int, status: str) -> None:
    video = ready_video(camera_id, [])
    store.insert("jobs", {
        "kind": "process", "video_id": video, "backend": "linq", "fake": 1, "status": status,
        "stage": "queued", "created_at": AT,
    })  # fmt: skip


def broadcast(camera_id: int, status: str) -> None:
    video = ready_video(camera_id, [])
    services.broadcast_start(camera_id, BroadcastIn(video_id=video), "admin")
    if status != "playing":
        store.run("UPDATE broadcasts SET status = ? WHERE camera_id = ?", status, camera_id)


SETUPS: dict[str, Any] = {
    "red": lambda c: event(c, level="red", red_at=AT),
    "red_closed": lambda c: event(c, level="red", status="false_alarm"),
    "yellow": lambda c: event(c),
    "yellow_ended": lambda c: event(c, ended_at=AT),
    "yellow_closed": lambda c: event(c, status="auto_finished"),
    "processing": lambda c: job(c, "queued"),
    "retry_wait": lambda c: job(c, "retry_wait"),
    "failed": lambda c: job(c, "failed"),
    "ended": lambda c: broadcast(c, "ended"),
    "stopped": lambda c: broadcast(c, "stopped"),
    "playing": lambda c: broadcast(c, "playing"),
}


@pytest.mark.parametrize(
    ("setup", "state", "reason"),
    [
        (["red", "yellow", "processing"], "red", None),
        (["red_closed", "yellow", "failed"], "yellow", None),
        (["yellow", "processing"], "yellow", None),
        (["yellow_ended", "yellow_closed", "processing"], "no_observation", "processing"),
        (["retry_wait", "failed"], "no_observation", "processing"),
        (["failed", "ended"], "no_observation", "failed"),
        (["ended"], "no_observation", "ended"),
        (["stopped"], "no_observation", "no_source"),
        ([], "no_observation", "no_source"),
        (["yellow_ended", "playing"], "normal", None),
        (["failed", "playing"], "normal", None),
    ],
)
def test_camera_state_precedence(
    core: Settings, setup: list[str], state: str, reason: str | None
) -> None:
    camera_id = camera()
    for name in setup:
        SETUPS[name](camera_id)
    (found,) = services.camera_states()
    assert (found.camera_id, found.state, found.reason) == (camera_id, state, reason)
    if reason is not None:
        assert found.reason_text == services.texts.NO_OBSERVATION_TEXTS[reason]  # type: ignore[index]


def test_sector_states(core: Settings) -> None:
    red, yellow, blind, empty = (
        services.sector_create(SectorIn(name=n), "admin").id
        for n in ("Красный", "Жёлтый", "Слепой", "Пустой")
    )

    def cam(sector_id: int) -> int:
        return services.camera_create(CameraIn(sector_id=sector_id, name="К"), "admin").id

    event(cam(red), level="red")
    cam(red)
    event(cam(yellow))
    broadcast(cam(yellow), "playing")
    seen, unseen = cam(blind), cam(blind)
    broadcast(seen, "playing")
    view = services.operator_dashboard_view()
    by_id = {s.sector_id: s for s in view.sectors}
    assert (by_id[red].state, by_id[red].open_red) == ("red", 1)
    assert (by_id[yellow].state, by_id[yellow].open_yellow) == ("yellow", 1)
    assert (by_id[blind].state, by_id[blind].reason_text) == (
        "no_observation",
        "Нет наблюдения: 1 из 2 камер",
    )
    assert (by_id[blind].cameras_total, by_id[blind].cameras_no_observation) == (2, 1)
    assert (by_id[empty].state, by_id[empty].cameras_total) == ("no_observation", 0)
    broadcast(unseen, "playing")
    (normal,) = [s for s in services.operator_dashboard_view().sectors if s.sector_id == blind]
    assert (normal.state, normal.reason_text) == ("normal", "Норма")


def test_state_changes_published(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([{}])
    t0 = started(b)
    ws = hub.connect("operator")
    at(fake_clock, t0, 1000)
    services.broadcast_tick()
    first = drain(ws)
    assert [k for k, _ in first] == ["camera.state", "sector.state"]
    assert first[0][1]["state"] == "normal"
    at(fake_clock, t0, 2000)
    services.broadcast_tick()
    assert drain(ws) == []
    at(fake_clock, t0, 5000)
    services.broadcast_tick()
    states = [(k, d["state"]) for k, d in drain(ws) if k.endswith(".state")]
    assert states == [("camera.state", "yellow"), ("sector.state", "yellow")]


def test_feed_priority_order(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    c = camera()
    now = fake_clock.now()

    def ago(minutes: float) -> str:
        return clock.iso(now - timedelta(minutes=minutes))

    other = event(c, status="confirmed", published_at=ago(1))
    yellow_old = event(c, published_at=ago(5))
    yellow_new = event(c, status="viewed", published_at=ago(2))
    red = event(c, level="red", published_at=ago(10))
    red_confirmed = event(c, level="red", status="confirmed", published_at=ago(0.5))
    closed_in = event(c, status="false_alarm", published_at=ago(40), last_action_at=ago(29.9))
    event(c, status="resolved", published_at=ago(40), last_action_at=ago(30.1))
    event(c, status="superseded", published_at=ago(0))
    feed = services.operator_feed()
    assert [e.id for e in feed] == [red, yellow_new, yellow_old, red_confirmed, other, closed_in]
    assert [e.priority for e in feed] == [3, 2, 2, 1, 1, 0]
    _tune(monkeypatch, core, feed={"limit": 2})
    assert [e.id for e in services.operator_feed()] == [red, yellow_new]
    _tune(monkeypatch, core, feed={"recent_closed_min": 60})
    assert len(services.operator_feed()) == 7


async def test_dashboard_and_sector_view_shape(
    client: httpx.AsyncClient, core: Settings, fake_clock: FakeClock
) -> None:
    b = playing([{}])
    at(fake_clock, started(b), 5000)
    services.broadcast_tick()
    camera_id = store.broadcast(b)["camera_id"]  # type: ignore[index]
    r = await client.get("/api/operator/dashboard")
    assert r.status_code == 200
    dashboard = OperatorDashboard.model_validate(r.json())
    (sector,) = dashboard.sectors
    assert (sector.state, sector.open_yellow) == ("yellow", 1)
    (item,) = dashboard.feed
    assert item.notification_text == "Жёлтая опасность · Сектор 5 · Бег 2,4 роста/с"
    assert item.duration_s == 2.0  # the episode goes on: now - started_at
    assert (await client.get("/api/operator/feed")).json() == r.json()["feed"]
    view = SectorView.model_validate(
        (await client.get(f"/api/sectors/{sector.sector_id}/view")).json()
    )
    (tile,) = view.cameras
    assert tile.camera.id == camera_id and tile.state.state == "yellow"
    assert tile.broadcast is not None and tile.broadcast.id == b
    assert tile.preview_url == f"/api/cameras/{camera_id}/preview"
    assert [e.id for e in view.feed] == [item.id]
    assert (await client.get("/api/sectors/999/view")).status_code == 404


async def test_camera_live_view_shape(
    client: httpx.AsyncClient, core: Settings, fake_clock: FakeClock
) -> None:
    b = playing([{}])
    camera_id = store.broadcast(b)["camera_id"]  # type: ignore[index]
    r = await client.get(f"/api/cameras/{camera_id}/view")
    assert r.status_code == 200, r.text
    view = CameraLiveView.model_validate(r.json())
    assert view.broadcast is not None and view.broadcast.id == b
    assert view.video is not None and view.video.id == view.broadcast.video_id
    assert view.analysis is not None and [e.scenario for e in view.analysis.episodes] == ["running"]
    assert view.state.state == "normal" and view.zones == [] and view.calibration is None
    empty = camera()
    bare = CameraLiveView.model_validate((await client.get(f"/api/cameras/{empty}/view")).json())
    assert (bare.broadcast, bare.video, bare.analysis) == (None, None, None)
    assert (await client.get("/api/cameras/999/view")).status_code == 404


async def test_preview_jpeg(
    client: httpx.AsyncClient,
    core: Settings,
    fake_clock: FakeClock,
    make_video,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    camera_id = camera()
    url = f"/api/cameras/{camera_id}/preview"
    assert (await client.get(url)).status_code == 404
    video = services.video_import(camera_id, make_video(tmp_path, 2, 10)).video
    assert (await client.get(url)).status_code == 404  # not ready yet
    store.video_update(video.id, {"status": "ready"})
    reads: list[int] = []
    real = media.read_frame

    def counted(path: Path, frame_idx: int) -> Any:
        reads.append(frame_idx)
        return real(path, frame_idx)

    monkeypatch.setattr(media, "read_frame", counted)
    r = await client.get(url)
    assert r.status_code == 200 and r.headers["content-type"] == "image/jpeg"
    assert r.content[:2] == b"\xff\xd8" and reads == [0]
    fake_clock.advance(core.preview.cache_s - 0.001)
    assert (await client.get(url)).content == r.content and reads == [0]
    fake_clock.advance(0.001)
    await client.get(url)
    assert reads == [0, 0]
    # A playing broadcast: the frame at its position.
    with store.tx():
        artifact = store.insert("artifacts", {
            "cache_key": "k", "video_sha256": "h", "model_id": "m", "model_version": "v",
            "task": "detect", "input_size": 640, "step": 1, "backend": "linq", "fake": 1,
            "path": "p", "frames": 1, "metrics_json": "{}", "created_at": AT,
        })  # fmt: skip
        analysis = store.insert("analyses", {
            "video_id": video.id, "version": 1, "det_artifact_id": artifact, "config_json": "{}",
            "hud_path": hud_file("h", [0, 1000]), "gaps_json": "[]", "duration_ms": 2000,
            "created_at": AT,
        })  # fmt: skip
        store.video_update(video.id, {"active_analysis_id": analysis})
    services.broadcast_start(camera_id, BroadcastIn(), "admin")
    store.run("UPDATE broadcasts SET position_ms = 1000")
    fake_clock.advance(core.preview.cache_s)
    await client.get(url)
    assert reads[-1] == 10  # 1.0 s at 10 fps
