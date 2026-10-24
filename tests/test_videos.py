"""Slice 2: upload and import of videos (tech.md 8.1), file with Range, camera setup view."""

import hashlib
import json
from pathlib import Path

import httpx
import pytest

from safewatch import cli, config, services
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.hub import hub
from safewatch.inference.linq import LinqBackend
from safewatch.media import BROWSER_CODECS
from safewatch.types import (
    ApiError,
    CameraIn,
    CameraSetupView,
    SectorIn,
    UploadResult,
    Video,
    WsMessage,
)

ADMIN = {"X-Role": "admin"}


def _camera(name: str = "Камера 1") -> int:
    sector = services.sector_create(SectorIn(name=f"Цех {name}"), "admin")
    return services.camera_create(CameraIn(sector_id=sector.id, name=name), "admin").id


async def _upload(
    client: httpx.AsyncClient,
    camera_id: int,
    data: bytes,
    name: str = "clip.mp4",
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    files = {"file": (name, data, "video/mp4")}
    url = f"/api/cameras/{camera_id}/videos"
    return await client.post(url, files=files, headers=ADMIN if headers is None else headers)


def _uploads(core: Settings) -> list[str]:
    folder = core.data_dir / "uploads"
    return sorted(p.name for p in folder.iterdir()) if folder.exists() else []


async def test_upload_probes_and_queues_job(
    client: httpx.AsyncClient, core: Settings, tmp_path: Path, make_video
) -> None:
    camera_id = _camera()
    ws = hub.connect("admin")
    clip = make_video(tmp_path, 3, 25, (320, 240))
    response = await _upload(client, camera_id, clip.read_bytes())
    assert response.status_code == 201
    result = UploadResult.model_validate(response.json())
    video = result.video
    assert (video.width, video.height, video.fps, video.frame_count) == (320, 240, 25, 75)
    assert abs(video.duration_ms - 3000) <= 40
    assert (video.codec, video.browser_playable, video.status) == ("mp4v", False, "uploaded")
    assert "mp4v" not in BROWSER_CODECS and "avc1" in BROWSER_CODECS
    assert result.reused is False and result.job is not None
    assert (result.job.kind, result.job.status, result.job.video_id) == (
        "process",
        "queued",
        video.id,
    )
    sha = hashlib.sha256(clip.read_bytes()).hexdigest()
    # The H.264 copy of slice 18 sits beside the source (tech.md 8.20).
    assert _uploads(core) == [f"{sha}.mp4", f"{sha}.web.mp4"]
    message = WsMessage.model_validate_json(ws.queue.get_nowait() or "")
    assert message.type == "job.progress" and message.data == result.job
    got = await client.get(f"/api/videos/{video.id}")
    assert Video.model_validate(got.json()) == video


async def test_upload_same_file_reuses_video(
    client: httpx.AsyncClient,
    core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    camera_id, other_id = _camera(), _camera("Камера 2")
    data = make_video(tmp_path, 1, 25).read_bytes()
    first = UploadResult.model_validate((await _upload(client, camera_id, data)).json())
    again = UploadResult.model_validate((await _upload(client, camera_id, data)).json())
    assert again.reused is True and again.video.id == first.video.id
    assert again.job is not None and first.job is not None and again.job.id == first.job.id

    monkeypatch.setattr(services, "_backend", LinqBackend(core, FakeRemoteShell()))
    assert (await services.run_next_job()) is not None
    done = UploadResult.model_validate((await _upload(client, camera_id, data)).json())
    assert (done.reused, done.job, done.video.status) == (True, None, "ready")

    other = UploadResult.model_validate((await _upload(client, other_id, data)).json())
    assert other.reused is False and other.video.id != first.video.id
    listed = (await client.get(f"/api/cameras/{camera_id}/videos")).json()
    assert [Video.model_validate(v).id for v in listed] == [first.video.id]
    assert (await client.get("/api/cameras/999/videos")).status_code == 404


async def test_upload_rejects_bad_files(
    client: httpx.AsyncClient, core: Settings, tmp_path: Path, make_video
) -> None:
    camera_id = _camera()
    clip = make_video(tmp_path, 1, 25).read_bytes()
    text = await _upload(client, camera_id, b"hello", name="notes.txt")
    assert text.status_code == 415
    junk = await _upload(client, camera_id, b"not a video" * 100, name="junk.mp4")
    assert junk.status_code == 415
    body = ApiError.model_validate(junk.json())
    assert (body.code, body.message) == ("unsupported_video", "Видео не читается")
    assert _uploads(core) == []
    assert (await _upload(client, 999, clip)).status_code == 404
    assert (await _upload(client, camera_id, clip, headers={})).status_code == 400
    assert (
        await _upload(client, camera_id, clip, headers={"X-Role": "operator"})
    ).status_code == 403
    assert _uploads(core) == []


async def test_upload_limit_boundary(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    camera_id = _camera()
    tuned = core.model_copy(update={"upload": core.upload.model_copy(update={"max_mb": 1})})
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    exact = await _upload(client, camera_id, b"\0" * 2**20)
    assert exact.status_code == 415  # passed the size check, failed the video check
    over = await _upload(client, camera_id, b"\0" * (2**20 + 1))
    assert over.status_code == 413
    assert ApiError.model_validate(over.json()).code == "too_large"
    assert _uploads(core) == []


async def test_video_file_supports_range(
    client: httpx.AsyncClient,
    core: Settings,
    tmp_path: Path,
    make_video,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # No H.264 copy: the source itself is served (the copy: tests/test_clips.py).
    off = core.transcode.model_copy(update={"enabled": False})
    tuned = core.model_copy(update={"transcode": off})
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    camera_id = _camera()
    data = make_video(tmp_path, 1, 25).read_bytes()
    video = UploadResult.model_validate((await _upload(client, camera_id, data)).json()).video
    part = await client.get(f"/api/videos/{video.id}/file", headers={"Range": "bytes=0-99"})
    assert part.status_code == 206
    assert part.content == data[:100]
    assert part.headers["content-range"] == f"bytes 0-99/{len(data)}"
    whole = await client.get(f"/api/videos/{video.id}/file")
    assert (whole.status_code, whole.content) == (200, data)
    assert (await client.get("/api/videos/999/file")).status_code == 404


def test_import_cli(
    core: Settings, tmp_path: Path, make_video, capsys: pytest.CaptureFixture[str]
) -> None:
    camera_id = _camera()
    clip = make_video(tmp_path, 1, 25, name="running.mp4")
    assert cli.main(["import", str(clip), "--camera", str(camera_id)]) == 0
    result = UploadResult.model_validate(json.loads(capsys.readouterr().out))
    assert result.video.filename == "running.mp4" and result.job is not None
    assert cli.main(["import", str(tmp_path / "missing.mp4"), "--camera", str(camera_id)]) == 3
    assert cli.main(["import", str(clip), "--camera", "999"]) == 3
    notes = tmp_path / "notes.txt"
    notes.write_text("x", encoding="utf-8")
    assert cli.main(["import", str(notes), "--camera", str(camera_id)]) == 2
    junk = tmp_path / "junk.mp4"
    junk.write_bytes(b"junk" * 100)
    assert cli.main(["import", str(junk), "--camera", str(camera_id)]) == 2


async def test_camera_setup_view_shape(
    client: httpx.AsyncClient, tmp_path: Path, make_video
) -> None:
    camera_id = _camera()
    ids = []
    for n, luma in enumerate((40, 200)):
        data = make_video(tmp_path, 1, 25, luma=luma, name=f"v{n}.mp4").read_bytes()
        ids.append(UploadResult.model_validate((await _upload(client, camera_id, data)).json()))
    response = await client.get(f"/api/admin/cameras/{camera_id}")
    view = CameraSetupView.model_validate(response.json())
    assert view.camera.id == camera_id and view.camera.videos_count == 2
    assert [v.id for v in view.videos] == [ids[1].video.id, ids[0].video.id]
    assert [j.video_id for j in view.jobs] == [ids[1].video.id, ids[0].video.id]
    assert (view.calibration, view.zones, view.broadcast) == (None, [], None)
    rows = {r.scenario: (r.enabled, r.params) for r in view.rules}  # no rows: the defaults
    assert len(rows) == 12 and rows["running"] == rows["fall"] == (True, {})
    assert (await client.get("/api/admin/cameras/999")).status_code == 404
