"""Local orchestrator: video -> LinQ Jupyter -> TPU -> JSON Lines back here.

    python tools/linq/run_video.py data/videos/clip.mp4 --program yolov8n_640.tpu [--step 5]
           [--size 640] [--task detect|pose] [--out results/linq_smoke/raw/clip.jsonl]

Steps (no streaming — the case forbids it): upload the file with the Contents API, start
remote/video_worker.py detached (setsid nohup), poll its .progress file, download the
JSONL and summary. Remote workspace: ~/work/mosprom_work/.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from jupyter_remote import JupyterRemote  # noqa: E402

REMOTE_DIR = "mosprom_work"            # relative to the Jupyter root (~/work)
REMOTE_ABS = "~/work/mosprom_work"
WORKER_FILES = [HERE / "linq_tpu.py", HERE / "yolo_io.py", HERE / "remote" / "video_worker.py"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--program", required=True)
    ap.add_argument("--size", type=int, default=640)
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--task", choices=["detect", "pose"], default="detect")
    ap.add_argument("--classes", default="0,2,5,7,67")
    ap.add_argument("--inflight", type=int, default=8)
    ap.add_argument("--out")
    ap.add_argument("--timeout", type=float, default=3600)
    a = ap.parse_args()

    video = Path(a.video)
    tag = f"{video.stem}_{Path(a.program).stem}_s{a.step}"
    out = Path(a.out) if a.out else HERE.parents[1] / "results" / "linq_smoke" / "raw" / f"{tag}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    t0 = time.monotonic()
    jr = JupyterRemote.from_env()
    for f in WORKER_FILES:
        jr.upload(f, f"{REMOTE_DIR}/{f.name}", progress=False)
    jr.upload(video, f"{REMOTE_DIR}/videos/{video.name}")
    t_upload = time.monotonic() - t0

    remote_out = f"{REMOTE_ABS}/out/{tag}.jsonl"
    args = ["python", "video_worker.py", "--video", f"videos/{video.name}", "--program", a.program,
            "--out", remote_out, "--size", str(a.size), "--step", str(a.step), "--task", a.task,
            "--inflight", str(a.inflight)]
    if a.task == "detect" and a.classes:
        args += ["--classes", a.classes]
    cmd = (f"mkdir -p {REMOTE_ABS}/out && cd {REMOTE_ABS} && rm -f {remote_out}.progress && "
           f"setsid nohup {' '.join(shlex.quote(x) for x in args)} > {remote_out}.log 2>&1 < /dev/null & echo started")
    rc, so, se = jr.exec(cmd, timeout=60)
    if rc != 0:
        raise SystemExit(f"start failed: {se}")
    t1 = time.monotonic()
    rel = f"{REMOTE_DIR}/out/{tag}.jsonl"
    while True:
        time.sleep(3)
        rc, so, _ = jr.exec(f"cat {remote_out}.progress 2>/dev/null; echo; "
                            f"pgrep -f {shlex.quote(remote_out)} >/dev/null && echo RUNNING || echo STOPPED", timeout=30)
        lines = [l for l in so.splitlines() if l.strip()]
        state = lines[-1] if lines else "?"
        prog = lines[0] if len(lines) > 1 else "{}"
        print(f"[{time.monotonic() - t1:6.1f}s] {state} {prog}", file=sys.stderr)
        if '"finished": true' in prog:
            break
        if state == "STOPPED":
            _, log, _ = jr.exec(f"tail -30 {remote_out}.log", timeout=30)
            raise SystemExit(f"remote worker stopped without finishing:\n{log}")
        if time.monotonic() - t1 > a.timeout:
            raise SystemExit("timeout")
    t_remote = time.monotonic() - t1
    jr.download(rel, out)
    jr.download(rel + ".summary.json", out.with_suffix(".summary.json"))
    jr.shutdown_kernel()
    summary = json.loads(out.with_suffix(".summary.json").read_text())
    summary["end_to_end_s"] = {"upload": round(t_upload, 1), "remote_run_incl_poll": round(t_remote, 1),
                               "total": round(time.monotonic() - t0, 1)}
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
