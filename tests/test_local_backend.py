"""Slice 3: LocalBackend writes the JSONL of `video_worker.py` with onnxruntime on CPU."""

import math
from pathlib import Path

import pytest

from safewatch import registry
from safewatch.config import ROOT, Settings
from safewatch.errors import InferenceError
from safewatch.inference.artifacts import read_jsonl
from safewatch.inference.local import LocalBackend

MODELS = registry.load_models(registry.MODELS_FILE)
HAVE_ONNX = all(m.local_onnx and (ROOT / m.local_onnx).is_file() for m in MODELS)


@pytest.mark.skipif(not HAVE_ONNX, reason="models/*.onnx are not in the repo (CI)")
def test_local_matches_jsonl_format(core: Settings, tmp_path: Path, make_video) -> None:
    video = make_video(tmp_path, 1, 25)  # 25 frames
    backend = LocalBackend(core)
    shares: list[float] = []
    for model in registry.active_models(core):
        out = tmp_path / f"{model.task}.jsonl"
        metrics = backend.run(video, "0" * 64, model, 2, out, shares.append)
        frames = read_jsonl(out, expected_frames=math.ceil(25 / 2))
        assert len(frames) == metrics.frames_processed == 13
        assert all(d.cls in model.classes for f in frames for d in f.detections)
        assert (metrics.backend, metrics.fake, metrics.task) == ("local", False, model.task)
        assert metrics.tpu_rtt_p50_ms is None and metrics.upload_s is None
        assert (
            metrics.preprocess_ms is not None
            and (out.parent / f"{out.stem}.summary.json").is_file()
        )
    assert shares[-1] == 1.0


def test_local_without_onnx_is_model_missing(core: Settings, tmp_path: Path, make_video) -> None:
    model = registry.resolve(core.pipeline.detector)
    gone = model.model_copy(update={"local_onnx": "models/missing.onnx"})
    video = make_video(tmp_path, 1, 25)
    with pytest.raises(InferenceError) as exc:
        LocalBackend(core).run(video, "0" * 64, gone, 2, tmp_path / "x.jsonl", lambda s: None)
    assert exc.value.code == "model_missing"
