"""Export Ultralytics variants to ONNX via documented Python API YOLO(...).export(format='onnx', ...).
Usage: export_variants.py WEIGHTS_DIR OUT_DIR [only_variant_substring]"""
import sys, shutil, json, time, traceback, logging, io
from pathlib import Path

W, OUT = Path(sys.argv[1]), Path(sys.argv[2])
only = sys.argv[3] if len(sys.argv) > 3 else None
from ultralytics import YOLO

V = [
    # (variant_name, weights, kwargs)
    ("yolo11n_default", "yolo11n.pt", {}),
    ("yolo11n_noslim", "yolo11n.pt", {"simplify": False}),
    ("yolo11n_op11", "yolo11n.pt", {"opset": 11}),
    ("yolo11n_op12", "yolo11n.pt", {"opset": 12}),
    ("yolo11n_op13", "yolo11n.pt", {"opset": 13}),
    ("yolo11n_op17", "yolo11n.pt", {"opset": 17}),
    ("yolo11n_op9", "yolo11n.pt", {"opset": 9}),
    ("yolo11n_dynamic", "yolo11n.pt", {"dynamic": True}),
    ("yolo11n_384x640", "yolo11n.pt", {"imgsz": [384, 640]}),
    ("yolo11n_b4", "yolo11n.pt", {"batch": 4}),
    ("yolo11n_nms", "yolo11n.pt", {"nms": True}),
    ("yolo11n_nms_op11", "yolo11n.pt", {"nms": True, "opset": 11}),
    ("yolo11n_nms_dyn_b4", "yolo11n.pt", {"nms": True, "dynamic": True, "batch": 4}),
    ("yolov8n_default", "yolov8n.pt", {}),
    ("yolov8n_op11", "yolov8n.pt", {"opset": 11}),
    ("yolov8n_nms", "yolov8n.pt", {"nms": True}),
    ("yolov5nu_default", "yolov5nu.pt", {}),
    ("yolov5su_default", "yolov5su.pt", {}),
    ("yolo26n_default", "yolo26n.pt", {}),
    ("yolo26n_e2e", "yolo26n.pt", {"nms": False}),
    ("yolo26n_e2e_op11", "yolo26n.pt", {"nms": False, "opset": 11}),
    ("yolo26n_nms", "yolo26n.pt", {"nms": True}),
    ("yolo26n_384x640", "yolo26n.pt", {"imgsz": [384, 640]}),
]
summary = {}
for name, wt, kw in V:
    if only and only not in name:
        continue
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy(W / wt, d / wt)
    # capture ultralytics logger output
    buf = io.StringIO()
    h = logging.StreamHandler(buf)
    lg = logging.getLogger("ultralytics")
    lg.addHandler(h)
    t = time.time()
    try:
        f = YOLO(str(d / wt)).export(format="onnx", device="cpu", **kw)
        summary[name] = {"ok": True, "file": str(f), "kwargs": kw, "sec": round(time.time() - t, 1)}
    except Exception as e:
        summary[name] = {"ok": False, "error": repr(e)[:800], "kwargs": kw, "trace": traceback.format_exc()[-1500:]}
    lg.removeHandler(h)
    (d / "export.log").write_text(buf.getvalue(), encoding="utf-8")
    (d / wt).unlink()
    print(name, summary[name].get("ok"), summary[name].get("file") or summary[name].get("error"), flush=True)
p = OUT / ("summary.json" if not only else f"summary_{only}.json")
p.write_text(json.dumps(summary, indent=1), encoding="utf-8")
