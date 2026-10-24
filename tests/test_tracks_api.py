"""Slice 4: the `analysis` stage of a job and GET /api/videos/{id}/tracks (tech.md 8.1, 6.4)."""

import math
from pathlib import Path

import httpx
import pytest

from safewatch import config, services, store
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import CameraIn, HudFrame, Job, SectorIn, TracksWindow


def _camera() -> int:
    sector = services.sector_create(SectorIn(name="Цех"), "admin")
    return services.camera_create(CameraIn(sector_id=sector.id, name="Камера"), "admin").id


async def _analyzed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, make_video, camera_id: int
) -> Job:
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), FakeRemoteShell()))
    clip = make_video(tmp_path, 3, 25, name="walk.mp4")
    services.video_import(camera_id, clip)
    job = await services.run_next_job()
    assert job is not None
    return job


async def test_tracks_window_contents(
    core: Settings, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    job = await _analyzed(monkeypatch, tmp_path, make_video, _camera())
    assert (job.status, job.stage, job.progress) == ("done", "done", 1.0)
    assert job.analysis_id is not None and job.analysis_ms is not None
    row = store.one("SELECT * FROM analyses WHERE id = ?", job.analysis_id)
    assert row is not None and row["version"] == 1 and row["video_id"] == job.video_id
    job_row = store.job(job.id)
    assert job_row is not None and row["pose_artifact_id"] is not None
    assert (row["det_artifact_id"], row["pose_artifact_id"]) == (
        job_row["det_artifact_id"],
        job_row["pose_artifact_id"],
    )
    assert services.video_get(job.video_id).active_analysis_id == job.analysis_id
    lines = (core.data_dir / row["hud_path"]).read_text(encoding="utf-8").splitlines()
    assert row["hud_path"] == f"analyses/{job.video_id}-v1/hud.jsonl"
    assert len(lines) == math.ceil(75 / 2)  # one HudFrame per analyzed frame (step 2)
    frames = [HudFrame.model_validate_json(line) for line in lines]
    people = {o.track_id for f in frames for o in f.objects if o.kind == "person"}
    assert people == {1}  # the demo scene: one person, keypoints from the pose run
    assert any(o.kpts for f in frames for o in f.objects)

    window = services.video_tracks(job.video_id, 1000, 2000)
    assert [f.ts_ms for f in window.frames] == list(range(1040, 2000, 80))  # [from, to)
    assert (window.analysis_id, window.from_ms, window.to_ms) == (job.analysis_id, 1000, 2000)
    edge = services.video_tracks(job.video_id, 0, 80)
    assert [f.ts_ms for f in edge.frames] == [0]


async def test_tracks_window_bounds(
    client: httpx.AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
) -> None:
    camera_id = _camera()
    job = await _analyzed(monkeypatch, tmp_path, make_video, camera_id)
    url = f"/api/videos/{job.video_id}/tracks"
    ok = await client.get(url, params={"from_ms": 0, "to_ms": 10000})
    assert ok.status_code == 200
    assert len(TracksWindow.model_validate(ok.json()).frames) == math.ceil(75 / 2)
    for from_ms, to_ms in [(0, 10001), (500, 500), (600, 500)]:
        bad = await client.get(url, params={"from_ms": from_ms, "to_ms": to_ms})
        assert (bad.status_code, bad.json()["code"]) == (422, "validation"), (from_ms, to_ms)

    other = make_video(tmp_path, 1, 25, name="fresh.mp4", luma=200)
    fresh = services.video_import(camera_id, other).video.id  # queued, not analyzed
    busy = await client.get(f"/api/videos/{fresh}/tracks", params={"from_ms": 0, "to_ms": 100})
    assert (busy.status_code, busy.json()["code"]) == (409, "video_not_ready")
    missing = await client.get("/api/videos/999/tracks", params={"from_ms": 0, "to_ms": 100})
    assert missing.status_code == 404
