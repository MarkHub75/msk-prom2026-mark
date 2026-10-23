"""Letterbox and versioned YOLO output ABIs; no network/runtime dependencies."""
from dataclasses import dataclass
from collections.abc import Mapping
import numpy as np
from PIL import Image


@dataclass(frozen=True)
class LetterboxTransform:
    original_width: int
    original_height: int
    input_width: int
    input_height: int
    resized_width: int
    resized_height: int
    left: int
    top: int

    def points(self, xy):
        out = np.asarray(xy, dtype=np.float64).copy()
        out[..., 0] = (out[..., 0] - self.left) * self.original_width / self.resized_width
        out[..., 1] = (out[..., 1] - self.top) * self.original_height / self.resized_height
        out[..., 0] = np.clip(out[..., 0], 0, self.original_width)
        out[..., 1] = np.clip(out[..., 1], 0, self.original_height)
        return out


def preprocess(frame, manifest):
    """RGB uint8 HWC -> owned contiguous model tensor plus exact resize geometry."""
    frame = np.asarray(frame)
    if frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
        raise ValueError("frame must be RGB uint8 HWC with three channels")
    oh, ow = frame.shape[:2]
    if not oh or not ow:
        raise ValueError("empty frame")
    spec = manifest["input"]
    layout = spec.get("layout", "NCHW")
    shape = spec["shape"]
    if layout not in ("NCHW", "NHWC") or len(shape) != 4 or shape[0] != 1:
        raise ValueError("only explicit static batch-one NCHW/NHWC inputs supported")
    if layout == "NCHW":
        _, channels, ih, iw = shape
    else:
        _, ih, iw, channels = shape
    if channels != 3 or not isinstance(iw, int) or not isinstance(ih, int) or min(iw, ih) < 1:
        raise ValueError("invalid static input shape")
    ratio = min(iw / ow, ih / oh)
    rw, rh = max(1, round(ow * ratio)), max(1, round(oh * ratio))
    left, top = (iw - rw) // 2, (ih - rh) // 2
    resized = np.asarray(Image.fromarray(frame).resize((rw, rh), Image.Resampling.BILINEAR))
    canvas = np.full((ih, iw, 3), manifest.get("padding_value", 114), dtype=np.uint8)
    canvas[top:top + rh, left:left + rw] = resized
    dtype = np.dtype(spec.get("dtype", "float32"))
    if dtype not in (np.dtype("float32"), np.dtype("float16"), np.dtype("uint8")):
        raise ValueError("unsupported input dtype")
    scale = spec.get("scale", 1 / 255 if dtype.kind == "f" else 1)
    if dtype.kind != "f" and scale != 1:
        raise ValueError("integer input requires explicit unscaled RGB")
    tensor = canvas.astype(dtype)
    if dtype.kind == "f":
        tensor *= scale
    if layout == "NCHW":
        tensor = tensor.transpose(2, 0, 1)
    return np.ascontiguousarray(tensor[None]), LetterboxTransform(ow, oh, iw, ih, rw, rh, left, top)


def _nms(boxes, scores, classes, iou_threshold, limit):
    # Stable score ordering makes tied-score output reproducible.
    order = np.argsort(-scores, kind="stable")
    keep = []
    while len(order) and len(keep) < limit:
        i = int(order[0]); keep.append(i)
        rest = order[1:]
        if not len(rest):
            break
        tl = np.maximum(boxes[i, :2], boxes[rest, :2])
        br = np.minimum(boxes[i, 2:], boxes[rest, 2:])
        inter = np.prod(np.maximum(br - tl, 0), axis=1)
        area_i = np.prod(np.maximum(boxes[i, 2:] - boxes[i, :2], 0))
        area_r = np.prod(np.maximum(boxes[rest, 2:] - boxes[rest, :2], 0), axis=1)
        iou = inter / np.maximum(area_i + area_r - inter, 1e-12)
        order = rest[(classes[rest] != classes[i]) | (iou <= iou_threshold)]
    return keep


def decode(outputs, manifest, transform):
    """Decode already-decoded YOLO boxes (not raw conv heads) and apply NMS once.

    v8/pose_v8 default BCN; classic v5 default BNC. v5 scores=obj*class;
    v8 scores are class probabilities. No sigmoid, DFL, stride or anchor decode.
    """
    decoder = manifest["decoder"]
    if decoder not in ("detect_v8", "pose_v8", "detect_v5"):
        raise ValueError("unsupported decoder; raw/end-to-end outputs require a separate adapter")
    if manifest.get("nms_in_graph", False):
        raise ValueError("post-NMS graph output cannot use a pre-NMS decoder")
    classes = manifest["classes"]
    if not isinstance(classes, list) or not classes or len(set(classes)) != len(classes):
        raise ValueError("classes must be an ordered unique list")
    if isinstance(outputs, Mapping):
        name = manifest.get("output_name")
        if name is None:
            if len(outputs) != 1:
                raise ValueError("multiple outputs require output_name")
            raw = next(iter(outputs.values()))
        else:
            raw = outputs[name]
    elif isinstance(outputs, (tuple, list)):
        if len(outputs) != 1:
            raise ValueError("exactly one decoded output required")
        raw = outputs[0]
    else:
        raw = outputs
    raw = np.asarray(raw)
    if raw.ndim != 3 or raw.shape[0] != 1 or raw.dtype.kind != "f":
        raise ValueError("decoded output must be floating batch-one rank three")
    layout = manifest.get("output_layout", "BNC" if decoder == "detect_v5" else "BCN")
    if layout not in ("BNC", "BCN"):
        raise ValueError("output_layout must be BNC or BCN")
    rows = raw[0].T if layout == "BCN" else raw[0]
    nc = len(classes)
    keypoint_count = int(manifest.get("keypoint_count", 17)) if decoder == "pose_v8" else 0
    expected = 4 + nc + (1 if decoder == "detect_v5" else 0) + keypoint_count * 3
    if rows.shape[1] != expected:
        raise ValueError(f"channel count {rows.shape[1]} does not match explicit ABI {expected}")
    if not np.all(np.isfinite(rows)):
        raise ValueError("nonfinite model output")
    class_start = 5 if decoder == "detect_v5" else 4
    probs = rows[:, class_start:class_start + nc]
    if np.any((probs < 0) | (probs > 1)):
        raise ValueError("expected probabilities, not logits")
    if decoder == "detect_v5" and np.any((rows[:, 4] < 0) | (rows[:, 4] > 1)):
        raise ValueError("invalid objectness")
    cls = np.argmax(probs, axis=1)
    scores = probs[np.arange(len(rows)), cls]
    if decoder == "detect_v5":
        scores = scores * rows[:, 4]
    cfg = manifest.get("thresholds", {})
    conf, iou = float(cfg.get("confidence", .25)), float(cfg.get("iou", .45))
    limit = int(cfg.get("max_detections", 300))
    if not (0 <= conf <= 1 and 0 <= iou <= 1 and limit > 0):
        raise ValueError("invalid NMS thresholds")
    accepted = (scores >= conf) & (rows[:, 2] > 0) & (rows[:, 3] > 0)
    rows, scores, cls = rows[accepted], scores[accepted], cls[accepted]
    boxes = np.concatenate((rows[:, :2] - rows[:, 2:4] / 2, rows[:, :2] + rows[:, 2:4] / 2), axis=1)
    keep = _nms(boxes, scores, cls, iou, limit)
    results = []
    for idx in keep:
        box = transform.points(boxes[idx].reshape(2, 2)).reshape(4)
        if box[2] <= box[0] or box[3] <= box[1]:
            continue
        keypoints = None
        if keypoint_count:
            kp = rows[idx, 4 + nc:].reshape(keypoint_count, 3).astype(np.float64).copy()
            if np.any((kp[:, 2] < 0) | (kp[:, 2] > 1)):
                raise ValueError("invalid keypoint probabilities")
            kp[:, :2] = transform.points(kp[:, :2])
            keypoints = kp.tolist()
        results.append({"detection_id": f"d{len(results)}", "class_name": classes[int(cls[idx])], "score": float(scores[idx]), "bbox_xyxy": box.tolist(), "keypoints": keypoints})
    return results
