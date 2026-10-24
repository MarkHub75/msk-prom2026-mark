"""Slice 17: the demo pack (tech.md 8.19): build on fake LinQ, import, the world plays."""

import json
import shutil
from pathlib import Path

import httpx
import pytest
import yaml
from conftest import FakeClock
from test_analysis_api import _textured

from safewatch import cli, config, demo, services, store, texts
from safewatch.config import ROOT, Settings
from safewatch.errors import InferenceError, NotFound, UnsupportedVideo, ValidationFailed
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference import artifacts
from safewatch.inference.linq import LinqBackend
from safewatch.types import (
    DemoLayout,
    DemoPack,
    EventDetail,
    EventFilter,
    EventSummary,
    Fault,
)

SEED_SECTOR, SEED_CAMERA = texts.DEMO_SECTORS[0], texts.DEMO_CAMERAS[0][0]
NEW_SECTOR, NEW_CAMERA = "Сектор 9 · Демо-участок", "Камера 9.1 · Новая"
CALIBRATION = {
    "image_points": [[0.1, 0.5], [0.9, 0.5], [0.9, 0.95], [0.1, 0.95]],
    "world_points": [[0.0, 0.0], [8.0, 0.0], [8.0, 3.0], [0.0, 3.0]],
}
ZONE = {"kind": "danger", "name": "Пресс", "points": [[0.6, 0.3], [0.9, 0.3], [0.9, 0.9]]}
TABLES = ("sectors", "cameras", "zones", "calibrations", "camera_rules", "videos", "artifacts")
TABLES += ("jobs", "demo_packs")
OPERATOR, MASTER = {"X-Role": "operator"}, {"X-Role": "master"}


def _shell(
    monkeypatch: pytest.MonkeyPatch, script: list[Fault | None] | None = None
) -> FakeRemoteShell:
    shell = FakeRemoteShell(script)
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), shell))
    return shell


def _layout(tmp_path: Path, cameras: list[dict[str, object]] | None = None) -> Path:
    """Two cameras over one `demo.mp4` (the demo scene: a yellow run and a red fall)."""
    videos = tmp_path / "videos"
    videos.mkdir(exist_ok=True)
    _textured(videos / "demo.mp4")
    seed = {"sector": SEED_SECTOR, "name": SEED_CAMERA, "videos": [{"file": "demo.mp4"}]}
    seed["zones"] = [ZONE]  # the seed camera has its own zones: not written
    new = {"sector": NEW_SECTOR, "name": NEW_CAMERA, "videos": [{"file": "demo.mp4"}]}
    new |= {"calibration": CALIBRATION, "zones": [ZONE], "rules": {"fall": {"enabled": True}}}
    path = tmp_path / "layout.yaml"
    data = {"name": "argus", "cameras": cameras or [seed, new]}
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    return path


def _build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    _shell(monkeypatch)
    out = tmp_path / "pack"
    services.demo_build(_layout(tmp_path), tmp_path / "videos", out, allow_fake=True)
    return out


def _counts() -> dict[str, int]:
    return {t: store.one(f"SELECT count(*) AS n FROM {t}")["n"] for t in TABLES}  # type: ignore[index]


def test_build_writes_manifest_and_artifacts(
    fake_core: Settings, tmp_path: Path, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _counts()
    out = _build(tmp_path, monkeypatch)
    manifest = demo.read_manifest(out / demo.MANIFEST)
    assert manifest.name == "argus" and manifest.contract == "1.1.0"
    assert [c.name for c in manifest.cameras] == [SEED_CAMERA, NEW_CAMERA]
    video = manifest.cameras[0].videos[0]
    assert video.file == "videos/demo.mp4" and (out / video.file).is_file()
    assert video.sha256 == services._sha256(tmp_path / "videos" / "demo.mp4")
    refs = [fake_core.pipeline.detector, fake_core.pipeline.pose]
    assert [a.model for a in video.artifacts] == refs
    for a in video.artifacts:
        frames = artifacts.read_jsonl(out / a.file, a.frames)
        assert len(frames) == a.metrics.frames_processed == 200  # 10 fps -> step 1
        assert (a.backend, a.fake, a.metrics.fake, a.step) == ("linq", True, True, 1)
    assert manifest.cameras[1].videos[0] == video  # one run per video and model
    assert services._backend.shell.calls.count("start") == 2  # type: ignore[attr-defined]
    sha = demo.write_manifest(tmp_path / "copy.json", manifest)
    assert sha == services._sha256(tmp_path / "copy.json")
    assert _counts() == before  # files only
    with pytest.raises(ValidationFailed):  # the out folder is not empty
        services.demo_build(_layout(tmp_path), tmp_path / "videos", out, allow_fake=True)
    with pytest.raises(NotFound):
        services.demo_build(tmp_path / "nope.yaml", tmp_path / "videos", tmp_path / "x", True)
    missing = _layout(tmp_path, [{"sector": "С", "name": "К", "videos": [{"file": "no.mp4"}]}])
    with pytest.raises(NotFound):
        services.demo_build(missing, tmp_path / "videos", tmp_path / "x", allow_fake=True)
    (tmp_path / "videos" / "bad.mp4").write_bytes(b"not a video")
    bad = _layout(tmp_path, [{"sector": "С", "name": "К", "videos": [{"file": "bad.mp4"}]}])
    with pytest.raises(UnsupportedVideo):
        services.demo_build(bad, tmp_path / "videos", tmp_path / "x", allow_fake=True)
    (tmp_path / "broken.yaml").write_text("name: x\ncameras: 5\n", encoding="utf-8")
    with pytest.raises(ValidationFailed):
        services.demo_build(tmp_path / "broken.yaml", tmp_path / "videos", tmp_path / "x", True)
    _shell(monkeypatch, ["unavailable"])
    with pytest.raises(InferenceError):
        services.demo_build(_layout(tmp_path), tmp_path / "videos", tmp_path / "x", True)
    assert not (tmp_path / "x").exists()  # no half of a pack


def test_build_refuses_fake_without_flag(
    fake_core: Settings, tmp_path: Path, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shell = _shell(monkeypatch)
    with pytest.raises(ValidationFailed, match="--allow-fake"):
        services.demo_build(_layout(tmp_path), tmp_path / "videos", tmp_path / "pack")
    assert shell.calls == [] and not (tmp_path / "pack").exists()


async def test_import_creates_world_without_inference(
    core: Settings,
    fake_core: Settings,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    fake_clock: FakeClock,
) -> None:
    out = _build(tmp_path, monkeypatch)
    monkeypatch.setattr(config, "get_settings", lambda: core)  # the server runs without fake
    shell = _shell(monkeypatch)
    services.seed_demo()
    seed_camera = store.one("SELECT id FROM cameras WHERE name = ?", SEED_CAMERA)["id"]  # type: ignore[index]
    seed_zones = services.zones_list(seed_camera)
    report = services.demo_import(out)
    assert (report.skipped, report.cameras, report.videos, report.jobs) == (False, 2, 2, 2)
    new_camera = store.one("SELECT id FROM cameras WHERE name = ?", NEW_CAMERA)["id"]  # type: ignore[index]
    camera = services.camera_get(new_camera)
    sectors = {s.id: s.name for s in services.sectors_list()}
    assert not camera.is_demo and sectors[camera.sector_id] == NEW_SECTOR
    assert services.zones_list(seed_camera) == seed_zones  # setup of the seed camera kept
    assert [(z.kind, z.name) for z in services.zones_list(new_camera)] == [("danger", "Пресс")]
    assert services.calibration_get(new_camera) is not None
    assert services.calibration_get(seed_camera) is None
    rules = {r.scenario: r for r in services.camera_rules(new_camera)}
    assert rules["fall"].enabled
    jobs = services.jobs_list()
    assert {(j.backend, j.fake, j.status) for j in jobs} == {("linq", True, "queued")}
    fake_clock.advance(1)  # imported artifacts are older than the start of the job
    for _ in jobs:
        job = await services.run_next_job()
        assert job is not None and job.status == "done", job
        assert [m.cached for m in job.metrics] == [True, True]
    assert "start" not in shell.calls
    for camera_id in (seed_camera, new_camera):
        assert services.broadcast_get(camera_id).status == "playing"  # type: ignore[union-attr]
        video = services.videos_list(camera_id)[0]
        assert services.video_analysis(video.id).episodes


async def test_import_is_idempotent(
    fake_core: Settings,
    client: httpx.AsyncClient,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    out = _build(tmp_path, monkeypatch)
    services.seed_demo()
    assert services.demo_import(out).skipped is False
    counts = _counts()
    again = services.demo_import(out)
    assert (again.skipped, again.name, again.jobs) == (True, "argus", 0)
    assert _counts() == counts
    r = await client.get("/api/demo/packs")
    assert r.status_code == 200
    (pack,) = [DemoPack.model_validate(p) for p in r.json()]
    sha = services._sha256(out / demo.MANIFEST)
    assert (pack.name, pack.fake, pack.backend, pack.sha256) == ("argus", True, "linq", sha)
    assert (pack.cameras, pack.videos) == (2, 2)


def test_import_rejects_broken_pack(
    fake_core: Settings,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = _build(tmp_path, monkeypatch)
    services.seed_demo()
    counts = _counts()
    data = json.loads((out / demo.MANIFEST).read_text(encoding="utf-8"))
    unknown = tmp_path / "unknown"
    shutil.copytree(out, unknown)
    data["cameras"][1]["videos"][0]["artifacts"][0]["model"] = "det-nope@1"
    (unknown / demo.MANIFEST).write_text(json.dumps(data), encoding="utf-8")
    assert cli.main(["demo", "import", str(unknown)]) == 2
    assert "det-nope@1" in capsys.readouterr().err
    foreign = tmp_path / "foreign"
    shutil.copytree(out, foreign)
    _textured(foreign / "videos" / "demo.mp4", seed=1)  # another video under the same name
    with pytest.raises(ValidationFailed, match="sha256"):
        services.demo_import(foreign)
    assert cli.main(["demo", "import", str(foreign)]) == 2
    assert cli.main(["demo", "import", str(tmp_path / "none")]) == 3
    assert _counts() == counts


def test_serve_autoloads_pack(
    fake_core: Settings,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    out = _build(tmp_path, monkeypatch)
    off = fake_core.model_copy(update={"demo": fake_core.demo.model_copy(update={"pack": out})})
    off.demo.autoload = False
    monkeypatch.setattr(config, "get_settings", lambda: off)
    cli.seed_on_serve()
    assert store.demo_world_exists() and services.demo_packs() == []
    on = off.model_copy(update={"demo": off.demo.model_copy(update={"autoload": True})})
    monkeypatch.setattr(config, "get_settings", lambda: on)
    cli.seed_on_serve()
    assert [p.name for p in services.demo_packs()] == ["argus"]
    gone = on.model_copy(update={"demo": on.demo.model_copy(update={"pack": tmp_path / "no"})})
    monkeypatch.setattr(config, "get_settings", lambda: gone)
    cli.seed_on_serve()  # no folder: nothing to import, the server starts
    assert len(services.demo_packs()) == 1


async def _act(client: httpx.AsyncClient, event_id: int, role: dict[str, str], **body: str) -> str:
    r = await client.post(f"/api/events/{event_id}/actions", json=body, headers=role)
    assert r.status_code == 200, r.text
    return EventDetail.model_validate(r.json()).event.status


async def test_demo_flow_reaches_master_and_journal(
    fake_core: Settings,
    client: httpx.AsyncClient,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    fake_clock: FakeClock,
) -> None:
    out = _build(tmp_path, monkeypatch)
    services.seed_demo()
    services.demo_import(out)
    fake_clock.advance(1)
    while await services.run_next_job() is not None:
        pass
    red = None
    for _ in range(40):  # the broadcast plays by the server clock
        fake_clock.advance(0.5)
        services.broadcast_tick()
        feed = (await client.get("/api/operator/feed", headers=OPERATOR)).json()
        red = next((e for e in map(EventSummary.model_validate, feed) if e.level == "red"), None)
        if red is not None:
            break
    assert red is not None and not red.is_demo
    assert await _act(client, red.id, OPERATOR, action="confirm") == "sent_to_master"
    assert await _act(client, red.id, MASTER, action="accept") == "master_accepted"
    assert await _act(client, red.id, MASTER, action="resolve", comment="Помог") == "resolved"
    page = services.events_list(EventFilter(camera_id=red.camera_id, scenario="fall"))
    assert red.clip is not None  # the episode of the pack video (tech.md 8.20)
    assert [(e.id, e.status, e.clip) for e in page.items] == [(red.id, "resolved", red.clip)]


def test_cli_build_and_import(
    fake_core: Settings,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _shell(monkeypatch)
    layout, videos, out = _layout(tmp_path), str(tmp_path / "videos"), tmp_path / "pack"
    build = ["demo", "build", str(layout), "--videos", videos, "--out", str(out)]
    assert cli.main(build) == 2 and not out.exists()
    assert cli.main([*build, "--allow-fake"]) == 0
    printed = json.loads(capsys.readouterr().out)
    first = printed["cameras"][0]["videos"][0]["artifacts"][0]
    assert first["frames"] == 200 and "metrics" not in first
    assert cli.main([*build, "--allow-fake"]) == 2  # not empty
    no_video = ["demo", "build", str(layout), "--videos", str(tmp_path), "--allow-fake"]
    assert cli.main([*no_video, "--out", str(tmp_path / "x")]) == 3
    _shell(monkeypatch, ["unavailable"])
    failed = tmp_path / "failed"
    cmd = ["demo", "build", str(layout), "--videos", videos, "--out", str(failed), "--allow-fake"]
    assert cli.main(cmd) == 4 and not failed.exists()
    assert cli.main(["demo", "import", str(out)]) == 0
    assert json.loads(capsys.readouterr().out.splitlines()[-1])["jobs"] == 2


def test_example_layout_is_valid(core: Settings) -> None:
    path = ROOT / "config" / "demo.example.yaml"
    layout = DemoLayout.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    (camera,) = layout.cameras
    assert (camera.sector, camera.name) == (SEED_SECTOR, SEED_CAMERA)  # binds to the seed
    assert [v.file for v in camera.videos] == ["synthetic_coco_40x1s.mp4"]
    kinds = {k.id for k in core.zone_kinds}
    assert [z.kind for z in camera.zones] == ["danger"] and kinds >= {"danger"}
    assert core.demo.pack == Path("data/demo/argus") and core.demo.autoload
