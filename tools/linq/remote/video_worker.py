"""Runs INSIDE LinQ Jupyter: video file -> frames -> YOLO on LinQ TPU -> JSON Lines.

    python video_worker.py --video v.mp4 --program yolov8n_640.tpu --out v.jsonl [--step 5]
           [--size 640] [--conf 0.25] [--inflight 8] [--task detect|pose] [--classes 0,2,5,7,67]
           [--nc 2]

Each output line: {"frame_idx", "ts_ms", "detections": [{"cls","name","score","bbox_xyxy"[, "kpts"]}]}.
A summary with timings goes to <out>.summary.json; progress to <out>.progress (polled by run_video.py).
Needs linq_tpu.py and yolo_io.py next to it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import deque

# The LinQ Jupyter container shows 64 CPUs but its cgroup quota is 1.5 CPU: default thread
# pools (OpenMP/BLAS/onnxruntime/OpenCV) oversubscribe it and everything crawls.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import cv2  # noqa: E402
import numpy as np  # noqa: E402

cv2.setNumThreads(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yolo_io  # noqa: E402
from linq_tpu import TpuClient, program_uri  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--program", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=640)
    ap.add_argument("--step", type=int, default=1, help="process every N-th frame")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.45)
    ap.add_argument("--inflight", type=int, default=8, help="TPU requests in flight")
    ap.add_argument("--task", choices=["detect", "pose"], default="detect")
    ap.add_argument("--classes", default="", help="comma list of COCO ids to keep (detect)")
    ap.add_argument("--nc", type=int, default=0, help="class count of the model (default: 80 detect, 1 pose)")
    ap.add_argument("--input-name", default="images")
    ap.add_argument("--output-name", default="", help="TPU output tensor name (default: the only one)")
    ap.add_argument("--tail", default="", help="tail ONNX for cut programs (decode on CPU, onnxruntime)")
    a = ap.parse_args()
    tail = None
    if a.tail:
        import onnxruntime as ort
        so = ort.SessionOptions()
        so.log_severity_level = 3
        so.intra_op_num_threads = 1
        so.inter_op_num_threads = 1
        tail = ort.InferenceSession(a.tail, so, providers=["CPUExecutionProvider"])

    nc, kpt = (1, (17, 3)) if a.task == "pose" else (80, None)
    nc = a.nc or nc
    classes = [int(c) for c in a.classes.split(",") if c] or None
    cap = cv2.VideoCapture(a.video)
    if not cap.isOpened():
        raise SystemExit(f"cannot open {a.video}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    n_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prog_path = a.out + ".progress"
    t_start = time.monotonic()
    t_pre = t_post = 0.0
    rtts: list[float] = []
    n_done = 0
    pending: deque = deque()

    def drain(client: TpuClient, out_f, block_until: int) -> None:
        nonlocal t_post, n_done
        while len(pending) > block_until:
            mid, fidx, ts, meta = pending.popleft()
            r = client.collect([mid], timeout=120)[0]
            if not r.ok:
                raise RuntimeError(f"TPU error frame {fidx}: {r.worker.get('error_message')}")
            rtts.append(r.rtt_s)
            t0 = time.perf_counter()
            if tail is not None:
                y = tail.run(None, {i.name: r.outputs[i.name] for i in tail.get_inputs()})[0]
            else:
                y = r.outputs[a.output_name] if a.output_name else next(iter(r.outputs.values()))
            dets = yolo_io.postprocess(y, meta, a.conf, a.iou, nc=nc, kpt_shape=kpt, classes=classes)
            t_post += time.perf_counter() - t0
            out_f.write(json.dumps({"frame_idx": fidx, "ts_ms": round(ts, 1), "detections": dets}) + "\n")
            n_done += 1
            if n_done % 25 == 0:
                with open(prog_path, "w") as pf:
                    json.dump({"done": n_done, "frame_idx": fidx, "n_total": n_total,
                               "elapsed_s": round(time.monotonic() - t_start, 1)}, pf)

    with TpuClient() as client, open(a.out, "w") as out_f:
        # R5: queue state and target URI go to the log tail that LinqBackend reads on failure
        print(json.dumps({"input_queue": client.input_queue_info(),
                          "uri": program_uri(a.program)}), file=sys.stderr, flush=True)
        fidx = -1
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            fidx += 1
            if fidx % a.step:
                continue
            ts = cap.get(cv2.CAP_PROP_POS_MSEC) or fidx * 1000.0 / fps
            t0 = time.perf_counter()
            x, meta = yolo_io.preprocess(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), a.size)
            t_pre += time.perf_counter() - t0
            pending.append((client.submit(a.program, {a.input_name: x}), fidx, ts, meta))
            drain(client, out_f, a.inflight - 1)
        drain(client, out_f, 0)

    wall = time.monotonic() - t_start
    summary = {
        "video": os.path.basename(a.video), "program": a.program, "size": a.size, "step": a.step,
        "fps_video": fps, "frames_total": n_total, "frames_processed": n_done, "wall_s": round(wall, 2),
        "throughput_fps": round(n_done / wall, 2) if wall else None,
        "per_frame_ms": {"preprocess": round(1000 * t_pre / max(n_done, 1), 2),
                         "postprocess": round(1000 * t_post / max(n_done, 1), 2),
                         "tpu_rtt_median": round(1000 * float(np.median(rtts)), 2) if rtts else None,
                         "tpu_rtt_p90": round(1000 * float(np.percentile(rtts, 90)), 2) if rtts else None},
        "inflight": a.inflight,
    }
    with open(a.out + ".summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    with open(prog_path, "w") as pf:
        json.dump({"done": n_done, "finished": True}, pf)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
