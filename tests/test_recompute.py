"""Slice 9: recompute of tech.md 8.12 and the configuration snapshot of an analysis."""

from pathlib import Path

import httpx
import pytest
from test_analysis_api import _demo_job
from test_broadcast import actions, drain
from test_calibration import FLOOR, SQUARE, camera
from test_operator_views import event

from safewatch import services, store
from safewatch.config import Settings
from safewatch.hub import hub
from safewatch.types import AnalysisConfig, CalibrationIn, CameraRuleIn, Job, ZoneIn, ZonePatch

OHS = {"X-Role": "ohs"}


def _status(event_id: int) -> str:
    row = store.event(event_id)
    assert row is not None
    return str(row["status"])


async def test_recompute_supersedes_untouched_events(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = camera()
    job = await _demo_job(monkeypatch, tmp_path, camera_id)
    old = services.broadcast_get(camera_id)
    assert old is not None and old.status == "playing"  # autostart of the processed video
    episode = store.episodes(job.analysis_id or 0)[0]["id"]
    common = {"episode_id": episode, "video_id": job.video_id, "broadcast_id": old.id}
    untouched = [event(camera_id, **common, status=s) for s in ("new", "auto_finished")]
    touched = [event(camera_id, **common, status=s) for s in ("viewed", "confirmed", "resolved")]
    ws = hub.connect("operator")

    url = f"/api/videos/{job.video_id}/recompute"
    first = Job.model_validate((await client.post(url, headers=OHS)).json())
    again = Job.model_validate((await client.post(url, headers=OHS)).json())
    assert again.id == first.id  # repeated clicks share the queued job
    done = await services.run_next_job()
    assert done is not None and (done.id, done.status) == (first.id, "done")
    assert await services.run_next_job() is None

    assert [_status(e) for e in untouched] == ["superseded", "superseded"]
    assert [_status(e) for e in touched] == ["viewed", "confirmed", "resolved"]
    assert actions(untouched[0])[-1] == ("system", "superseded", "new", "superseded")
    assert actions(untouched[1])[-1] == ("system", "superseded", "auto_finished", "superseded")
    assert [len(actions(e)) for e in touched] == [1, 1, 1]  # history kept as it was
    row = store.all("SELECT * FROM event_actions WHERE event_id = ? ORDER BY id", untouched[0])[-1]
    assert row["comment"] == "Пересчёт: версия анализа 2"

    messages = drain(ws)
    assert [d["id"] for t, d in messages if t == "event.updated"] == untouched
    states = [(d["id"], d["status"]) for t, d in messages if t == "broadcast.state"]
    fresh = services.broadcast_get(camera_id)
    assert fresh is not None and fresh.id != old.id
    assert (fresh.status, fresh.analysis_id, fresh.loop) == ("playing", done.analysis_id, old.loop)
    assert states == [(old.id, "stopped"), (fresh.id, "playing")]

    # A stopped broadcast is not started again by the next recompute.
    services.broadcast_stop(camera_id, "admin")
    services.video_recompute(job.video_id, "admin")
    await services.run_next_job()
    last = services.broadcast_get(camera_id)
    assert last is not None and (last.id, last.status) == (fresh.id, "stopped")


async def test_config_snapshot_stored(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = camera()
    services.calibration_set(
        camera_id, CalibrationIn(image_points=SQUARE, world_points=FLOOR), "admin"
    )
    fence = ZoneIn(kind="fence", name="Забор", points=[(0.0, 0.02), (0.05, 0.02)])
    zone = services.zone_create(camera_id, fence, "ohs")
    services.camera_rule_set(
        camera_id, "fall", CameraRuleIn(enabled=True, params={"still_s": 5.0}), "ohs"
    )
    job = await _demo_job(monkeypatch, tmp_path, camera_id)

    def snapshot() -> AnalysisConfig:
        row = store.analysis(job.analysis_id or 0)
        assert row is not None
        return AnalysisConfig.model_validate_json(row["config_json"])

    cfg = snapshot()
    assert cfg.calibration is not None and cfg.calibration.world_points == FLOOR
    assert [(z.id, z.name) for z in cfg.zones] == [(zone.id, "Забор")]
    assert cfg.rules["fall"].params == {"still_s": 5.0} and cfg.rules["running"].params == {}

    services.zone_update(zone.id, ZonePatch(name="Новый забор"), "admin")
    services.calibration_delete(camera_id, "admin")
    assert snapshot() == cfg  # a later edit leaves the analysis as it was
