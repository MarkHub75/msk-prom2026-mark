"""W2-D kit: shared helpers (paths, hashing, letterbox preprocessing, ONNX inventory).
Environment: venv-W1-10 (ultralytics==8.4.184, torch 2.14.1+cpu, onnx 1.23.2, onnxruntime 1.31.0, numpy 2.5.2).
All large artifacts live in KIT_HOME (default <SCRATCH>/kit-W2-D, override with env KIT_HOME).
"""
import hashlib, json, os
from collections import Counter
from pathlib import Path

import numpy as np

KIT_HOME = Path(os.environ.get(
    "KIT_HOME",
    r"C:\Users\User\AppData\Local\Temp\claude\C--Users-User-Documents-mosprom2026-hack-research-model-stack-claude"
    r"\adce1a1a-fbbd-4ab7-b3bb-2b61dbc9d01b\scratchpad\kit-W2-D"))
WEIGHTS = KIT_HOME / "weights"
GRAPHS = KIT_HOME / "graphs"
REFS = KIT_HOME / "refs"
CALIB = KIT_HOME / "calib"
LOGS = KIT_HOME / "logs"

STRIDES = (8, 16, 32)


def sha256_file(p, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_array(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(str(a.dtype).encode()); h.update(str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def letterbox_u8(img_bgr, new_hw=(640, 640), color=114, interp=None):
    """Ultralytics LetterBox(auto=False, scaleup=True, center=True) re-implemented (W1-11 sec. 6.1).
    Returns (canvas_bgr_u8 [H,W,3], meta dict). Banker's round() as in Ultralytics."""
    import cv2
    interp = cv2.INTER_LINEAR if interp is None else interp
    h, w = img_bgr.shape[:2]
    Hn, Wn = new_hw
    r = min(Hn / h, Wn / w)
    nw, nh = max(round(w * r), 1), max(round(h * r), 1)
    dw, dh = Wn - nw, Hn - nh
    top, bottom = round(dh / 2 - 0.1), round(dh / 2 + 0.1)
    left, right = round(dw / 2 - 0.1), round(dw / 2 + 0.1)
    im = img_bgr
    if (w, h) != (nw, nh):
        im = cv2.resize(im, (nw, nh), interpolation=interp)
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(color,) * 3)
    gain_x, gain_y = nw / w, nh / h
    meta = dict(h=h, w=w, new_w=nw, new_h=nh, gain=r, gain_x=gain_x, gain_y=gain_y,
                pad_left=left, pad_top=top, pad_right=right, pad_bottom=bottom, imgsz=[Hn, Wn],
                color=color, interp="INTER_LINEAR", preproc_version="W2-D/letterbox_u8 v1")
    return im, meta


def to_tensors(canvas_bgr_u8):
    """canvas BGR u8 [H,W,3] -> (u8 RGB HWC, f32 NCHW 0..1, f32 NHWC 0..1)."""
    rgb = np.ascontiguousarray(canvas_bgr_u8[..., ::-1])
    nhwc = rgb.astype(np.float32) / np.float32(255.0)
    nchw = np.ascontiguousarray(nhwc.transpose(2, 0, 1))
    return rgb, nchw, np.ascontiguousarray(nhwc)


def onnx_inventory(path):
    import onnx
    m = onnx.load(str(path))
    g = m.graph
    inits = {i.name for i in g.initializer}

    def shp(vi):
        t = vi.type.tensor_type
        return {"name": vi.name, "dtype": onnx.TensorProto.DataType.Name(t.elem_type),
                "shape": [d.dim_param if d.dim_param else d.dim_value for d in t.shape.dim]}
    try:
        onnx.checker.check_model(m, full_check=True); chk = "ok"
    except Exception as ex:  # noqa
        chk = ("FAIL: " + str(ex))[:300]
    return {"file": Path(path).name, "bytes": os.path.getsize(path), "sha256": sha256_file(path),
            "ir_version": m.ir_version, "opset": {(o.domain or "ai.onnx"): o.version for o in m.opset_import},
            "inputs": [shp(i) for i in g.input if i.name not in inits], "outputs": [shp(o) for o in g.output],
            "n_nodes": len(g.node), "ops": dict(sorted(Counter(n.op_type for n in g.node).items(), key=lambda x: (-x[1], x[0]))),
            "checker": chk}


def write_json(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
