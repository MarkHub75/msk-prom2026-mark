"""Slice 3: manual retry of a failed job and recovery of jobs a stopped server left running."""

from pathlib import Path

import httpx
import pytest
import uvicorn

from safewatch import cli, services, store
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import CameraIn, Fault, Job, SectorIn


def _video(tmp_path: Path, make_video, name: str = "clip.mp4") -> int:
    sector = services.sector_create(SectorIn(name=f"Цех {name}"), "admin")
    camera_id = services.camera_create(CameraIn(sector_id=sector.id, name="Камера"), "admin").id
    return services.video_import(camera_id, make_video(tmp_path, 2, 25, name=name)).video.id


def _shell(monkeypatch: pytest.MonkeyPatch, core: Settings, script: list[Fault | None]) -> None:
    monkeypatch.setattr(services, "_backend", LinqBackend(core, FakeRemoteShell(script)))


async def test_manual_retry(
    core: Settings,
    client: httpx.AsyncClient,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _shell(monkeypatch, core, ["bad_output", None])
    video_id = _video(tmp_path, make_video)
    failed = await services.run_next_job()
    assert failed is not None and (failed.status, failed.error_code) == ("failed", "bad_output")

    url = f"/api/jobs/{failed.id}/retry"
    assert (await client.post(url)).status_code == 400
    assert (await client.post(url, headers={"X-Role": "operator"})).status_code == 403
    assert (
        await client.post("/api/jobs/999/retry", headers={"X-Role": "admin"})
    ).status_code == 404
    response = await client.post(url, headers={"X-Role": "admin"})
    assert response.status_code == 200
    job = Job.model_validate(response.json())
    assert (job.status, job.attempts, job.error_code, job.error_text) == ("queued", 0, None, None)
    assert job.next_attempt_at is None and job.finished_at is None
    assert services.video_get(video_id).status == "uploaded"

    again = await client.post(url, headers={"X-Role": "admin"})
    assert (again.status_code, again.json()["code"]) == (409, "job_not_failed")
    done = await services.run_next_job()
    assert done is not None and (done.id, done.status, done.attempts) == (job.id, "done", 1)
    with pytest.raises(services.Conflict):
        services.job_retry(job.id, "admin")


def test_recover_running_jobs(
    core: Settings, tmp_path: Path, make_video, monkeypatch: pytest.MonkeyPatch
) -> None:
    running = _video(tmp_path, make_video, "a.mp4")
    queued = _video(tmp_path, make_video, "b.mp4")
    run_id = store.video_last_job(running)["id"]
    store.job_update(run_id, {"status": "running", "stage": "inference_detect"})
    assert services.recover_jobs() == 1
    assert services.job_get(run_id).status == "queued"
    assert services.job_get(store.video_last_job(queued)["id"]).status == "queued"
    assert services.recover_jobs() == 0

    # `serve` puts them back before the server starts.
    store.job_update(run_id, {"status": "running"})

    async def no_server(self: uvicorn.Server) -> None:
        return None

    monkeypatch.setattr(uvicorn.Server, "serve", no_server)
    monkeypatch.setattr(cli, "_port_free", lambda host, port: True)
    assert cli.serve(None, None, False) == 0
    assert services.job_get(run_id).status == "queued"
