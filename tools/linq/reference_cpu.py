"""CPU reference: run a YOLO ONNX in onnxruntime with yolo_io pre/post-processing.

    python tools/linq/reference_cpu.py models/yolov8n_640_op13.onnx IMG [IMG ...] [--out results/linq_smoke/cpu_ref.json]
    python tools/linq/reference_cpu.py ... --check-ultralytics models/yolov8n.pt   # sanity of our post-processing
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yolo_io  # noqa: E402


def load_rgb(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


class CpuYolo:
    def __init__(self, onnx_path: str):
        self.meta = json.loads(Path(onnx_path).with_suffix(".json").read_text(encoding="utf-8"))
        self.sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        self.size = self.meta["inputs"][0]["shape"][-1]
        self.in_name = self.meta["inputs"][0]["name"]

    def raw(self, x: np.ndarray) -> np.ndarray:
        return self.sess.run(None, {self.in_name: x})[0]

    def detect(self, img_rgb: np.ndarray, conf=0.25, iou=0.45):
        x, m = yolo_io.preprocess(img_rgb, self.size)
        t0 = time.perf_counter()
        y = self.raw(x)
        dt = time.perf_counter() - t0
        kpt = tuple(self.meta["kpt_shape"]) if self.meta.get("kpt_shape") else None
        return yolo_io.postprocess(y, m, conf, iou, nc=self.meta["nc"], kpt_shape=kpt), dt, y


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("onnx")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--check-ultralytics")
    a = ap.parse_args()
    model = CpuYolo(a.onnx)
    res = {}
    for p in a.images:
        dets, dt, _ = model.detect(load_rgb(p))
        res[Path(p).name] = {"ms": round(dt * 1000, 1), "detections": dets}
        print(f"{Path(p).name}: {len(dets)} dets, {dt * 1000:.0f} ms, "
              f"{sorted({d['name'] for d in dets})}")
    if a.check_ultralytics:
        from ultralytics import YOLO
        u = YOLO(a.check_ultralytics)
        for p in a.images:
            r = u.predict(p, imgsz=model.size, conf=0.25, iou=0.45, verbose=False, rect=False)[0]
            ud = [{"cls": int(c), "score": float(s), "bbox_xyxy": b.tolist()}
                  for c, s, b in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy)]
            mt = yolo_io.match_dets(ud, res[Path(p).name]["detections"])
            print(f"  vs ultralytics {Path(p).name}: {mt}")
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
