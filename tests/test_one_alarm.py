"""UPGRADE v3 stage 2: one incident, one alarm on the default single play (tech.md 8.5, 8.7, 8.24).

The synthetic case pins the counts per event; the real case replays the cached LinQ detections
of the selected demo pack `argus-real-v2` (skipped where the pack is not unpacked, e.g. CI).
"""

import shutil
from collections import Counter
from datetime import timedelta
from typing import Any

import httpx
import pytest
import respx
from conftest import FakeClock
from test_broadcast import camera, drain, events, ready_video, started
from test_delivery import LAMP, deliveries
from test_demo_pack import _shell
from test_jobs import _tune

from safewatch import clock, config, services, store
from safewatch.config import ROOT, CallConfig, Settings, WebhookConfig
from safewatch.hub import Client, hub
from safewatch.types import ActionIn, BroadcastIn, EventFilter, ZoneIn

PACK = ROOT / "data" / "demo" / "argus-real-v2"
YELLOW_TO_RED = {"escalate_ms": 7000, "level_max": "red", "end_ms": 12_000}
RED = {"level_initial": "red", "level_max": "red", "confirm_ms": 6000, "end_ms": 12_000}


def channels(monkeypatch: pytest.MonkeyPatch, core: Settings) -> None:
    """A red lamp webhook and the call stub to the master (no real network)."""
    lamp = WebhookConfig(name="lamp-1", url=LAMP, levels=["red"], timeout_s=3)
    call = CallConfig(name="master", to="", levels=["red"], provider="stub")
    _tune(monkeypatch, core, delivery={"webhooks": [lamp], "calls": [call]})


async def run(fake_clock: FakeClock, seconds: float, step: float = 0.25) -> int:
    """Every background loop of the worker on the fake clock; the actions written."""
    written = 0
    for _ in range(int(seconds / step)):
        fake_clock.advance(step)
        written += services.broadcast_tick() + services.escalation_tick()
        written += await services.deliveries_flush()
    return written


def alerts(sent: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    return [d for kind, d in sent if kind == "notification"]


def no_duplicate_side_effects(operator: Client, master: Client) -> dict[str, list[Any]]:
    """One takeover and one siren per event, one hand-over per event, one delivery per action."""
    ops, masters = alerts(drain(operator)), alerts(drain(master))
    takeovers = Counter(n["event_id"] for n in ops if n["takeover"])
    sirens = Counter(n["event_id"] for n in ops if n["sound"] == "siren")
    handed = Counter(n["event_id"] for n in masters)
    sent = Counter((d["event_id"], d["channel"], d["kind"]) for d in deliveries())
    assert set(takeovers.values()) <= {1} and takeovers == sirens
    assert set(handed.values()) <= {1}
    assert set(sent.values()) <= {1}
    return {"takeovers": sorted(takeovers), "handed": sorted(handed), "sent": sorted(sent)}


@respx.mock
async def test_default_show_alarms_once(
    core: Settings, fake_clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    channels(monkeypatch, core)
    respx.post(LAMP).mock(return_value=httpx.Response(200))
    cam_a, cam_b = camera(), camera("Сектор 6 · Цех")
    ready_video(cam_a, [YELLOW_TO_RED], 20_000)
    ready_video(cam_b, [RED], 20_000)
    operator, master = hub.connect("operator"), hub.connect("master")
    # No `loop` in the request: broadcast.loop_default is a single play now.
    first_a = services.broadcast_start(cam_a, BroadcastIn(), "admin")
    first_b = services.broadcast_start(cam_b, BroadcastIn(), "admin")
    assert (first_a.loop, first_b.loop) == (False, False)
    t0 = started(first_a.id)
    # Three video lengths and past the 45 s escalation: the video does not come round again.
    await run(fake_clock, 70)
    rows = events()
    assert [(e["camera_id"], e["level"], e["cycle"]) for e in rows] == [
        (cam_a, "red", 0),
        (cam_b, "red", 0),
    ]
    a, b = rows
    # Yellow turned red on the same card; red_at stays the moment of the escalation.
    assert a["red_at"] == clock.iso(clock.parse(t0) + timedelta(seconds=7))
    assert {store.broadcast(x.id)["status"] for x in (first_a, first_b)} == {"ended"}  # type: ignore[index]
    seen = no_duplicate_side_effects(operator, master)
    assert seen["takeovers"] == seen["handed"] == [a["id"], b["id"]]
    assert sum(k == "to_master" and c.startswith("call:") for _, c, k in seen["sent"]) == 2
    # A restart: process caches start empty, the database stays; nothing is published again.
    for name in ("_camera_seen", "_sector_seen", "_preview_cache"):
        monkeypatch.setattr(services, name, {})
    assert await run(fake_clock, 30) == 0
    assert len(events()) == 2 and not alerts(drain(operator)) and not alerts(drain(master))
    # A manual restart is a new show: a new event of the new broadcast, the old one kept.
    journal_b = store.all("SELECT * FROM event_actions WHERE event_id = ?", b["id"])
    again = services.broadcast_start(cam_b, BroadcastIn(), "admin")
    await run(fake_clock, 7)
    fresh = [e for e in events() if e["broadcast_id"] == again.id]
    assert len(fresh) == 1 and fresh[0]["id"] != b["id"] and fresh[0]["level"] == "red"
    kept = next(e for e in events() if e["id"] == b["id"])
    assert kept["status"] == b["status"] == "sent_to_master"
    assert store.all("SELECT * FROM event_actions WHERE event_id = ?", b["id"]) == journal_b
    assert [n["event_id"] for n in alerts(drain(operator)) if n["takeover"]] == [fresh[0]["id"]]


@pytest.mark.skipif(not (PACK / "manifest.json").exists(), reason="demo pack not unpacked")
@respx.mock
async def test_real_pack_one_alarm_per_episode(
    core: Settings,
    fake_clock: FakeClock,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Any,
    linq_tails: Any,
) -> None:
    channels(monkeypatch, core)
    respx.post(LAMP).mock(return_value=httpx.Response(200))
    pack = tmp_path / PACK.name
    shutil.copytree(PACK, pack)  # the pack folder belongs to its own agent: read a copy
    shell = _shell(monkeypatch)
    report = services.demo_import(pack)
    assert (report.cameras, report.videos, report.jobs) == (4, 4, 4)
    fake_clock.advance(1)
    while await services.run_next_job() is not None:
        pass
    assert "start" not in shell.calls  # the cache, never a live LinQ run
    cams = {c.name.split(" · ")[0]: c.id for c in services.cameras_list()}
    episodes = {}
    for name, camera_id in cams.items():
        (video,) = services.videos_list(camera_id)
        assert video.status == "ready" and services.broadcast_get(camera_id).loop is False  # type: ignore[union-attr]
        episodes[name] = services.video_analysis(video.id).episodes
    # The background camera 2.3 has nothing; 1.3 reproduces the walking man red in `danger`.
    assert episodes["Камера 2.3"] == []
    assert [e.reason_code for e in episodes["Камера 1.3"]] == ["proximity_zone"]
    operator, master = hub.connect("operator"), hub.connect("master")
    await run(fake_clock, 25)  # every video played out once
    by_camera = Counter(e["camera_id"] for e in events())
    assert by_camera == Counter({cams[n]: len(eps) for n, eps in episodes.items() if eps})
    # The operator confirms the fence event, the master takes and resolves it: the journal has it.
    fence = next(e for e in events() if e["camera_id"] == cams["Камера 1.5"])
    services.event_action(fence["id"], ActionIn(action="confirm"), "operator", None)
    services.event_action(fence["id"], ActionIn(action="accept"), "master", None)
    services.event_action(
        fence["id"], ActionIn(action="resolve", comment="Проход перекрыт"), "master", None
    )
    # The rest are left: each escalates by timeout once; then three more video lengths.
    await run(fake_clock, 65)
    assert Counter(e["camera_id"] for e in events()) == by_camera
    seen = no_duplicate_side_effects(operator, master)
    assert seen["takeovers"] == sorted(e["id"] for e in events())
    assert seen["handed"] == sorted(e["id"] for e in events())
    page = services.events_list(EventFilter(camera_id=cams["Камера 1.5"]))
    assert [(e.id, e.status) for e in page.items] == [(fence["id"], "resolved")]
    # The zone of 1.3 is a forklift lane: kind vehicle_path (config/default.yaml), not danger.
    (lane,) = services.zones_list(cams["Камера 1.3"])
    assert lane.kind == "danger"
    services.zone_delete(lane.id, "admin")
    services.zone_create(
        cams["Камера 1.3"], ZoneIn(kind="vehicle_path", name=lane.name, points=lane.points), "admin"
    )
    (video,) = services.videos_list(cams["Камера 1.3"])
    services.video_recompute(video.id, "admin")
    await services.run_next_job()
    assert services.video_analysis(video.id).episodes == []
    # The positive case stays: a person inside a danger zone (1.4, at the press) is still red.
    assert "proximity_zone" in [e.reason_code for e in episodes["Камера 1.4"]]
    assert config.get_settings().broadcast.loop_default is False
