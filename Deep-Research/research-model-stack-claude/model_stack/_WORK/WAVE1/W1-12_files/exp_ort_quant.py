"""W1-12 local experiment: ORT static quantization of yolo11n ONNX (third-party runtime, NOT LinQ).
Usage: python exp_ort_quant.py <workdir>
"""
import sys, os, json, hashlib, collections
from pathlib import Path
import numpy as np

work = Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
os.chdir(work)
os.environ.setdefault("YOLO_OFFLINE", "0")
import ultralytics, onnx, onnxruntime as ort, cv2, torch
from ultralytics import YOLO
from ultralytics.utils import ASSETS
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantFormat, QuantType, CalibrationMethod

log = {"versions": {"ultralytics": ultralytics.__version__, "onnx": onnx.__version__, "onnxruntime": ort.__version__,
                    "torch": torch.__version__, "numpy": np.__version__}}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

m = YOLO("yolo11n.pt")
log["pt_sha256"] = sha("yolo11n.pt"); log["pt_size"] = Path("yolo11n.pt").stat().st_size
f = m.export(format="onnx", imgsz=640, opset=13, batch=1, dynamic=False, simplify=True)
f = Path(f); log["onnx"] = {"path": str(f), "sha256": sha(f), "size": f.stat().st_size}
mo = onnx.load(str(f))
log["onnx"]["inputs"] = [(i.name, [d.dim_value for d in i.type.tensor_type.shape.dim]) for i in mo.graph.input]
log["onnx"]["outputs"] = [(o.name, [d.dim_value for d in o.type.tensor_type.shape.dim]) for o in mo.graph.output]
log["onnx"]["opset"] = [(o.domain, o.version) for o in mo.opset_import]
log["onnx"]["op_hist"] = dict(collections.Counter(n.op_type for n in mo.graph.node))

def letterbox(img, s=640):
    h, w = img.shape[:2]; r = min(s / h, s / w)
    nh, nw = int(round(h * r)), int(round(w * r))
    im = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    out = np.full((s, s, 3), 114, np.uint8)
    top, left = (s - nh) // 2, (s - nw) // 2
    out[top:top + nh, left:left + nw] = im
    return out

imgs = sorted([p for p in Path(ASSETS).iterdir() if p.suffix.lower() in {".jpg", ".png"}])
log["images"] = [p.name for p in imgs]
def prep(p):
    im = letterbox(cv2.imread(str(p)))[:, :, ::-1].transpose(2, 0, 1)
    return (im.astype(np.float32) / 255.0)[None]
X = [prep(p) for p in imgs]

class R(CalibrationDataReader):
    def __init__(self): self.it = iter([{"images": x} for x in X])
    def get_next(self): return next(self.it, None)

sess_fp = ort.InferenceSession(str(f), providers=["CPUExecutionProvider"])
Y = [sess_fp.run(None, {"images": x})[0] for x in X]  # (1, 84, 8400)
box = np.concatenate([y[0, :4] for y in Y], 1); cls = np.concatenate([y[0, 4:] for y in Y], 1)
log["fp32_output_ranges"] = {"box_min": float(box.min()), "box_max": float(box.max()),
                              "cls_min": float(cls.min()), "cls_max": float(cls.max())}
s_shared = float(max(abs(box.min()), abs(box.max()), cls.max())) / 127.0
log["single_symmetric_int8_scale_for_output0"] = s_shared
log["cls_scores_above_0.25_fp32"] = int((cls > 0.25).sum())
log["cls_scores_representable_levels_with_shared_scale"] = int(1.0 / s_shared)

def nms_count(y, conf=0.25):
    c = y[0, 4:].max(0); return int((c > conf).sum())

variants = {
    "A_all_ops_per_tensor_minmax": dict(per_channel=False),
    "B_all_ops_per_channel_minmax": dict(per_channel=True),
    "C_ultralytics_style_conv_only": dict(per_channel=False, nodes_to_exclude=[n.name for n in mo.graph.node if n.op_type not in {"Conv", "Gemm", "MatMul"}]),
}
log["variants"] = {}
for name, kw in variants.items():
    out = work / f"yolo11n_{name}.onnx"
    try:
        quantize_static(str(f), str(out), R(), quant_format=QuantFormat.QDQ, activation_type=QuantType.QInt8,
                        weight_type=QuantType.QInt8, calibrate_method=CalibrationMethod.MinMax, **kw)
        q = onnx.load(str(out))
        hist = collections.Counter(n.op_type for n in q.graph.node)
        s = ort.InferenceSession(str(out), providers=["CPUExecutionProvider"])
        Yq = [s.run(None, {"images": x})[0] for x in X]
        res = {"QuantizeLinear": hist.get("QuantizeLinear", 0), "DequantizeLinear": hist.get("DequantizeLinear", 0),
               "size": out.stat().st_size, "per_image": []}
        for p, y, yq in zip(imgs, Y, Yq):
            res["per_image"].append({
                "img": p.name,
                "fp32_cand_conf>0.25": nms_count(y), "q_cand_conf>0.25": nms_count(yq),
                "box_maxabs_err_px": float(np.abs(y[0, :4] - yq[0, :4]).max()),
                "cls_maxabs_err": float(np.abs(y[0, 4:] - yq[0, 4:]).max()),
                "cls_max_fp32": float(y[0, 4:].max()), "cls_max_q": float(yq[0, 4:].max()),
                "distinct_cls_values_q": int(np.unique(yq[0, 4:]).size)})
        # output0 scale in QDQ graph (last DequantizeLinear feeding the graph output, if any)
        outname = q.graph.output[0].name
        prod = {o: n for n in q.graph.node for o in n.output}
        n = prod.get(outname); res["output_producer"] = n.op_type if n else None
        if n is not None and n.op_type == "DequantizeLinear":
            init = {i.name: onnx.numpy_helper.to_array(i) for i in q.graph.initializer}
            res["output_dq_scale"] = float(init[n.input[1]]) if n.input[1] in init else None
        log["variants"][name] = res
    except Exception as e:
        log["variants"][name] = {"error": f"{type(e).__name__}: {e}"}

Path(work / "exp_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
print(json.dumps(log, indent=2))
