"""W1-12 experiment D: cut yolo11n ONNX at raw head convs (box 64ch + cls 80ch per scale), quantize ALL ops with ORT,
decode DFL/boxes/sigmoid on CPU in numpy, compare with fp32 output0. Third-party runtime (ORT CPU), NOT LinQ.
Usage: python exp_rawhead.py <workdir>"""
import sys, json, collections
from pathlib import Path
import numpy as np, onnx, onnxruntime as ort, cv2
from onnx import numpy_helper
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantFormat, QuantType, CalibrationMethod
from ultralytics.utils import ASSETS

work = Path(sys.argv[1]); src = work / "yolo11n.onnx"
m = onnx.load(str(src)); g = m.graph
init = {i.name: numpy_helper.to_array(i) for i in g.initializer}
prod = {o: n for n in g.node for o in n.output}
pairs = []
for k in range(3):
    pairs.append((f"/model.23/cv2.{k}/cv2.{k}.2/Conv_output_0", f"/model.23/cv3.{k}/cv3.{k}.2/Conv_output_0"))
outs = [t for p in pairs for t in p]
cut = work / "yolo11n_rawhead.onnx"
onnx.utils.extract_model(str(src), str(cut), ["images"], outs)
cm = onnx.load(str(cut))
log = {"rawhead_outputs": [(o.name, [d.dim_value for d in o.type.tensor_type.shape.dim]) for o in cm.graph.output],
       "rawhead_op_hist": dict(collections.Counter(n.op_type for n in cm.graph.node))}

def letterbox(img, s=640):
    h, w = img.shape[:2]; r = min(s / h, s / w); nh, nw = int(round(h * r)), int(round(w * r))
    out = np.full((s, s, 3), 114, np.uint8); top, left = (s - nh) // 2, (s - nw) // 2
    out[top:top + nh, left:left + nw] = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR); return out
imgs = sorted([p for p in Path(ASSETS).iterdir() if p.suffix.lower() in {".jpg", ".png"}])
X = [(letterbox(cv2.imread(str(p)))[:, :, ::-1].transpose(2, 0, 1).astype(np.float32) / 255.0)[None] for p in imgs]
class R(CalibrationDataReader):
    def __init__(self): self.it = iter([{"images": x} for x in X])
    def get_next(self): return next(self.it, None)

qpath = work / "yolo11n_rawhead_int8_all.onnx"
quantize_static(str(cut), str(qpath), R(), quant_format=QuantFormat.QDQ, activation_type=QuantType.QInt8,
                weight_type=QuantType.QInt8, calibrate_method=CalibrationMethod.MinMax, per_channel=True)
qh = collections.Counter(n.op_type for n in onnx.load(str(qpath)).graph.node)
log["rawhead_int8"] = {"QuantizeLinear": qh["QuantizeLinear"], "DequantizeLinear": qh["DequantizeLinear"],
                       "non_qdq_ops_left": {k: v for k, v in qh.items() if k not in ("QuantizeLinear", "DequantizeLinear")}}

def decode(raw):  # raw: list of 6 arrays [box(1,64,h,w), cls(1,80,h,w)] x3, strides 8/16/32
    boxes, scores = [], []
    for k, s in enumerate((8, 16, 32)):
        b, c = raw[2 * k][0], raw[2 * k + 1][0]
        h, w = b.shape[1:]
        d = b.reshape(4, 16, h * w); d = np.exp(d - d.max(1, keepdims=True)); d /= d.sum(1, keepdims=True)
        dist = (d * np.arange(16)[None, :, None]).sum(1)  # (4, hw) ltrb
        gy, gx = np.mgrid[0:h, 0:w]; ax = gx.reshape(-1) + 0.5; ay = gy.reshape(-1) + 0.5
        x1, y1, x2, y2 = ax - dist[0], ay - dist[1], ax + dist[2], ay + dist[3]
        boxes.append(np.stack([(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1]) * s)
        scores.append(1 / (1 + np.exp(-c.reshape(80, -1))))
    return np.concatenate(boxes, 1), np.concatenate(scores, 1)

sf = ort.InferenceSession(str(src), providers=["CPUExecutionProvider"])
sr = ort.InferenceSession(str(cut), providers=["CPUExecutionProvider"])
sq = ort.InferenceSession(str(qpath), providers=["CPUExecutionProvider"])
log["per_image"] = []
for p, x in zip(imgs, X):
    y = sf.run(None, {"images": x})[0][0]
    bf, cf = decode(sr.run(None, {"images": x}))
    bq, cq = decode(sq.run(None, {"images": x}))
    sel = y[4:].max(0) > 0.25
    log["per_image"].append({
        "img": p.name,
        "fp32_rawhead_decode_vs_output0_maxabs_box": float(np.abs(bf - y[:4]).max()),
        "fp32_rawhead_decode_vs_output0_maxabs_cls": float(np.abs(cf - y[4:]).max()),
        "fp32_cand_conf>0.25": int(sel.sum()), "int8_cand_conf>0.25": int((cq.max(0) > 0.25).sum()),
        "int8_box_maxabs_err_px_on_fp32_candidates": float(np.abs(bq[:, sel] - y[:4, sel]).max()),
        "int8_box_meanabs_err_px_on_fp32_candidates": float(np.abs(bq[:, sel] - y[:4, sel]).mean()),
        "int8_cls_maxabs_err_on_fp32_candidates": float(np.abs(cq[:, sel] - y[4:, sel]).max()),
        "int8_cls_max": float(cq.max()), "fp32_cls_max": float(y[4:].max())})
(work / "exp_rawhead_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
print(json.dumps(log, indent=2))
