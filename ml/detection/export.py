"""Export local trusted YOLOv8 weights and write an explicit model manifest.

Example: python -m ml.detection.export --weights model.pt --output artifacts/model
No automatic weight download or TPU-compatibility claim is made.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import importlib.metadata


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_model(weights, output, model_id, decoder, size=640, opset=13, class_map=None, source=None):
    from ultralytics import YOLO
    import onnx
    weights, output = Path(weights).resolve(), Path(output).resolve()
    if not weights.is_file():
        raise FileNotFoundError(weights)
    output.mkdir(parents=True, exist_ok=True)
    # Export inside owned artifact directory; never overwrite a source neighbor.
    local_weights = output / "weights.pt"
    if local_weights != weights:
        shutil.copy2(weights, local_weights)
    model = YOLO(str(local_weights))
    if model.task != ("pose" if decoder == "pose_v8" else "detect"):
        raise ValueError("weights task does not match decoder")
    names = [model.names[i] for i in range(len(model.names))]
    classes = [(class_map or {}).get(n, n) for n in names]
    exported = Path(model.export(format="onnx", imgsz=size, opset=opset, simplify=False, dynamic=False, batch=1, half=False, nms=False, device="cpu"))
    graph = onnx.load(exported)
    onnx.checker.check_model(graph)
    if len(graph.graph.input) != 1 or len(graph.graph.output) != 1:
        raise ValueError("expected one input and one decoded output")
    shape = [int(d.dim_value) for d in graph.graph.input[0].type.tensor_type.shape.dim]
    manifest = {
        "schema_version": "1.0", "model_id": model_id,
        "decoder": decoder, "classes": classes, "source_classes": names,
        "input": {"name": graph.graph.input[0].name, "shape": shape, "layout": "NCHW", "dtype": "float32", "scale": 1 / 255},
        "output_name": graph.graph.output[0].name, "output_layout": "BCN",
        "nms_in_graph": False, "padding_value": 114,
        "thresholds": {"confidence": .25, "iou": .45, "max_detections": 300},
        "artifacts": {"weights": {"file": "weights.pt", "sha256": sha256(local_weights)}, "onnx": {"file": exported.name, "sha256": sha256(exported)}},
        "versions": {name: importlib.metadata.version(name) for name in ("ultralytics", "torch", "onnx")},
        "opset": opset, "source": source, "linq_status": "NOT_RUN"
    }
    if decoder == "pose_v8":
        kp_shape = model.model.model[-1].kpt_shape
        if list(kp_shape) != [17, 3]:
            raise ValueError("MVP requires COCO-17 keypoints")
        manifest["keypoint_count"] = 17
        manifest["keypoint_order"] = "COCO-17"
    path = output / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--weights", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--decoder", choices=["detect_v8", "pose_v8"], required=True)
    p.add_argument("--size", type=int, default=640)
    p.add_argument("--opset", type=int, default=13)
    p.add_argument("--class-map", help="JSON source-class to canonical-class mapping")
    p.add_argument("--source", help="Pinned source provenance, never credentials")
    a = p.parse_args()
    print(export_model(a.weights, a.output, a.model_id, a.decoder, a.size, a.opset, json.loads(a.class_map) if a.class_map else None, a.source))


if __name__ == "__main__":
    main()
