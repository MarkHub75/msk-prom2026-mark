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
        if self.manifest.get("decoder") == "split_pose_v8":
            names = self.manifest["split_outputs"]
            nc = len(self.manifest["classes"])
            count = self.manifest.get("keypoint_count",17)
            keypoints = output[:,4+nc:].reshape(1,count,3,-1)
            values = {names["boxes"]: output[:,:4].copy(),
                      names["class_scores"]: output[:,4:4+nc].copy(),
                      names["keypoint_xy"]: keypoints[:,:,:2].copy(),
                      names["keypoint_scores"]: keypoints[:,:,2:].copy()}
        else:
            values = {self.manifest.get("output_name", "output0"): output}
        return {"request_id": request["request_id"], "model_id": request["model_id"], "backend": "pytorch", "status": "ok", "outputs": values, "timings": {"roundtrip_ms": (time.perf_counter() - start) * 1000}}
