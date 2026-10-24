"""LocalBackend (tech.md 8.1): the loop of `video_worker.py` in this process, onnxruntime on CPU.

Blocking: `services` calls `run` through `asyncio.to_thread`; nothing here writes to the
database. Pre- and postprocessing come from `tools/linq/yolo_io.py`, so the JSONL matches the
LinQ worker line for line.
"""

import importlib.util
import json
import math
import time
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import cv2

from safewatch import clock, registry, texts
from safewatch.config import ROOT, Settings
from safewatch.errors import InferenceError
from safewatch.types import BackendName, BackendState, BackendStatus, InferenceMetrics, ModelSpec

PROGRESS_EVERY = 25  # frames between progress calls, as the worker writes `.progress`


def _yolo_io(tools_dir: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("yolo_io", tools_dir / "yolo_io.py")
    if spec is None or spec.loader is None:
        raise InferenceError("internal", "cannot load yolo_io.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalBackend:  # InferenceBackend: onnxruntime on CPU, same JSONL as the worker
    name: BackendName = "local"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def close(self) -> None:
        """Nothing to release: a session lives for one run (tech.md 8.29)."""

    def _session(self, model: ModelSpec) -> Any:
        onnx = ROOT / model.local_onnx if model.local_onnx else None
        if onnx is None or not onnx.is_file():
            raise InferenceError("model_missing", f"{model.id}@{model.version}: no local ONNX")
        import onnxruntime as ort  # heavy: only the local backend needs it

        options = ort.SessionOptions()
        options.log_severity_level = 3
        options.intra_op_num_threads = self.settings.local.threads
        options.inter_op_num_threads = 1
        return ort.InferenceSession(str(onnx), options, providers=["CPUExecutionProvider"])

    def run(
        self,
        video: Path,
        video_sha256: str,
        model: ModelSpec,
        step: int,
        out: Path,
        progress: Callable[[float], None],
    ) -> InferenceMetrics:
        started = time.perf_counter()
        session = self._session(model)
        yolo_io = _yolo_io(self.settings.linq.tools_dir)
        input_name = session.get_inputs()[0].name
        nc, kpt = (1, (17, 3)) if model.task == "pose" else (80, None)
        classes: list[int] | None = list(model.classes)
        if f"{model.id}@{model.version}" in self.settings.pipeline.extra:
            nc, classes = len(model.classes), None  # the worker's --nc: all own classes
        cap = cv2.VideoCapture(str(video))
        if not cap.isOpened():
            raise InferenceError("video_unreadable", video.name)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        n_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        expected = max(1, math.ceil(n_total / step))
        t_pre = t_post = 0.0
        done = 0
        loop_started = time.perf_counter()
        with out.open("w", encoding="utf-8", newline="\n") as f:
            fidx = -1
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                fidx += 1
                if fidx % step:
                    continue
                ts = cap.get(cv2.CAP_PROP_POS_MSEC) or fidx * 1000.0 / fps
                t0 = time.perf_counter()
                x, meta = yolo_io.preprocess(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), model.input_size
                )
                t1 = time.perf_counter()
                y = session.run(None, {input_name: x})[0]
                t2 = time.perf_counter()
                dets = yolo_io.postprocess(
                    y, meta, model.conf, model.iou, nc=nc, kpt_shape=kpt, classes=classes
                )
                t_pre += t1 - t0
                t_post += time.perf_counter() - t2
                row = {"frame_idx": fidx, "ts_ms": round(ts, 1), "detections": dets}
                f.write(json.dumps(row) + "\n")
                done += 1
                if done % PROGRESS_EVERY == 0:
                    progress(min(1.0, done / expected))
        cap.release()
        wall = time.perf_counter() - loop_started
        progress(1.0)
        per_frame = {
            "preprocess": round(1000 * t_pre / max(done, 1), 2),
            "postprocess": round(1000 * t_post / max(done, 1), 2),
        }
        total_s = time.perf_counter() - started
        summary = {
            "video": video.name,
            "onnx": model.local_onnx,
            "size": model.input_size,
            "step": step,
            "fps_video": fps,
            "frames_total": n_total,
            "frames_processed": done,
            "wall_s": round(wall, 2),
            "throughput_fps": round(done / wall, 2) if wall else None,
            "per_frame_ms": per_frame,
            "end_to_end_s": round(total_s, 3),
        }
        summary_path = out.parent / f"{out.stem}.summary.json"
        summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8", newline="\n")
        return InferenceMetrics(
            backend="local",
            fake=False,  # no external service to fake
            model_id=model.id,
            model_version=model.version,
            task=model.task,
            input_size=model.input_size,
            step=step,
            frames_processed=done,
            wall_s=round(wall, 3),
            throughput_fps=round(done / wall, 2) if wall else 0.0,
            preprocess_ms=per_frame["preprocess"],
            postprocess_ms=per_frame["postprocess"],
            tpu_rtt_p50_ms=None,
            tpu_rtt_p90_ms=None,
            upload_s=None,
            total_s=round(total_s, 3),
            cached=False,
        )

    def check(self) -> BackendStatus:
        present: list[str] = []
        missing: list[str] = []
        for model in registry.active_models(self.settings):
            name = model.local_onnx or f"{model.id}@{model.version}"
            ok = model.local_onnx is not None and (ROOT / model.local_onnx).is_file()
            (present if ok else missing).append(name)
        state: BackendState = "models_missing" if missing else "ok"
        if missing:
            message = texts.LOCAL_MODELS_MISSING.format(names=", ".join(missing))
        else:
            message = texts.LOCAL_OK.format(present=len(present), total=len(present))
        return BackendStatus(
            backend="local",
            fake=False,
            state=state,
            checked_at=clock.now(),
            latency_ms=None,
            present=present,
            missing=missing,
            message=message,
        )
