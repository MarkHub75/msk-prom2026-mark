"""Slice 18: the event clip and the H.264 copy for the browser (tech.md 8.20)."""

import hashlib
import logging
from pathlib import Path
from typing import Any

import httpx
import imageio_ffmpeg
import psutil
import pytest
from conftest import FakeClock
from test_e2e import _flow
from test_videos import _camera, _upload

from safewatch import config, media, services, store
from safewatch.config import Settings
from safewatch.types import EventDetail, EventFilter, UploadResult


def _has_ffmpeg() -> bool:
    try:
        imageio_ffmpeg.get_ffmpeg_exe()
    except RuntimeError:
        return False
    return True


FFMPEG = pytest.mark.skipif(not _has_ffmpeg(), reason="imageio-ffmpeg has no ffmpeg here")


def _tune(monkeypatch: pytest.MonkeyPatch, core: Settings, **transcode: Any) -> Settings:
    tuned = core.model_copy(update={"transcode": core.transcode.model_copy(update=transcode)})
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    return tuned


def _row(start_ms: int, confirm_ms: int, duration_ms: int = 60_000) -> dict[str, Any]:
    return {
        "clip_video_id": 5,
        "clip_start_ms": start_ms,
        "clip_confirm_ms": confirm_ms,
        "clip_duration_ms": duration_ms,
        "clip_browser_playable": 0,
        "clip_web_path": None,
    }


def _no_ffmpeg_running() -> bool:
    return not [p for p in psutil.Process().children(recursive=True) if "ffmpeg" in p.name()]


def _web_files(core: Settings) -> list[str]:
    folder = core.data_dir / "uploads"
    return sorted(p.name for p in folder.iterdir() if ".web." in p.name)


def test_clip_window_bounds(core: Settings) -> None:
    def window(row: dict[str, Any]) -> tuple[int, int]:
        clip = services._clip(row)
        assert clip is not None
        return clip.start_ms, clip.end_ms

    assert window(_row(1000, 2000)) == (0, 7000)  # 3 s before cut at the video start
    clip = services._clip(_row(10_000, 11_000))
    assert clip is not None and (clip.start_ms, clip.end_ms) == (7000, 16_000)
    assert (clip.video_id, clip.url) == (5, "/api/videos/5/file#t=7.0,16.0")
    assert window(_row(10_000, 11_000, duration_ms=14_000)) == (7000, 14_000)  # video end
    assert window(_row(10_000, 40_000)) == (7000, 37_000)  # clips.max_s = 30
    assert window(_row(10_000, 31_999)) == (7000, 36_999)  # just under max_s
    assert services._clip({**_row(0, 0), "clip_video_id": None}) is None
    assert clip.playable is False
    copy = services._clip({**_row(0, 0), "clip_web_path": "uploads/x.web.mp4"})
    assert copy is not None and copy.playable is True


def test_clip_none_for_seed_demo(core: Settings) -> None:
    services.seed_demo()
    items = services.events_list(EventFilter(limit=200)).items
    assert items and all(e.is_demo for e in items)
    assert [e.clip for e in items] == [None] * len(items)


async def test_clip_in_feed_journal_detail(
    client: httpx.AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
) -> None:
    camera_id, event_id = await _flow(client, monkeypatch, tmp_path, linq_tails, fake_clock)
    sql = """SELECT ep.start_ms, ep.confirm_ms, v.id, v.duration_ms FROM events e
JOIN episodes ep ON ep.id = e.episode_id JOIN analyses an ON an.id = ep.analysis_id
JOIN videos v ON v.id = an.video_id WHERE e.id = ?"""
    row = store.one(sql, event_id)
    assert row is not None
    start_ms = max(0, row["start_ms"] - 3000)
    end_ms = min(row["duration_ms"], row["confirm_ms"] + 5000, start_ms + 30_000)
    detail = EventDetail.model_validate((await client.get(f"/api/events/{event_id}")).json())
    clip = detail.event.clip
    assert clip is not None and (clip.video_id, clip.start_ms, clip.end_ms) == (
        row["id"],
        start_ms,
        end_ms,
    )
    assert clip.url == f"/api/videos/{row['id']}/file#t={start_ms / 1000:.1f},{end_ms / 1000:.1f}"
    assert clip.playable is _has_ffmpeg()  # the demo video is mp4v: playable through the copy
    journal = services.events_list(EventFilter(camera_id=camera_id)).items
    feed = services.operator_feed()
    master = services.master_inbox_view().recent_resolved
    for items in (journal, feed, master):
        assert [e.clip for e in items if e.id == event_id] == [clip]


@FFMPEG
async def test_transcode_makes_browser_codec(
    client: httpx.AsyncClient, core: Settings, tmp_path: Path, make_video
) -> None:
    source = make_video(tmp_path, 2, 25)
    data = source.read_bytes()
    r = await _upload(client, _camera(), data)
    assert r.status_code == 201, r.text
    video = UploadResult.model_validate(r.json()).video
    sha = hashlib.sha256(data).hexdigest()
    row = store.video(video.id)
    assert row is not None
    assert (row["path"], row["web_path"]) == (f"uploads/{sha}.mp4", f"uploads/{sha}.web.mp4")
    assert (video.sha256, video.codec, video.browser_playable, video.web_playable) == (
        sha,
        "mp4v",
        False,
        True,
    )
    copy = media.probe_video(core.data_dir / row["web_path"])
    assert copy is not None and copy.codec in ("avc1", "h264")
    assert (copy.frame_count, copy.fps, copy.width, copy.height) == (50, 25, 320, 240)
    # The import of the same file takes the copy already made.
    other = services.video_import(_camera("Камера 2"), source).video
    assert store.video(other.id)["web_path"] == row["web_path"] and other.web_playable
    assert _no_ffmpeg_running()


@FFMPEG
async def test_video_file_serves_web_copy(
    client: httpx.AsyncClient, core: Settings, tmp_path: Path, make_video
) -> None:
    data = make_video(tmp_path, 1, 25).read_bytes()
    video = UploadResult.model_validate((await _upload(client, _camera(), data)).json()).video
    copy = (core.data_dir / "uploads" / f"{video.sha256}{media.WEB_SUFFIX}").read_bytes()
    part = await client.get(f"/api/videos/{video.id}/file", headers={"Range": "bytes=0-99"})
    assert part.status_code == 206
    assert part.content == copy[:100] and part.content != data[:100]
    assert part.headers["content-range"] == f"bytes 0-99/{len(copy)}"
    assert part.headers["content-type"] == "video/mp4"


async def test_transcode_disabled_key(
    client: httpx.AsyncClient,
    core: Settings,
    tmp_path: Path,
    make_video,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _tune(monkeypatch, core, enabled=False)
    data = make_video(tmp_path, 1, 25).read_bytes()
    video = UploadResult.model_validate((await _upload(client, _camera(), data)).json()).video
    assert (video.browser_playable, video.web_playable) == (False, False)
    assert store.video(video.id)["web_path"] is None
    assert _web_files(core) == []


async def test_transcode_failure_keeps_video(
    client: httpx.AsyncClient,
    core: Settings,
    tmp_path: Path,
    make_video,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING, logger="safewatch.media")
    with monkeypatch.context() as patch:  # ffmpeg is not where imageio-ffmpeg says
        patch.setattr(imageio_ffmpeg, "get_ffmpeg_exe", lambda: str(tmp_path / "no-ffmpeg.exe"))
        r = await _upload(client, _camera(), make_video(tmp_path, 1, 25).read_bytes())
    assert r.status_code == 201, r.text
    video = UploadResult.model_validate(r.json()).video
    assert (video.status, video.web_playable) == ("uploaded", False)
    assert store.video(video.id)["web_path"] is None
    assert _web_files(core) == [] and "transcode:" in caplog.text
    if not _has_ffmpeg():
        return
    # The real ffmpeg, killed by the timeout: the upload still succeeds, no process stays.
    caplog.clear()
    _tune(monkeypatch, core, timeout_s=0.001)
    data = make_video(tmp_path, 2, 25, name="slow.mp4").read_bytes()
    r = await _upload(client, _camera("Камера 2"), data)
    assert r.status_code == 201, r.text
    video = UploadResult.model_validate(r.json()).video
    assert video.web_playable is False and store.video(video.id)["web_path"] is None
    assert "transcode: timeout" in caplog.text
    assert _web_files(core) == [] and _no_ffmpeg_running()


@FFMPEG
async def test_h264_not_transcoded(
    client: httpx.AsyncClient,
    core: Settings,
    tmp_path: Path,
    make_video,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h264 = tmp_path / "h264.mp4"
    assert media.transcode(make_video(tmp_path, 1, 25), h264, core.transcode)

    def forbidden(*args: object) -> bool:
        raise AssertionError("an H.264 source needs no copy")

    monkeypatch.setattr(media, "transcode", forbidden)
    video = UploadResult.model_validate(
        (await _upload(client, _camera(), h264.read_bytes())).json()
    )
    assert video.video.codec in ("avc1", "h264")
    assert (video.video.browser_playable, video.video.web_playable) == (True, True)
    assert store.video(video.video.id)["web_path"] is None
    assert _web_files(core) == []
