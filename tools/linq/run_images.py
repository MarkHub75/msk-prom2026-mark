"""Images -> LinQ TPU (via tunnel) -> detections, compared with the fp32 CPU reference.

    python tools/linq/run_images.py --program mosprom_x.tpu --onnx models/yolov8n_640_op13.onnx \
        [--tail models/linq/<tag>/<tag>_tail.onnx] IMG [IMG ...] [--repeat 10] [--out results/linq_smoke/x.json]

--onnx is the full fp32 model: it gives the input contract (sidecar .json) and the CPU reference.
--tail, for cut programs: the TPU returns head tensors, the tail ONNX finishes decode on CPU.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yolo_io  # noqa: E402
from linq_tpu import TpuClient  # noqa: E402
from reference_cpu import CpuYolo, load_rgb  # noqa: E402


def tpu_to_output(r_outputs: dict, tail: ort.InferenceSession | None) -> np.ndarray:
    if tail is None:
        return next(iter(r_outputs.values()))
    feeds = {i.name: r_outputs[i.name].astype(np.float32) for i in tail.get_inputs()}
    return tail.run(None, feeds)[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--program", required=True)
    ap.add_argument("--onnx", required=True)
    ap.add_argument("--tail")
    ap.add_argument("--repeat", type=int, default=10)
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--out")
    a = ap.parse_args()

    cpu = CpuYolo(a.onnx)
    kpt = tuple(cpu.meta["kpt_shape"]) if cpu.meta.get("kpt_shape") else None
    tail = ort.InferenceSession(a.tail, providers=["CPUExecutionProvider"]) if a.tail else None
    report = {"program": a.program, "onnx": Path(a.onnx).name, "tail": Path(a.tail).name if a.tail else None,
              "images": {}, "output_contract": None}
    with TpuClient() as c:
        for p in a.images:
            img = load_rgb(p)
            ref, cpu_dt, ref_raw = cpu.detect(img, conf=a.conf)
            x, meta = yolo_io.preprocess(img, cpu.size)
            rtts, full = [], []
            for i in range(a.repeat):
                t0 = time.perf_counter()
                x, meta = yolo_io.preprocess(img, cpu.size)
                r = c.infer(a.program, {cpu.in_name: x}, timeout=120)
                y = tpu_to_output(r.outputs, tail)
                dets = yolo_io.postprocess(y, meta, a.conf, nc=cpu.meta["nc"], kpt_shape=kpt)
                full.append(time.perf_counter() - t0)
                rtts.append(r.rtt_s)
            if report["output_contract"] is None:
                report["output_contract"] = {k: {"shape": list(v.shape), "dtype": str(v.dtype)}
                                             for k, v in r.outputs.items()}
            mt = yolo_io.match_dets(ref, dets)
            raw_diff = float(np.abs(y - ref_raw).max()) if y.shape == ref_raw.shape else None
            report["images"][Path(p).name] = {
                "cpu_fp32": ref, "tpu": dets, "match": mt, "max_abs_raw_diff": raw_diff,
                "ms": {"tpu_rtt_median": round(1000 * float(np.median(rtts)), 1),
                       "full_cycle_median": round(1000 * float(np.median(full)), 1),
                       "cpu_onnx": round(cpu_dt * 1000, 1)}}
            print(f"{Path(p).name}: cpu={len(ref)} tpu={len(dets)} match={mt['matched']} "
                  f"recall={mt['recall_vs_ref']:.2f} iou={mt['mean_iou']} dscore={mt['mean_abs_score_diff']} "
                  f"rtt={np.median(rtts) * 1000:.0f}ms full={np.median(full) * 1000:.0f}ms "
                  f"classes_tpu={sorted({d['name'] for d in dets})}")
    ms = [v["match"] for v in report["images"].values() if v["match"]["n_ref"]]
    report["summary"] = {
        "mean_recall_vs_cpu": float(np.mean([m["recall_vs_ref"] for m in ms])) if ms else None,
        "mean_precision_vs_cpu": float(np.mean([m["precision_vs_ref"] for m in ms])) if ms else None,
        "mean_iou": float(np.mean([m["mean_iou"] for m in ms if m["mean_iou"] is not None])) if ms else None,
        "mean_abs_score_diff": float(np.mean([m["mean_abs_score_diff"] for m in ms
                                              if m["mean_abs_score_diff"] is not None])) if ms else None,
    }
    print(json.dumps(report["summary"]))
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
