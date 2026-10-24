"""Slice 5: episodes and evidence of a job, GET /analysis, evidence images, recompute, meta."""

import hashlib
from pathlib import Path

import cv2
import httpx
import numpy as np
import pytest
from test_jobs import _tune

from safewatch import config, registry, services, store
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.rules.fall import FallPlugin
from safewatch.rules.running import RunningPlugin
from safewatch.types import Analysis, CameraIn, EpisodeDraft, Job, Meta, SectorIn

OHS, OPERATOR, ADMIN = {"X-Role": "ohs"}, {"X-Role": "operator"}, {"X-Role": "admin"}


def _camera() -> int:
    sector = services.sector_create(SectorIn(name="Цех"), "admin")
    return services.camera_create(CameraIn(sector_id=sector.id, name="Камера"), "admin").id


def _textured(path: Path, seed: int = 0) -> Path:
    """20 s at 10 fps, 1600x300: wide enough for the demo scene, noisy enough for JPEG."""
    img = np.random.default_rng(seed).integers(0, 256, (300, 1600, 3), dtype=np.uint8)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), 10, (1600, 300))
    for _ in range(200):
        writer.write(img)
    writer.release()
    return path


async def _demo_job(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, camera_id: int) -> Job:
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), FakeRemoteShell()))
    services.video_import(camera_id, _textured(tmp_path / "demo.mp4"))  # auto scene: demo
    job = await services.run_next_job()
    assert job is not None
    return job


async def _analysis(client: httpx.AsyncClient, video_id: int) -> Analysis:
    r = await client.get(f"/api/videos/{video_id}/analysis")
    assert r.status_code == 200, r.text
    return Analysis.model_validate(r.json())


async def test_job_creates_episodes_and_evidence(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = _camera()
    job = await _demo_job(monkeypatch, tmp_path, camera_id)
    assert (job.status, job.stage, job.progress) == ("done", "done", 1.0)
    analysis = await _analysis(client, job.video_id)
    assert (analysis.id, analysis.version, analysis.pose_used) == (job.analysis_id, 1, True)
    found = [(e.scenario, e.level_initial, e.level_max) for e in analysis.episodes]
    assert found == [("running", "yellow", "yellow"), ("fall", "red", "red")]
    running, fall = analysis.episodes
    assert running.scenario_title == "Бег и резкие перемещения"
    assert running.reason_text.startswith("Бег ") and running.confirm_ms - running.start_ms >= 1000
    assert fall.reason_text == "Зафиксировано падение"  # the track survives the fall (S30)
    assert fall.end_reason == "video_end" and fall.end_ms == 20_000
    for episode in analysis.episodes:
        (shot,) = episode.evidence
        assert shot.kind == "confirm" and shot.url == f"/api/evidence/{shot.id}/image"
        data = (core.data_dir / f"evidence/{episode.id}-confirm.jpg").read_bytes()
        assert shot.sha256 == hashlib.sha256(data).hexdigest()
        assert cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR).shape[1] == 1280
        (who,) = [o for o in shot.objects if o.kind == "person"]
        # The HUD of the confirm frame carries the observation of the scenario.
        assert episode.scenario in {t.code for t in who.tags}

    other = services.video_import(camera_id, _textured(tmp_path / "queued.mp4", seed=1)).video.id
    busy = await client.get(f"/api/videos/{other}/analysis")
    assert (busy.status_code, busy.json()["code"]) == (409, "video_not_ready")
    assert (await client.get("/api/videos/999/analysis")).status_code == 404


async def test_evidence_404_and_sha(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    job = await _demo_job(monkeypatch, tmp_path, _camera())
    shot = (await _analysis(client, job.video_id)).episodes[0].evidence[0]
    image = await client.get(shot.url)
    assert (image.status_code, image.headers["content-type"]) == (200, "image/jpeg")
    assert hashlib.sha256(image.content).hexdigest() == shot.sha256
    assert (await client.get("/api/evidence/999/image")).status_code == 404

    _tune(monkeypatch, core, evidence={"jpeg_quality": 30})
    services.video_recompute(job.video_id, "ohs")
    await services.run_next_job()
    low = (await _analysis(client, job.video_id)).episodes[0].evidence[0]
    assert len((await client.get(low.url)).content) < len(image.content)
    (core.data_dir / f"evidence/{store.evidence(low.id)['episode_id']}-confirm.jpg").unlink()
    assert (await client.get(low.url)).status_code == 404


async def test_recompute_creates_new_version(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = _camera()
    job = await _demo_job(monkeypatch, tmp_path, camera_id)
    shell = FakeRemoteShell()
    monkeypatch.setattr(services, "_backend", LinqBackend(core, shell))
    url = f"/api/videos/{job.video_id}/recompute"
    assert (await client.post(url)).status_code == 400
    assert (await client.post(url, headers=OPERATOR)).status_code == 403
    assert (await client.post("/api/videos/999/recompute", headers=ADMIN)).status_code == 404
    r = await client.post(url, headers=OHS)
    assert r.status_code == 202
    queued = Job.model_validate(r.json())
    assert (queued.kind, queued.status) == ("recompute", "queued")
    done = await services.run_next_job()
    assert done is not None and (done.id, done.status) == (queued.id, "done")
    assert "start" not in shell.calls  # the same artifacts: no inference on LinQ
    analysis = await _analysis(client, job.video_id)
    assert (analysis.id, analysis.version) == (done.analysis_id, 2)
    assert services.video_get(job.video_id).active_analysis_id == done.analysis_id

    fresh = services.video_import(camera_id, _textured(tmp_path / "queued.mp4", seed=1)).video.id
    busy = await client.post(f"/api/videos/{fresh}/recompute", headers=ADMIN)
    assert (busy.status_code, busy.json()["code"]) == (409, "video_not_ready")

    # Queued while the artifacts exist, the file is gone before the job runs.
    assert (await client.post(url, headers=ADMIN)).status_code == 202
    row = store.analysis(done.analysis_id or 0)
    assert row is not None
    (core.data_dir / store.artifact_path(row["pose_artifact_id"])).unlink()
    gone = await client.post(url, headers=ADMIN)
    assert (gone.status_code, gone.json()["code"]) == (409, "artifacts_missing")
    await services.run_next_job()  # the process job of the fresh video goes first
    failed = await services.run_next_job()
    assert failed is not None and (failed.status, failed.error_code) == (
        "failed",
        "artifacts_missing",
    )


def _draft(scenario: str, reason_code: str, method: str, uncertain_ms: int = 0) -> EpisodeDraft:
    return EpisodeDraft(
        scenario=scenario, subject="track:1", zone_id=None, level_initial="yellow",
        level_max="yellow", start_ms=0, confirm_ms=1000, escalate_ms=None, end_ms=5000,
        end_reason="video_end", reason_code=reason_code, reason_text="", method=method,
        confidence=0.87, metrics={"speed_bh_s": 2.44}, uncertain_ms=uncertain_ms,
        confirm_frame_idx=10, escalate_frame_idx=None,
    )  # fmt: skip


async def test_meta_lists_running_and_fall(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    meta = Meta.model_validate((await client.get("/api/meta")).json())
    by_id = {s.id: s for s in meta.scenarios}  # slice 10 adds the other plugins of 8.3
    assert (by_id["running"].status, by_id["fall"].status) == ("active", "active")
    running, fall = by_id["running"], by_id["fall"]
    assert {p.key: p.default for p in running.params} == core.scenarios.running
    assert {p.key: p.default for p in fall.params} == core.scenarios.fall
    tuned = _tune(
        monkeypatch, core, scenarios={"running": {**core.scenarios.running, "hold_s": 2.0}}
    )
    meta = Meta.model_validate((await client.get("/api/meta")).json())
    assert {p.key: p.default for p in meta.scenarios[0].params}["hold_s"] == 2.0
    monkeypatch.setattr(registry, "active_classes", lambda settings: ["car"])
    meta = Meta.model_validate((await client.get("/api/meta")).json())
    assert {s.status for s in meta.scenarios if s.id != "load_carrying"} == {"model_missing"}
    assert "person" in meta.scenarios[0].status_text

    params = tuned.scenarios.running
    why = RunningPlugin().explain(_draft("running", "running", "relative", 2400), params)
    assert [(w.label, w.value) for w in why] == [
        ("Правило", "Бег: скорость выше 1,5 роста/с дольше 2,0 с"),
        ("Скорость, роста/с", "2,4"),
        ("Метод", "в ростах человека"),
        ("Уверенность детекции", "0,9"),
        ("Потеря видимости", "2 с"),
    ]
    calibrated = RunningPlugin().explain(_draft("running", "running", "calibrated"), params)
    assert calibrated[0].value == "Бег: скорость выше 2,5 м/с дольше 2,0 с"
    lines = FallPlugin().explain(_draft("fall", "fall", "pose"), core.scenarios.fall)
    assert lines[0].value == "Падение: переход стоя → лёжа не дольше 2,0 с, лежит дольше 2,0 с"
    assert ("Метод", "поза") in [(w.label, w.value) for w in lines]
    still = FallPlugin().explain(_draft("fall", "lying_still", "bbox"), core.scenarios.fall)
    assert still[0].value == "Неподвижность: лежит без движения дольше 10,0 с"
