"""Slice 2: the job queue, artifact cache and retry policy of tech.md 8.1 on FakeRemoteShell."""

import asyncio
import math
import sqlite3
from datetime import timedelta
from pathlib import Path
from typing import Any

import pydantic
import pytest

from safewatch import config, services, store
from safewatch.config import PipelineConfig, Settings, get_settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.hub import hub
from safewatch.inference import make_backend
from safewatch.inference.artifacts import CACHE_SCHEMA, cache_key
from safewatch.inference.linq import JupyterShell, LinqBackend
from safewatch.inference.local import LocalBackend
from safewatch.types import CameraIn, Fault, Job, SectorIn, WsMessage


def _tune(
    monkeypatch: pytest.MonkeyPatch, settings: Settings, **sections: dict[str, Any]
) -> Settings:
    """Settings with some section keys changed; the shared cached object stays intact."""
    update = {
        name: getattr(settings, name).model_copy(update=values) for name, values in sections.items()
    }
    tuned = settings.model_copy(update=update)
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    return tuned


def _shell(
    monkeypatch: pytest.MonkeyPatch, script: list[Fault | None] | None = None
) -> FakeRemoteShell:
    shell = FakeRemoteShell(script)
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), shell))
    return shell


def _video(tmp_path: Path, make_video, camera: str = "Камера 1", seconds: float = 3) -> int:
    sector = services.sector_create(SectorIn(name=f"Цех {camera}"), "admin")
    camera_id = services.camera_create(CameraIn(sector_id=sector.id, name=camera), "admin").id
    clip = make_video(tmp_path, seconds, 25)
    return services.video_import(camera_id, clip).video.id


async def test_job_runs_detect_then_pose(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    video_id = _video(tmp_path, make_video)
    job = await services.run_next_job()
    assert job is not None
    assert (job.status, job.stage, job.progress, job.attempts) == ("done", "done", 1.0, 1)
    assert services.video_get(video_id).status == "ready"
    assert [m.task for m in job.metrics] == ["detect", "pose"]
    frames = math.ceil(75 / 2)  # 25 fps -> step 2
    for m in job.metrics:
        assert (m.backend, m.fake, m.step, m.frames_processed) == ("linq", True, 2, frames)
        assert m.cached is False
    rows = store.all("SELECT path FROM artifacts")
    assert len(rows) == 2 and all((fake_core.data_dir / r["path"]).is_file() for r in rows)
    assert services.jobs_list() == [job] and services.job_get(job.id) == job
    assert services.jobs_list("failed") == []
    with pytest.raises(services.ValidationFailed):
        services.jobs_list(limit=fake_core.jobs.list_max + 1)
    assert len(services.jobs_list(limit=fake_core.jobs.list_max)) == 1
    with pytest.raises(services.NotFound):
        services.job_get(999)
    assert await services.run_next_job() is None


async def test_job_progress_published(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    _video(tmp_path, make_video)
    ws = hub.connect("operator")
    await services.run_next_job()
    jobs = []
    while not ws.queue.empty():
        message = WsMessage.model_validate_json(ws.queue.get_nowait() or "")
        if message.type == "broadcast.state":  # autostart of slice 6
            continue
        assert message.type == "job.progress" and isinstance(message.data, Job)
        jobs.append(message.data)
    stages = [j.stage for j in jobs]
    assert stages.index("inference_detect") < stages.index("inference_pose") < stages.index("done")
    progress = [j.progress for j in jobs]
    assert progress == sorted(progress) and progress[-1] == 1.0
    assert 0.45 in progress and 0.85 in progress


async def test_cache_hit_skips_remote(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    fake_clock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shell = _shell(monkeypatch)
    _video(tmp_path, make_video, "Камера 1")
    await services.run_next_job()
    assert shell.calls.count("start") == 2
    fake_clock.advance(1)
    _video(tmp_path, make_video, "Камера 2")  # the same file: the same sha256
    shell.calls.clear()
    job = await services.run_next_job()
    assert job is not None and job.status == "done"
    assert "start" not in shell.calls
    assert [m.cached for m in job.metrics] == [True, True]

    tuned = _tune(monkeypatch, fake_core, pipeline={"detector": "det-yolov8n@960-ap9999"})
    monkeypatch.setattr(services, "_backend", LinqBackend(tuned, shell))
    _video(tmp_path, make_video, "Камера 3")
    shell.calls.clear()
    job = await services.run_next_job()
    assert job is not None and shell.calls.count("start") == 1  # detector again, pose cached
    assert [m.cached for m in job.metrics] == [False, True]
    assert job.metrics[0].input_size == 960

    model = services.registry.resolve(fake_core.pipeline.detector)
    key = cache_key("abc", model, 2, "linq", True)
    assert (
        key != cache_key("abc", model, 3, "linq", True) != cache_key("abc", model, 2, "linq", False)
    )
    assert CACHE_SCHEMA == "jsonl-v1"


@pytest.mark.parametrize(("fps", "step"), [(25, 2), (30, 2), (60, 5), (10, 1), (12, 1), (24, 2)])
def test_step_from_fps(core: Settings, fps: float, step: int) -> None:
    assert services.analysis_step(fps) == step


def test_step_follows_target_fps_and_floor(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    _tune(monkeypatch, core, pipeline={"target_analysis_fps": 6})
    assert services.analysis_step(25) == 4
    data = core.pipeline.model_dump() | {"target_analysis_fps": 4, "min_analysis_fps": 5}
    with pytest.raises(pydantic.ValidationError):
        PipelineConfig.model_validate(data)
    assert PipelineConfig.model_validate(data | {"target_analysis_fps": 5}).target_analysis_fps == 5


async def test_backoff_and_max_attempts(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    fake_clock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _shell(monkeypatch, ["unavailable"])
    video_id = _video(tmp_path, make_video)
    job = await services.run_next_job()
    assert job is not None
    assert (job.status, job.error_code, job.attempts) == ("retry_wait", "linq_unavailable", 1)
    assert job.next_attempt_at == fake_clock.now() + timedelta(seconds=30)
    fake_clock.advance(29.999)
    assert await services.run_next_job() is None  # not due yet
    fake_clock.advance(0.001)
    job = await services.run_next_job()
    assert job is not None and job.status == "retry_wait"
    assert job.next_attempt_at == fake_clock.now() + timedelta(seconds=120)
    fake_clock.advance(120)
    job = await services.run_next_job()
    assert job is not None
    assert (job.status, job.error_code, job.attempts) == ("failed", "linq_unavailable", 3)
    assert services.video_get(video_id).status == "failed"


@pytest.mark.parametrize(
    ("script", "max_attempts", "status", "code"),
    [
        (["bad_output"], 3, "failed", "bad_output"),
        (["remote_error"], 3, "retry_wait", "remote_error"),
        (["unavailable"], 1, "failed", "linq_unavailable"),
        (["unavailable"], 2, "retry_wait", "linq_unavailable"),
    ],
)
async def test_failure_outcomes(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    script: list[Fault | None],
    max_attempts: int,
    status: str,
    code: str,
) -> None:
    _tune(monkeypatch, fake_core, jobs={"max_attempts": max_attempts})
    _shell(monkeypatch, script)
    _video(tmp_path, make_video)
    job = await services.run_next_job()
    assert job is not None and (job.status, job.error_code) == (status, code)


async def test_missing_tail_and_pose_error(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shell = _shell(monkeypatch, [None, "remote_error"])  # detector fine, pose stops
    _video(tmp_path, make_video, "Камера 1")
    job = await services.run_next_job()
    assert job is not None and (job.status, job.error_code) == ("done", None)
    assert job.error_text is not None and job.error_text.startswith("pose:")
    assert [m.task for m in job.metrics] == ["detect"]
    assert shell.runs == 2

    model = services.registry.resolve(fake_core.pipeline.detector)
    (linq_tails / str(model.linq_tail)).unlink()
    _video(tmp_path, make_video, "Камера 2", seconds=2)
    job = await services.run_next_job()
    assert job is not None and (job.status, job.error_code) == ("failed", "model_missing")


async def test_timeout_kills_remote_worker(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _tune(monkeypatch, fake_core, linq={"job_timeout_s": 0.2, "poll_interval_s": 0.01})
    shell = _shell(monkeypatch, ["timeout"])
    _video(tmp_path, make_video)
    job = await services.run_next_job()
    assert job is not None and (job.status, job.error_code) == ("retry_wait", "timeout")
    assert shell.calls[-1] == "kill" and shell.calls.count("kill") == 1


def test_make_backend_by_settings(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    real = make_backend(core)
    assert isinstance(real, LinqBackend) and isinstance(real.shell, JupyterShell)
    fake = make_backend(core.model_copy(update={"fake": True}))
    assert isinstance(fake, LinqBackend) and isinstance(fake.shell, FakeRemoteShell)
    assert isinstance(
        make_backend(core.model_copy(update={"inference_backend": "local"})), LocalBackend
    )
    monkeypatch.setenv("INFERENCE_BACKEND", "local")
    get_settings.cache_clear()
    try:
        assert get_settings().inference_backend == "local"
    finally:
        monkeypatch.delenv("INFERENCE_BACKEND")
        get_settings.cache_clear()


async def test_job_loop_survives_unexpected_error(
    core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    from safewatch import worker

    stop = asyncio.Event()
    calls: list[int] = []

    async def flaky() -> Job | None:
        calls.append(1)
        if len(calls) == 1:
            raise sqlite3.OperationalError("database is locked")
        stop.set()
        return None

    monkeypatch.setattr(services, "run_next_job", flaky)
    await asyncio.wait_for(worker.run_forever(stop), 5)
    assert len(calls) == 2
