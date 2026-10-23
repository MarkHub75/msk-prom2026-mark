"""Cut YOLOv5 v7.0 ONNX at Detect Conv outputs (onnx.utils.extract_model), run ORT, CPU-decode, compare with full graph.
Usage: v5_cut.py FULL.onnx CUT.onnx IMG OUT_JSON"""
import sys, json, onnx, numpy as np, onnxruntime as ort, cv2
from onnx.utils import extract_model
full, cut, imgp, outj = sys.argv[1:5]
outs = ["/model.24/m.0/Conv_output_0", "/model.24/m.1/Conv_output_0", "/model.24/m.2/Conv_output_0"]
extract_model(full, cut, ["images"], outs)
img = cv2.imread(imgp); h, w = img.shape[:2]; r = 640 / max(h, w)
im = cv2.resize(img, (round(w * r), round(h * r))); canvas = np.full((640, 640, 3), 114, np.uint8)
top = (640 - im.shape[0]) // 2; left = (640 - im.shape[1]) // 2; canvas[top:top + im.shape[0], left:left + im.shape[1]] = im
x = np.ascontiguousarray(canvas[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255)
ref = ort.InferenceSession(full, providers=["CPUExecutionProvider"]).run(None, {"images": x})[0]
ys = ort.InferenceSession(cut, providers=["CPUExecutionProvider"]).run(None, {"images": x})
anchors = np.array([[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]], np.float32).reshape(3, 3, 2)
dec = []
for i, (y, s) in enumerate(zip(ys, (8, 16, 32))):
    b, _, ny, nx = y.shape
    y = 1 / (1 + np.exp(-y.reshape(b, 3, 85, ny, nx).transpose(0, 1, 3, 4, 2)))
    gy, gx = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij"); grid = np.stack([gx, gy], -1)[None, None] - 0.5
    xy = (y[..., :2] * 2 + grid) * s; wh = (y[..., 2:4] * 2) ** 2 * anchors[i][None, :, None, None, :]
    dec.append(np.concatenate([xy, wh, y[..., 4:]], -1).reshape(b, -1, 85))
dec = np.concatenate(dec, 1)
m = onnx.load(cut)
from collections import Counter
r = {"cut_outputs": {o: list(v.shape) for o, v in zip(outs, ys)}, "raw_range": [float(min(v.min() for v in ys)), float(max(v.max() for v in ys))],
     "cut_ops": dict(Counter(n.op_type for n in m.graph.node)),
     "maxabs_decode_vs_full_xywh": float(np.abs(dec[..., :4] - ref[..., :4]).max()), "maxabs_decode_vs_full_objcls": float(np.abs(dec[..., 4:] - ref[..., 4:]).max()),
     "full_xywh_range": [float(ref[..., :4].min()), float(ref[..., :4].max())]}
json.dump(r, open(outj, "w"), indent=1); print(json.dumps(r))
