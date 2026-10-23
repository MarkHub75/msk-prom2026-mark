"""Runs INSIDE LinQ Jupyter: latency/throughput of a program, plus host diagnostics.

    python bench_tpu.py PROGRAM [--input images] [--shape 1,3,640,640] [--n 20] [--inflight 1,4,8]
"""
import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linq_tpu import TpuClient  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("program")
ap.add_argument("--input", default="images")
ap.add_argument("--shape", default="1,3,640,640")
ap.add_argument("--n", type=int, default=20)
ap.add_argument("--inflight", default="1,4,8")
a = ap.parse_args()

for p in ("/sys/fs/cgroup/cpu.max", "/sys/fs/cgroup/cpu/cpu.cfs_quota_us"):
    if os.path.exists(p):
        print("cgroup", p, open(p).read().strip())
print("sched_getaffinity cpus:", len(os.sched_getaffinity(0)), "| OMP/OPENBLAS threads env:",
      os.environ.get("OMP_NUM_THREADS"), os.environ.get("OPENBLAS_NUM_THREADS"))
x = np.random.rand(*[int(s) for s in a.shape.split(",")]).astype(np.float32)
print(f"input {x.shape} {x.nbytes / 1e6:.1f} MB")
import cv2  # noqa: E402
img = (np.random.rand(720, 1280, 3) * 255).astype(np.uint8)
for nt in (cv2.getNumThreads(), 1):
    cv2.setNumThreads(nt)
    t = time.perf_counter()
    for _ in range(20):
        cv2.resize(img, (640, 360))
    print(f"cv2.resize threads={nt}: {(time.perf_counter() - t) / 20 * 1000:.1f} ms")

with TpuClient() as c:
    print("input queue:", c.input_queue_info())
    for k in [int(v) for v in a.inflight.split(",")]:
        lat = []
        t0 = time.monotonic()
        done = 0
        while done < a.n:
            ids = [c.submit(a.program, {a.input: x}) for _ in range(min(k, a.n - done))]
            res = c.collect(ids, timeout=300)
            lat += [r.rtt_s for r in res]
            done += len(res)
            assert all(r.ok for r in res), res[0].worker
        wall = time.monotonic() - t0
        print(f"inflight={k}: n={a.n} rtt median={np.median(lat) * 1000:.0f} ms p90={np.percentile(lat, 90) * 1000:.0f} ms "
              f"throughput={a.n / wall:.2f} req/s pids={sorted({r.worker['worker_pid'] for r in res})}")
    print("input queue after:", c.input_queue_info())
