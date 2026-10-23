"""Run paired native/ONNX inference on exactly the same prepared image."""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from PIL import Image
from .codec import preprocess, decode
from .reference import NativeReferenceBackend
from .export import sha256


def verify(manifest_path, image_path, device="cpu"):
    import onnxruntime as ort
    import torch
    torch.set_num_threads(2)
    # Reference accuracy checks disable reduced-precision CUDA matmul/convolution.
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    manifest_path = Path(manifest_path)
    m = json.loads(manifest_path.read_text())
    frame = np.asarray(Image.open(image_path).convert("RGB"))
    tensor, transform = preprocess(frame, m)
    request = {"request_id": "parity-1", "model_id": m["model_id"], "inputs": {m["input"]["name"]: tensor}}
    native = NativeReferenceBackend(manifest_path.parent / m["artifacts"]["weights"]["file"], m, device)
    reference = native.infer(request)
    options = ort.SessionOptions(); options.intra_op_num_threads = 2
    session = ort.InferenceSession(str(manifest_path.parent / m["artifacts"]["onnx"]["file"]), sess_options=options, providers=["CPUExecutionProvider"])
    start = time.perf_counter()
    output_names = list(m["split_outputs"].values()) if m["decoder"] == "split_pose_v8" else [m["output_name"]]
    output_values = session.run(output_names, request["inputs"])
    outputs = dict(zip(output_names,output_values))
    elapsed = (time.perf_counter() - start) * 1000
    if m["decoder"] == "split_pose_v8":
        a = np.concatenate([v.reshape(-1) for v in reference["outputs"].values()])
        b = np.concatenate([outputs[name].reshape(-1) for name in reference["outputs"]])
    else:
        a, b = reference["outputs"][m["output_name"]], outputs[m["output_name"]]
    native_d = decode(reference["outputs"], m, transform)
    onnx_d = decode(outputs, m, transform)
    report = {"model_id": m["model_id"], "image_sha256": sha256(image_path), "weights_sha256": m["artifacts"]["weights"]["sha256"], "onnx_sha256": m["artifacts"]["onnx"]["sha256"], "shape": list(a.shape), "native_device": device, "raw_max_abs_error": float(np.max(np.abs(a - b))), "raw_allclose_atol_1e-3_rtol_1e-3": bool(np.allclose(a,b,atol=1e-3,rtol=1e-3)), "native_detections": len(native_d), "onnx_detections": len(onnx_d), "native_roundtrip_ms": reference["timings"]["roundtrip_ms"], "onnx_cpu_ms": elapsed, "linq_status": "NOT_RUN", "scope": "single paired image, not task accuracy or steady throughput"}
    return report, native_d, onnx_d


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", required=True); p.add_argument("--image", required=True)
    p.add_argument("--device", default="cpu"); p.add_argument("--output", required=True)
    a = p.parse_args(); report, native, onnx = verify(a.manifest, a.image, a.device)
    Path(a.output).write_text(json.dumps({"report": report, "native": native, "onnx": onnx}, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report["raw_allclose_atol_1e-3_rtol_1e-3"]:
        raise SystemExit(1)


if __name__ == "__main__": main()
