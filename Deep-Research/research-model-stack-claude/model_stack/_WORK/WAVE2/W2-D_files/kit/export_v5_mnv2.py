"""Step 1b: YOLOv5s v7.0 (official ultralytics/yolov5 tag v7.0, commit 915bbf29, export.py with torch.onnx.export forced to dynamo=False,
same trick as W1-10 run_v5_export_legacy.py) and torchvision mobilenet_v2 classifier -> ONNX at opsets {11,13,18}; then onnxslim (as Ultralytics does).
Usage: py -I export_v5_mnv2.py YOLOV5_V70_ROOT
Output: graphs/v5s7/v5s7.full.op<N>.onnx, graphs/mnv2/mnv2.logits.op<N>.onnx (+ mnv2 weights sha)."""
import json, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kitlib import GRAPHS, KIT_HOME, LOGS, WEIGHTS, sha256_file

V5ROOT = Path(sys.argv[1])
OPS = [11, 13, 18]
summary = {}
RUNNER = '''
import sys, runpy, torch
root = sys.argv[1]; args = sys.argv[2:]
_f = torch.onnx.export
def _legacy(*a, **k):
    k.setdefault("dynamo", False)
    return _f(*a, **k)
torch.onnx.export = _legacy
sys.path.insert(0, root)
sys.argv = [root + "/export.py"] + args
runpy.run_path(root + "/export.py", run_name="__main__")
'''
import onnx, onnxslim

# ---- YOLOv5s v7.0
for op in OPS:
    gid = f"v5s7.full.op{op}"
    out = GRAPHS / "v5s7" / f"{gid}.onnx"
    if out.exists():
        continue
    wd = KIT_HOME / "work" / gid
    shutil.rmtree(wd, ignore_errors=True); wd.mkdir(parents=True)
    shutil.copy(WEIGHTS / "yolov5s_v7.0.pt", wd / "yolov5s.pt")
    (wd / "runner.py").write_text(RUNNER)
    t = time.time()
    r = subprocess.run([sys.executable, "-I", str(wd / "runner.py"), str(V5ROOT), "--weights", str(wd / "yolov5s.pt"),
                        "--include", "onnx", "--opset", str(op), "--imgsz", "640", "--device", "cpu"],
                       capture_output=True, text=True, env={**__import__("os").environ, "PYTHONUTF8": "1"}, cwd=str(wd))
    (LOGS / f"export_{gid}.log").write_text(r.stdout + "\n---stderr---\n" + r.stderr, encoding="utf-8")
    f = wd / "yolov5s.onnx"
    if r.returncode != 0 or not f.exists():
        summary[gid] = {"ok": False, "rc": r.returncode, "stderr_tail": r.stderr[-800:]}
    else:
        m = onnx.load(str(f)); ms = onnxslim.slim(m)
        out.parent.mkdir(parents=True, exist_ok=True)
        onnx.save(ms, str(out))
        summary[gid] = {"ok": True, "sha256": sha256_file(out), "bytes": out.stat().st_size, "sec": round(time.time() - t, 1),
                        "raw_export_sha256": sha256_file(f), "weights_sha256": sha256_file(WEIGHTS / "yolov5s_v7.0.pt"),
                        "yolov5_commit": "915bbf294bb74c859f0b41f1c23bc395014ea679 (tag v7.0, from local clone; verified by git log in W1-10)"}
    print(gid, summary[gid].get("ok"), flush=True)

# ---- torchvision mobilenet_v2 (classifier). Weights: torchvision official IMAGENET1K_V1 (downloaded by torchvision itself)
import torch, torchvision
try:
    mdl = torchvision.models.mobilenet_v2(weights=torchvision.models.MobileNet_V2_Weights.IMAGENET1K_V1)
    wsrc = "torchvision MobileNet_V2_Weights.IMAGENET1K_V1"
except Exception as e:
    print("WEIGHTS DOWNLOAD FAILED, using random init (graph structure/parity only):", repr(e)[:200])
    torch.manual_seed(0)
    mdl = torchvision.models.mobilenet_v2(weights=None); wsrc = "random init (seed 0) - download failed: " + repr(e)[:120]
mdl.eval()
torch.save(mdl.state_dict(), WEIGHTS / "mnv2_state_dict.pt")   # our own file, for reproducibility (safe: state_dict of tensors)
x = torch.zeros(1, 3, 224, 224)
for op in OPS:
    gid = f"mnv2.logits.op{op}"
    out = GRAPHS / "mnv2" / f"{gid}.onnx"
    if out.exists():
        continue
    tmp = KIT_HOME / "work" / f"{gid}.raw.onnx"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(mdl, x, str(tmp), opset_version=op, dynamo=False, input_names=["images"], output_names=["output0"])
    m = onnxslim.slim(onnx.load(str(tmp)))
    onnx.save(m, str(out))
    summary[gid] = {"ok": True, "sha256": sha256_file(out), "bytes": out.stat().st_size, "weights": wsrc,
                    "weights_state_dict_sha256": sha256_file(WEIGHTS / "mnv2_state_dict.pt"), "torchvision": torchvision.__version__}
    print(gid, "ok", flush=True)
(GRAPHS / "export_summary_v5_mnv2.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
