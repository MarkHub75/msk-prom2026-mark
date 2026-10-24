"""Slice 3: the IT screen data (`system_view`) and the model registry view (`models_view`)."""

from pathlib import Path

import httpx
import pytest

from safewatch import config, registry, services
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import BackendStatus, CameraIn, ModelsView, SectorIn, SystemView


async def test_system_view_metrics(
    core: Settings,
    client: httpx.AsyncClient,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(services, "_backend", LinqBackend(core, FakeRemoteShell()))
    sector = services.sector_create(SectorIn(name="Цех"), "admin")
    for name in ("Камера 1", "Камера 2"):
        camera = services.camera_create(CameraIn(sector_id=sector.id, name=name), "admin")
        services.video_import(camera.id, make_video(tmp_path, 2, 25))
    view = SystemView.model_validate((await client.get("/api/system")).json())
    assert (view.backend, view.fake, view.backend_status.state) == ("linq", False, "unchecked")
    assert [j.status for j in view.queue] == ["queued", "queued"] and view.recent_jobs == []

    done = await services.run_next_job()
    assert done is not None and done.status == "done"
    view = SystemView.model_validate((await client.get("/api/system")).json())
    assert [j.id for j in view.recent_jobs] == [done.id] and len(view.queue) == 1
    detect, pose = view.recent_jobs[0].metrics
    assert (detect.task, pose.task) == ("detect", "pose")
    assert (detect.frames_processed, detect.tpu_rtt_p50_ms, detect.tpu_rtt_p90_ms) == (
        25,
        10.0,
        12.0,
    )
    assert detect.preprocess_ms == 1.0 and detect.upload_s is not None and detect.total_s > 0
    assert [m.id for m in view.models] == ["det-yolov8n", "pose-yolov8n"]
    assert (
        view.cameras == services.camera_states()
        and view.channels == []
        and view.latency.notify_delay_s.n == 0
    )

    checked = BackendStatus.model_validate((await client.post("/api/system/backend-check")).json())
    assert checked.state == "ok"
    view = SystemView.model_validate((await client.get("/api/system")).json())
    assert view.backend_status == checked


async def test_models_view(
    core: Settings, client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    view = ModelsView.model_validate((await client.get("/api/models")).json())
    assert [f"{m.id}@{m.version}" for m in view.active] == [
        core.pipeline.detector,
        core.pipeline.pose,
    ]
    assert view.available == registry.load_models(registry.MODELS_FILE)
    assert len(view.available) == 3
    no_pose = core.model_copy(update={"pipeline": core.pipeline.model_copy(update={"pose": None})})
    monkeypatch.setattr(config, "get_settings", lambda: no_pose)
    assert [m.task for m in services.models_view().active] == ["detect"]
