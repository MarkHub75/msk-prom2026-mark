"""Step 1: official Ultralytics 8.4.184 exports ('full' and 'e2e' heads) for all kit models and opsets.
Usage: py -I export_full.py [model_substring] [opset]
Writes graphs/<M>/<M>.<head>.op<N>.onnx + logs/export_<M>.<head>.op<N>.log + graphs/export_summary.json
Requires: KIT_HOME/weights/*.pt (sha256 in manifest), PYTHONUTF8=1 on Windows (W1-09-F13)."""
import io, json, logging, shutil, sys, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kitlib import GRAPHS, LOGS, WEIGHTS, KIT_HOME, sha256_file

only = sys.argv[1] if len(sys.argv) > 1 else None
only_op = int(sys.argv[2]) if len(sys.argv) > 2 else None

from ultralytics import YOLO
import ultralytics

# (M, weights, head, export kwargs)  -- nms omitted == Ultralytics default (None)
SPECS = [
    ("v8n", "yolov8n.pt", "full", {}),
    ("v11n", "yolo11n.pt", "full", {}),
    ("v26n", "yolo26n.pt", "full", {}),                 # nms=None -> one2many [1,84,8400]
    ("v26n", "yolo26n.pt", "e2e", {"nms": False}),      # end2end one2one [1,300,6]
    ("v8n-pose", "yolov8n-pose.pt", "full", {}),
    ("v8n-pose", "yolov8n-pose.pt", "nmsFalse", {"nms": False}),   # K005: compare with default
    ("v11n-pose", "yolo11n-pose.pt", "full", {}),
    ("v11n-pose", "yolo11n-pose.pt", "nmsFalse", {"nms": False}),
    ("v26n-pose", "yolo26n-pose.pt", "full", {}),
    ("v26n-pose", "yolo26n-pose.pt", "e2e", {"nms": False}),
]
OPSETS = [11, 13, 18]
EXTRA_OPSET17 = {"v8n"}   # point check of opset 17 (W1-10 6.5: opset influence is small)

summary_path = GRAPHS / "export_summary.json"
summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
LOGS.mkdir(parents=True, exist_ok=True)

for M, wt, head, kw in SPECS:
    for op in OPSETS + ([17] if M in EXTRA_OPSET17 and head == "full" else []):
        gid = f"{M}.{head}.op{op}"
        if only and only not in gid:
            continue
        if only_op and op != only_op:
            continue
        out = GRAPHS / M / f"{gid}.onnx"
        if out.exists():
            continue
        wd = KIT_HOME / "work" / gid
        if wd.exists():
            shutil.rmtree(wd)
        wd.mkdir(parents=True)
        shutil.copy(WEIGHTS / wt, wd / wt)
        buf = io.StringIO()
        h = logging.StreamHandler(buf)
        lg = logging.getLogger("ultralytics"); lg.addHandler(h)
        t = time.time()
        try:
            f = YOLO(str(wd / wt)).export(format="onnx", device="cpu", imgsz=640, opset=op, dynamic=False, batch=1, **kw)
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), out)
            summary[gid] = {"ok": True, "kwargs": kw, "opset": op, "weights": wt, "weights_sha256": sha256_file(WEIGHTS / wt),
                            "sha256": sha256_file(out), "bytes": out.stat().st_size, "sec": round(time.time() - t, 1),
                            "ultralytics": ultralytics.__version__}
        except Exception as e:
            summary[gid] = {"ok": False, "error": repr(e)[:600], "trace": traceback.format_exc()[-1200:], "kwargs": kw}
        lg.removeHandler(h)
        (LOGS / f"export_{gid}.log").write_text(buf.getvalue(), encoding="utf-8")
        shutil.rmtree(wd, ignore_errors=True)
        print(gid, summary[gid].get("ok"), summary[gid].get("sha256", summary[gid].get("error"))[:70], flush=True)
        summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8")
