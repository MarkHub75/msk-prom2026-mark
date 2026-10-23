"""Vendor resnet50 example, run unchanged in spirit, inside LinQ Jupyter (~/work/mosprom_work).

Expects linq_tpu.py next to it (uploaded by tools/linq/jupyter_remote.py).
"""
import os
import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.expanduser("~/work/mosprom_work"))
from linq_tpu import TpuClient  # noqa: E402

PROGRAM = "torch_resnet50_b1_o5_h1m.tpu"
IMG = os.path.expanduser("~/work/examples/ILSVRC2012_val_00000045.JPEG")
EXPECTED_CLASS = 257


def central_crop(image, percent=1.0):
    w, h = image.size
    d = int(min(h, w) * percent)
    t, l = (h - d) // 2, (w - d) // 2
    return image.crop((l, t, l + d, t + d))


def preprocess(image):
    image = central_crop(image.convert("RGB"), 0.85).resize(size=(224, 224))
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (np.asarray(image) / 255.0 - mean) / std
    return np.array([np.transpose(arr, (2, 0, 1))]).astype(np.float32)


x = preprocess(Image.open(IMG))
rtts, infs, pids = [], [], set()
with TpuClient() as c:
    print("broker", c.conn._impl.params.host, "input queue", c.input_queue_info())
    for i in range(20):
        r = c.infer(PROGRAM, {"input.1": x})
        cls = int(np.argmax(r.outputs["495"])) + 1
        assert cls == EXPECTED_CLASS, cls
        rtts.append(r.rtt_s * 1000)
        infs.append(r.worker["inference_time"] * 1000)
        pids.add(r.worker["worker_pid"])
    # pipelined: 32 tasks in flight
    t0 = time.monotonic()
    ids = [c.submit(PROGRAM, {"input.1": x}) for _ in range(32)]
    res = c.collect(ids, timeout=120)
    wall = time.monotonic() - t0
    assert all(int(np.argmax(r.outputs["495"])) + 1 == EXPECTED_CLASS for r in res)

print(f"class={cls} OK; sequential n=20: rtt median={np.median(rtts):.1f} ms "
      f"p90={np.percentile(rtts, 90):.1f} ms; worker inference_time median={np.median(infs):.1f} ms; pids={sorted(pids)}")
print(f"pipelined 32 in flight: wall={wall * 1000:.0f} ms -> {32 / wall:.1f} req/s; "
      f"pids={sorted({r.worker['worker_pid'] for r in res})}")
