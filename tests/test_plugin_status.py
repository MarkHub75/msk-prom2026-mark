"""Slice 10: plugin statuses from the active model classes, extra models, worker `--nc`."""

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pytest
import yaml
from test_jobs import _tune, _video
from test_linq_backend import RecordingShell
from test_rule_phone import ctx_with, worker
from test_rule_running import zone

from safewatch import registry, rules, services
from safewatch.config import Settings
from safewatch.inference.linq import LinqBackend
from safewatch.rules.harness import HarnessPlugin
from safewatch.rules.suspended_load import SuspendedLoadPlugin
from safewatch.types import ObjectState

DEFAULT = ["person", "car", "bus", "train", "truck", "cell phone"]
ORDER = [
    "running", "proximity", "phone", "fall", "fence_crossing", "restricted_under",
    "fire_smoking", "no_harness", "suspended_load", "load_carrying",
]  # fmt: skip
FIRE_MODEL = {
    "id": "fire-test",
    "version": "1",
    "task": "detect",
    "input_size": 640,
    "conf": 0.1,
    "iou": 0.45,
    "classes": {0: "fire", 1: "smoke"},
    "linq_program": "baseline_fire.tpu",
    "linq_tail": "models/linq/fire/fire_tail.onnx",
    "local_onnx": None,
}


def statuses(classes: list[str]) -> dict[str, tuple[str, str]]:
    return {m.id: (m.status, m.status_text) for m in rules.scenario_metas(classes)}


def test_status_follows_active_model_classes(core: Settings) -> None:
    default = statuses(DEFAULT)
    assert default["fire_smoking"] == (
        "model_missing",
        "Нет модели с классами: fire, smoke, cigarette",
    )
    assert default["no_harness"] == ("model_missing", "Нет модели с классами: no_harness")
    assert default["suspended_load"] == ("model_missing", "Нет модели с классами: suspended_load")
    for scenario in ("running", "proximity", "phone", "fall", "fence_crossing", "restricted_under"):
        assert default[scenario] == ("active", "Сценарий работает")
    # fire_smoking needs any one of its classes, the others need all of theirs.
    for one in ("fire", "smoke", "cigarette"):
        assert statuses([*DEFAULT, one])["fire_smoking"][0] == "active"
    assert statuses([*DEFAULT, "no_harness"])["no_harness"][0] == "active"
    assert statuses([*DEFAULT, "suspended_load"])["suspended_load"][0] == "active"
    no_truck = statuses([c for c in DEFAULT if c != "truck"])
    assert no_truck["proximity"] == ("model_missing", "Нет модели с классами: truck")
    assert statuses(["person"])["phone"] == ("model_missing", "Нет модели с классами: cell phone")
    # The registry of the running config is the default snapshot.
    assert statuses(registry.active_classes(core)) == default


def test_harness_and_suspended_load_rows() -> None:
    height = [zone("height", name="Площадка")]
    flag = ObjectState(name="no_harness", bbox=(500.0, 120.0, 520.0, 160.0), score=0.6)
    plugin, params = HarnessPlugin(), rules.defaults("no_harness")
    (o,) = plugin.observe(ctx_with([worker()], [flag], height), params)
    assert (o.state, o.level, o.hold_s, o.reason_text) == (
        "P",
        "yellow",
        3.0,
        "Работа на высоте без привязи",
    )
    assert plugin.observe(ctx_with([worker()], [], height), params)[0].state == "N"
    assert plugin.observe(ctx_with([worker()], [flag]), params)[0].state == "N"  # not at height
    apart = flag.model_copy(update={"bbox": (550.0, 120.0, 570.0, 160.0)})  # touches the edge
    assert plugin.observe(ctx_with([worker()], [apart], height), params)[0].state == "N"
    assert (
        plugin.observe(ctx_with([worker()], [flag], height), {"harness_hold_s": 5.0})[0].hold_s
        == 5.0
    )

    # The foot is at (500, 300): a load above it, within x 450..550, ends at y = 299.
    load = ObjectState(name="suspended_load", bbox=(450.0, 0.0, 550.0, 299.0), score=0.7)
    crane, values = SuspendedLoadPlugin(), rules.defaults("suspended_load")
    (o,) = crane.observe(ctx_with([worker()], [load]), values)
    assert (o.state, o.level, o.hold_s, o.reason_text) == (
        "P",
        "red",
        0.5,
        "Человек под подвешенным грузом",
    )
    low = load.model_copy(update={"bbox": (450.0, 0.0, 550.0, 300.0)})  # not above the foot
    assert crane.observe(ctx_with([worker()], [low]), values)[0].state == "N"
    aside = load.model_copy(update={"bbox": (501.0, 0.0, 600.0, 299.0)})
    assert crane.observe(ctx_with([worker()], [aside]), values)[0].state == "N"
    assert crane.observe(ctx_with([worker()], [load]), {"load_hold_s": 1.0})[0].hold_s == 1.0


def test_skeletons_listed_with_texts(core: Settings) -> None:
    assert [p.meta.id for p in rules.PLUGINS] == ORDER
    metas = {m.id: m for m in rules.scenario_metas()}
    skeleton = metas["load_carrying"]
    assert (skeleton.status, skeleton.status_text) == (
        "skeleton",
        "Сценарий уточняется: правила переноски не определены",
    )
    assert rules.plugin("load_carrying").observe(ctx_with([worker()], []), {}) == []
    assert [m.status for m in rules.scenario_metas([*DEFAULT, "fire"])].count("skeleton") == 1
    with pytest.raises(KeyError):
        rules.plugin("helmet")


@pytest.fixture
def extra_registry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, linq_tails: Path) -> Path:
    """config/models.yaml plus a fire model, its tail file in the fake repo root."""
    data = yaml.safe_load(registry.MODELS_FILE.read_text(encoding="utf-8"))
    data["models"].append(FIRE_MODEL)
    path = tmp_path / "models.yaml"
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(registry, "MODELS_FILE", path)
    tail = linq_tails / str(FIRE_MODEL["linq_tail"])
    tail.parent.mkdir(parents=True, exist_ok=True)
    tail.write_bytes(b"onnx")
    return path


async def test_extra_model_enables_fire_without_code(
    fake_core: Settings,
    extra_registry: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
) -> None:
    tuned = _tune(monkeypatch, fake_core, pipeline={"extra": ["fire-test@1"]})
    assert {m.id: m.status for m in rules.scenario_metas()}["fire_smoking"] == "active"
    assert {m.id: m.status for m in rules.scenario_metas()}["no_harness"] == "model_missing"

    shell = RecordingShell()
    monkeypatch.setattr(services, "_backend", LinqBackend(tuned, shell))
    _video(tmp_path, make_video, seconds=1)
    job = await services.run_next_job()
    assert job is not None and job.status == "done"
    assert [m.model_id for m in job.metrics] == ["det-yolov8n", "pose-yolov8n"]  # job columns
    starts = [c for c in shell.commands if c.endswith("# sw:start")]
    assert len(starts) == 3  # detector, extra model, pose
    (fire,) = [c for c in starts if "baseline_fire.tpu" in c]
    assert "--nc 2" in fire and "--classes" not in fire
    assert all("--nc" not in c for c in starts if c != fire)


def _worker_nc(monkeypatch: pytest.MonkeyPatch, clip: Path, out: Path, *extra: str) -> list[int]:
    """Runs video_worker.main() with stub TPU and yolo_io; returns `nc` of every postprocess."""
    seen: list[int] = []

    def postprocess(y: object, meta: object, conf: float, iou: float, **kw: object) -> list[object]:
        seen.append(int(kw["nc"]))  # type: ignore[call-overload]
        return []

    yolo = types.SimpleNamespace(
        preprocess=lambda img, size: (np.zeros((1, 3, 8, 8), np.float32), None),
        postprocess=postprocess,
    )
    reply = types.SimpleNamespace(ok=True, rtt_s=0.01, outputs={"y": np.zeros(1)}, worker={})

    class Client:
        def __enter__(self) -> "Client":
            return self

        def __exit__(self, *exc: object) -> None:
            return None

        def input_queue_info(self) -> dict[str, int]:
            return {}

        def submit(self, program: str, inputs: object) -> str:
            return "id"

        def collect(self, ids: list[str], timeout: float) -> list[object]:
            return [reply]

    tpu = types.SimpleNamespace(TpuClient=Client, program_uri=lambda p: p)
    monkeypatch.setitem(sys.modules, "yolo_io", yolo)
    monkeypatch.setitem(sys.modules, "linq_tpu", tpu)
    path = Path(__file__).parents[1] / "tools/linq/remote/video_worker.py"
    spec = importlib.util.spec_from_file_location("baseline_video_worker", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    argv = ["video_worker.py", "--video", str(clip), "--program", "p.tpu", "--out", str(out)]
    monkeypatch.setattr(sys, "argv", [*argv, "--step", "10", *extra])
    module.main()
    return seen


def test_worker_nc_argument(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, make_video) -> None:
    clip = make_video(tmp_path, 1, 25)
    out = tmp_path / "out.jsonl"
    assert set(_worker_nc(monkeypatch, clip, out, "--nc", "2")) == {2}
    assert set(_worker_nc(monkeypatch, clip, out)) == {80}
    assert set(_worker_nc(monkeypatch, clip, out, "--task", "pose")) == {1}
    assert len(out.read_text(encoding="utf-8").splitlines()) == 3  # frames 0, 10, 20
