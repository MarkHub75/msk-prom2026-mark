"""Slice 25: a false alarm of the operator becomes a dataset item (tech.md 8.26)."""

import io
import json
import logging
import zipfile
from pathlib import Path

import httpx
import numpy as np
import pytest
from conftest import FakeClock
from test_analysis_api import _textured
from test_broadcast import camera
from test_jobs import _tune

from safewatch import cli, config, media, services, store
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import DatasetItem, DatasetView, EventDetail, FrameDetections, HudFrame

OPERATOR = {"X-Role": "operator"}
COMMENT = "Тень от крана, людей нет"
LABEL_KEYS = {
    "event_id", "label", "scenario", "level", "reason_text", "video_sha256", "video_filename",
    "start_ms", "end_ms", "models", "analysis_version", "comment",
}  # fmt: skip


def _settings(monkeypatch: pytest.MonkeyPatch, core: Settings, max_frames: int = 40) -> None:
    # The H.264 copy runs ffmpeg and plays no part in the dataset.
    _tune(monkeypatch, core, transcode={"enabled": False}, datasets={"max_frames": max_frames})


async def _false_alarm(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, clock: FakeClock
) -> int:
    """Demo scene on fake LinQ, the broadcast publishes, the operator calls it a false alarm."""
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), FakeRemoteShell()))
    services.video_import(camera(), _textured(tmp_path / "demo.mp4"))  # the name: demo scene
    job = await services.run_next_job()  # the background worker is off in tests
    assert job is not None and job.status == "done"
    for _ in range(40):
        clock.advance(0.5)
        services.broadcast_tick()
        row = store.one("SELECT id FROM events ORDER BY id LIMIT 1")
        if row is not None:
            break
    assert row is not None
    body = {"action": "false_alarm", "comment": COMMENT}
    r = await client.post(f"/api/events/{row['id']}/actions", json=body, headers=OPERATOR)
    assert r.status_code == 200, r.text
    assert EventDetail.model_validate(r.json()).event.status == "false_alarm"
    return int(row["id"])


def _items() -> list[dict[str, object]]:
    return [dict(r) for r in store.all("SELECT * FROM dataset_items ORDER BY id")]


async def test_false_alarm_creates_item_once(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
) -> None:
    _settings(monkeypatch, core)
    event_id = await _false_alarm(client, monkeypatch, tmp_path, fake_clock)
    assert await services.datasets_flush() == 1
    assert await services.datasets_flush() == 0  # UNIQUE event_id: one item for good
    (item,) = _items()
    assert (item["event_id"], item["label"]) == (event_id, "false_alarm")
    assert item["path"] == f"datasets/false_alarms/{event_id}/"
    frames = list((core.data_dir / str(item["path"]) / "frames").iterdir())
    assert 1 < len(frames) <= 40 and item["frames"] == len(frames)
    view = DatasetView.model_validate((await client.get("/api/datasets/false-alarms")).json())
    assert (view.total, view.frames) == (1, len(frames))
    assert [(i.event_id, i.scenario) for i in view.items] == [(event_id, item["scenario"])]


async def test_demo_event_no_item(core: Settings) -> None:
    services.seed_demo()
    found = store.one("SELECT count(*) AS n FROM events WHERE status = 'false_alarm'")
    assert found is not None and found["n"] > 0  # the seed has false alarms, none has an episode
    assert await services.datasets_flush() == 0
    assert _items() == [] and services.datasets_view().total == 0


async def test_item_files_and_label(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
) -> None:
    _settings(monkeypatch, core, max_frames=3)
    event_id = await _false_alarm(client, monkeypatch, tmp_path, fake_clock)
    assert await services.datasets_flush() == 1
    folder = core.data_dir / f"datasets/false_alarms/{event_id}"
    names = {int(p.stem) for p in (folder / "frames").glob("*.jpg")}
    assert len(names) == 3
    detail = EventDetail.model_validate((await client.get(f"/api/events/{event_id}")).json())
    clip = detail.event.clip
    assert clip is not None
    lines = (folder / "hud.jsonl").read_text(encoding="utf-8").splitlines()
    hud = [HudFrame.model_validate_json(line) for line in lines]
    assert {f.frame_idx for f in hud} == names
    assert all(clip.start_ms <= f.ts_ms <= clip.end_ms for f in hud)  # the clip window
    for name in ("detections.jsonl", "pose.jsonl"):
        lines = (folder / name).read_text(encoding="utf-8").splitlines()
        assert {FrameDetections.model_validate_json(line).frame_idx for line in lines} == names
    image = media.read_frame(folder / "frames" / f"{min(names)}.jpg", 0)
    assert isinstance(image, np.ndarray) and image.shape[:2] == (300, 1600)  # full size
    label = json.loads((folder / "label.json").read_text(encoding="utf-8"))
    assert set(label) == LABEL_KEYS
    video = store.one("SELECT * FROM videos")
    assert video is not None and detail.event.reason_text == label["reason_text"]
    assert (label["event_id"], label["label"], label["comment"]) == (
        event_id,
        "false_alarm",
        COMMENT,
    )
    assert (label["scenario"], label["level"]) == (detail.event.scenario, detail.event.level)
    assert (label["video_sha256"], label["video_filename"]) == (video["sha256"], "demo.mp4")
    episode = detail.episode
    assert episode is not None and (label["start_ms"], label["end_ms"]) == (
        episode.start_ms,
        episode.end_ms,
    )
    assert label["analysis_version"] == 1 and len(label["models"]) == 2  # detector and pose
    assert all("@" in m for m in label["models"])


async def test_export_zip_manifest(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
) -> None:
    _settings(monkeypatch, core, max_frames=3)
    event_id = await _false_alarm(client, monkeypatch, tmp_path, fake_clock)
    await services.datasets_flush()
    r = await client.get("/api/datasets/false-alarms/export.zip")
    assert r.status_code == 200 and r.headers["content-type"] == "application/zip"
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        names = set(zf.namelist())
        manifest = [DatasetItem.model_validate(i) for i in json.loads(zf.read("manifest.json"))]
    assert [i.event_id for i in manifest] == [event_id]
    folder = core.data_dir / manifest[0].path
    files = {p.relative_to(core.data_dir).as_posix() for p in folder.rglob("*") if p.is_file()}
    assert len(files) == 3 + 4 and names == files | {"manifest.json"}


def test_cli_export(core: Settings, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    out = tmp_path / "out"
    assert cli.main(["dataset", "export", "--out", str(out)]) == 0
    path = Path(capsys.readouterr().out.strip())
    assert path == out / "false_alarms.zip"
    with zipfile.ZipFile(path) as zf:
        assert zf.namelist() == ["manifest.json"] and json.loads(zf.read("manifest.json")) == []


async def test_frame_error_retries(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    _settings(monkeypatch, core, max_frames=3)
    event_id = await _false_alarm(client, monkeypatch, tmp_path, fake_clock)
    read_frame = media.read_frame

    def broken(path: Path, frame_idx: int) -> np.ndarray:
        raise ValueError(f"frame {frame_idx} of {path.name} is not readable")

    monkeypatch.setattr(media, "read_frame", broken)
    with caplog.at_level(logging.WARNING, logger="safewatch.services"):
        assert await services.datasets_flush() == 0
    assert f"dataset: event {event_id}: frame" in caplog.text
    assert _items() == [] and not (core.data_dir / "datasets").exists()
    monkeypatch.setattr(media, "read_frame", read_frame)
    assert await services.datasets_flush() == 1  # the next tick tries again
    assert [i["event_id"] for i in _items()] == [event_id]
