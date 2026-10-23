"""Explicit PyTorch reference backend; never used as an automatic TPU fallback."""
import time
import numpy as np


class NativeReferenceBackend:
    def __init__(self, weights, manifest, device="cpu"):
        import torch
        from ultralytics import YOLO
        self.torch = torch
        self.model = YOLO(str(weights)).model.to(device).eval()
        self.manifest = manifest
        self.device = device

    def infer(self, request):
        if request["model_id"] != self.manifest["model_id"]:
            raise ValueError("model_id mismatch")
        spec = self.manifest["input"]
        if set(request["inputs"]) != {spec["name"]}:
            raise ValueError("input names mismatch")
        arr = np.asarray(request["inputs"][spec["name"]])
        if tuple(arr.shape) != tuple(spec["shape"]) or arr.dtype != np.dtype(spec["dtype"]) or not arr.flags.c_contiguous or not np.all(np.isfinite(arr)):
            raise ValueError("input shape/dtype/contiguity/finite mismatch")
        if spec.get("layout", "NCHW") != "NCHW":
            raise ValueError("PyTorch reference expects NCHW")
        start = time.perf_counter()
        with self.torch.inference_mode():
            result = self.model(self.torch.from_numpy(arr).to(self.device))
        # Ultralytics eval returns (decoded predictions, auxiliary raw features).
        if isinstance(result, (tuple, list)):
            result = result[0]
        output = result.detach().cpu().numpy().copy()
        return {"request_id": request["request_id"], "model_id": request["model_id"], "backend": "pytorch", "status": "ok", "outputs": {self.manifest.get("output_name", "output0"): output}, "timings": {"roundtrip_ms": (time.perf_counter() - start) * 1000}}
