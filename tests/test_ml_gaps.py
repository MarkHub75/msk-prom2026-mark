"""Slice 29: gaps of docs/ML_INTEGRATION.md (tech.md 8.30 items 1, 2, 3, 4, 7, 8, 10, 11, 14)."""

import hashlib
import sys
import types
from pathlib import Path
from typing import Any

import pytest
import test_plugin_status
from test_jobs import _tune, _video
from test_linq_backend import RecordingShell
from test_plugin_status import statuses

from safewatch import cli, config, registry, rules, services, store
from safewatch.analysis.pipeline import analyze
from safewatch.config import Settings
from safewatch.fakes import scenes
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference import local
from safewatch.inference.linq import LinqBackend
from safewatch.inference.local import LocalBackend
from safewatch.types import AnalysisConfig, Detection, FrameDetections, ModelSpec

extra_registry = test_plugin_status.extra_registry  # the fixture: a registry with fire-test@1
FIRE_REF = "matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4"  # no TPU program: model_missing


def _start(fake_core: Settings, tmp_path: Path, make_video, model: ModelSpec) -> RecordingShell:
    """One LinQ run of `model` on the fake; the shell keeps the commands and uploads."""
    shell = RecordingShell()
    clip = make_video(tmp_path, 1, 25)
    sha = hashlib.sha256(clip.read_bytes()).hexdigest()
    out = tmp_path / "artifacts" / f"{'a' * 64}.jsonl"
    LinqBackend(fake_core, shell).run(clip, sha, model, 2, out, lambda share: None)
    return shell


def _start_command(shell: RecordingShell) -> str:
    (cmd,) = [c for c in shell.commands if c.endswith("# sw:start")]
    return cmd


async def test_import_artifact_cli_and_cache(
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pipeline = core.pipeline.model_copy(update={"pose": None})
    tuned = core.model_copy(update={"inference_backend": "local", "pipeline": pipeline})
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    video_id = _video(tmp_path, make_video, seconds=1)  # queued on `local`
    step = services.analysis_step(25)
    jsonl = tmp_path / "vast.jsonl"
    frames = scenes.render("demo", 320, 240, 25, 25, step, "detect")
    jsonl.write_text(scenes.to_jsonl(frames), encoding="utf-8", newline="\n")
    ref = tuned.pipeline.detector
    argv = ["import-artifact", str(jsonl), "--video", str(video_id), "--model", ref]
    assert cli.main([*argv, "--backend", "local"]) == 0
    artifact_id = int(capsys.readouterr().out.strip())
    row = store.artifact_by_id(artifact_id)
    assert row is not None and (row["backend"], row["fake"], row["step"]) == ("local", 0, step)

    def no_run(*args: Any) -> None:
        raise AssertionError("the job must take the imported artifact")

    monkeypatch.setattr(LocalBackend, "run", no_run)
    monkeypatch.setattr(services, "_backend", LocalBackend(tuned))
    job = await services.run_next_job()
    assert job is not None and job.status == "done"
    assert store.job(job.id)["det_artifact_id"] == artifact_id
    assert [(m.backend, m.model_id) for m in job.metrics] == [("local", "det-yolov8n")]

    bad = tmp_path / "bad.jsonl"
    bad.write_text("not json\n", encoding="utf-8")
    assert cli.main(["import-artifact", str(bad), "--video", str(video_id), "--model", ref]) == 2
    assert cli.main([*argv[:4], "--model", "nope@1"]) == 2
    assert cli.main(["import-artifact", str(jsonl), "--video", "999", "--model", ref]) == 3
    assert cli.main(["import-artifact", str(tmp_path / "gone.jsonl"), *argv[2:]]) == 3


def test_detector_nc_passed(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    detector = registry.resolve(fake_core.pipeline.detector)
    own = detector.model_copy(update={"nc": 2, "classes": {0: "person", 1: "forklift", 7: "x"}})
    cmd = _start_command(_start(fake_core, tmp_path, make_video, own))
    assert "--nc 2" in cmd and "--classes 0,1 " in cmd
    coco = _start_command(_start(fake_core, tmp_path, make_video, detector))
    assert "--nc" not in coco and "--classes 0,2,5,6,7,67 " in coco


def test_input_name_passed(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    detector = registry.resolve(fake_core.pipeline.detector)
    named = detector.model_copy(update={"input_name": "input0"})
    assert "--input-name input0" in _start_command(_start(fake_core, tmp_path, make_video, named))
    plain = _start_command(_start(fake_core, tmp_path, make_video, detector))
    assert "--input-name" not in plain  # the worker takes `images`


def test_tail_optional(
    fake_core: Settings, tmp_path: Path, make_video, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No tail file anywhere (no `linq_tails`): a full-graph program needs none."""
    full = registry.resolve(fake_core.pipeline.detector).model_copy(update={"linq_tail": None})
    shell = _start(fake_core, tmp_path, make_video, full)
    assert "--tail" not in _start_command(shell)
    assert not any("/tails/" in remote for remote in shell.uploads)
    monkeypatch.setattr(registry, "active_models", lambda settings: [full])
    status = LinqBackend(fake_core, FakeRemoteShell()).check()
    assert (status.state, status.missing) == ("ok", [])


def test_vehicle_classes_from_config(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    _tune(monkeypatch, core, pipeline={"vehicle_classes": ["truck", "forklift"]})
    lift = ModelSpec(
        id="forklift-test", version="1", task="detect", input_size=640, conf=0.1, iou=0.45,
        classes={0: "forklift"}, linq_program="baseline_lift.tpu", linq_tail=None, local_onnx=None,
    )  # fmt: skip
    person = Detection(cls=0, name="", score=0.9, bbox_xyxy=(480.0, 200.0, 520.0, 300.0))
    det, extra = [], []
    for i in range(30):  # 10 fps, 3 s: the forklift drives at 0.5 own heights per second
        det.append(FrameDetections(frame_idx=i, ts_ms=i * 100.0, detections=[person]))
        box = (200.0 + 5 * i, 200.0, 300.0 + 5 * i, 300.0)
        machine = Detection(cls=0, name="", score=0.9, bbox_xyxy=box)
        extra.append(FrameDetections(frame_idx=i, ts_ms=i * 100.0, detections=[machine]))
    cfg = AnalysisConfig(
        width=1000, height=500, fps=10, step=1, duration_ms=3000, calibration=None, zones=[],
        rules={}, class_conf=core.class_conf, active_classes=["person", "forklift"],
    )  # fmt: skip
    detector = registry.resolve(core.pipeline.detector)
    result = analyze(det, None, Path("unused.mp4"), cfg, None, detector, [(lift, extra)])
    tracked = [o for f in result.hud for o in f.objects if o.label == "forklift"]
    assert tracked and all(o.kind == "vehicle" and o.track_id is not None for o in tracked)
    assert {o.track_id for o in tracked} == {tracked[0].track_id}
    assert [e.scenario for e in result.episodes] == ["proximity"]
    assert result.episodes[0].subject.startswith("pair:")


def test_proximity_any_vehicle(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    _tune(monkeypatch, core, pipeline={"vehicle_classes": ["truck", "forklift"]})
    assert statuses(["person", "forklift"])["proximity"][0] == "active"
    assert statuses(["person", "truck"])["proximity"][0] == "active"
    assert statuses(["person", "car"])["proximity"] == (
        "model_missing",
        "Модель не подключена: нужны классы truck, forklift",
    )
    assert statuses(["forklift"])["proximity"] == (
        "model_missing",
        "Модель не подключена: нужны классы person",
    )
    meta = {m.id: m for m in rules.scenario_metas(["person"])}["proximity"]
    assert meta.required_classes == ["person", "truck", "forklift"]


@pytest.mark.parametrize("fault", ["remote_error", "bad_output", "model_missing"])
async def test_extra_failure_falls_back(
    fault: str,
    fake_core: Settings,
    extra_registry: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
) -> None:
    # model_missing: Matvey's fire model has no TPU program, its run stops before `# sw:home`.
    ref = FIRE_REF if fault == "model_missing" else "fire-test@1"
    tuned = _tune(monkeypatch, fake_core, pipeline={"extra": [ref]})
    script = [None] if fault == "model_missing" else [None, fault, None]  # det, extra, pose
    shell = FakeRemoteShell(script)  # type: ignore[arg-type]
    monkeypatch.setattr(services, "_backend", LinqBackend(tuned, shell))
    video_id = _video(tmp_path, make_video, seconds=1)
    job = await services.run_next_job()
    assert job is not None and job.status == "done" and job.error_code is None
    assert job.error_text is not None and job.error_text.startswith(f"extra {ref}: ")
    assert [m.task for m in job.metrics] == ["detect", "pose"]
    analysis = store.analysis(store.video(video_id)["active_analysis_id"])
    cfg = AnalysisConfig.model_validate_json(analysis["config_json"])
    assert cfg.extra_artifact_ids == [] and "fire" not in cfg.active_classes
    assert statuses(cfg.active_classes)["fire_smoking"][0] == "model_missing"
    assert statuses(registry.active_classes(tuned))["fire_smoking"][0] == "active"


async def test_extra_metrics_in_job(
    fake_core: Settings,
    extra_registry: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
) -> None:
    tuned = _tune(monkeypatch, fake_core, pipeline={"extra": ["fire-test@1"]})
    monkeypatch.setattr(services, "_backend", LinqBackend(tuned, FakeRemoteShell()))
    video_id = _video(tmp_path, make_video, seconds=1)
    job = await services.run_next_job()
    assert job is not None and job.status == "done"
    expected = [("det-yolov8n", False), ("pose-yolov8n", False), ("fire-test", False)]
    assert [(m.model_id, m.cached) for m in services.job_get(job.id).metrics] == expected
    (listed,) = services.jobs_list()
    assert [m.model_id for m in listed.metrics] == [m for m, _ in expected]
    services.video_recompute(video_id, "admin")
    again = await services.run_next_job()
    assert again is not None
    assert [(m.model_id, m.cached) for m in again.metrics] == [(m, True) for m, _ in expected]


def test_local_providers_key(
    core: Settings, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    seen: list[list[str]] = []

    class Session:
        def __init__(self, path: str, options: object, providers: list[str]) -> None:
            seen.append(providers)

    fake_ort = types.SimpleNamespace(
        SessionOptions=lambda: types.SimpleNamespace(), InferenceSession=Session
    )
    monkeypatch.setitem(sys.modules, "onnxruntime", fake_ort)
    monkeypatch.setattr(local, "ROOT", tmp_path)
    model = registry.resolve(core.pipeline.detector)
    (tmp_path / str(model.local_onnx)).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / str(model.local_onnx)).write_bytes(b"onnx")
    LocalBackend(core)._session(model)
    gpu = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    LocalBackend(_tune(monkeypatch, core, local={"providers": gpu}))._session(model)
    assert seen == [["CPUExecutionProvider"], gpu]
