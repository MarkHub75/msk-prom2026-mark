"""Export an Ultralytics model to static ONNX for the LinQ SDK and write a contract sidecar.

    python tools/linq/export_onnx.py --model yolov8n.pt --imgsz 640
    python tools/linq/export_onnx.py --model yolov8n-pose.pt --imgsz 640

Output: models/<stem>_<imgsz>_op<opset>.onnx + .json (input/output names, shapes, export args).
Export profile: batch 1, static, fp32, nms=False (DFL/decode stay in the graph), simplify.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="yolov8n.pt")
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--opset", type=int, default=13)
    ap.add_argument("--no-simplify", action="store_true")
    a = ap.parse_args()

    import onnx
    import ultralytics
    from ultralytics import YOLO

    models = REPO / "models"
    models.mkdir(exist_ok=True)
    pt = models / a.model
    m = YOLO(str(pt) if pt.exists() else a.model)  # downloads into cwd if missing
    if not pt.exists() and Path(a.model).exists():
        shutil.move(a.model, pt)
    args = dict(format="onnx", imgsz=a.imgsz, opset=a.opset, batch=1, dynamic=False, half=False,
                nms=False, simplify=not a.no_simplify)
    src = Path(m.export(**args))
    dst = models / f"{Path(a.model).stem}_{a.imgsz}_op{a.opset}.onnx"
    shutil.move(str(src), dst)

    g = onnx.load(str(dst))
    dims = lambda t: [d.dim_value or d.dim_param for d in t.type.tensor_type.shape.dim]
    ops = sorted({n.op_type for n in g.graph.node})
    meta = {
        "onnx": dst.name, "source": a.model, "ultralytics": ultralytics.__version__,
        "export_args": args, "opset_imports": {i.domain or "ai.onnx": i.version for i in g.opset_import},
        "inputs": [{"name": t.name, "shape": dims(t), "dtype": "float32"} for t in g.graph.input],
        "outputs": [{"name": t.name, "shape": dims(t)} for t in g.graph.output],
        "task": m.task, "nc": len(m.names), "kpt_shape": list(getattr(m.model, "kpt_shape", []) or []) or None,
        "ops": ops, "n_nodes": len(g.graph.node),
        "preprocess": "RGB, letterbox to imgsz (pad 114, centered), /255, NCHW float32",
    }
    dst.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("onnx", "inputs", "outputs", "task", "nc", "kpt_shape", "n_nodes")}))
    print("ops:", " ".join(ops))


if __name__ == "__main__":
    main()
