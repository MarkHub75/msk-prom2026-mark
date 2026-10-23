"""Pre/post-processing for Ultralytics YOLO (v8/11) exported with nms=False.

Shared by the CPU reference (onnxruntime) and the LinQ TPU path so both see identical
tensors. Contract (Ultralytics 8.3.x export, nms=False):
  input  'images'  float32 [1,3,H,W], RGB, /255, letterbox pad 114, NCHW
  det    'output0' float32 [1, 4+nc, A]       boxes cx,cy,w,h in input pixels, class scores
                                              already sigmoid-ed, DFL/decode inside graph
  pose   'output0' float32 [1, 4+1+17*3, A]   + kpts x,y,conf (conf sigmoid-ed)
No objectness column (4+nc, not 5+nc).
"""
from __future__ import annotations

import numpy as np

COCO80 = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
          "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
          "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
          "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
          "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
          "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
          "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
          "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
          "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
          "teddy bear", "hair drier", "toothbrush"]
# classes the product cares about (COCO ids)
TARGET_CLASSES = {0: "person", 67: "cell phone", 2: "car", 7: "truck", 5: "bus"}


def letterbox(img_rgb: np.ndarray, size: int, pad: int = 114) -> tuple[np.ndarray, float, tuple[int, int]]:
    """Resize keeping aspect, pad to size x size. Returns (img, scale, (pad_x, pad_y))."""
    import cv2
    h, w = img_rgb.shape[:2]
    r = min(size / h, size / w)
    nh, nw = int(round(h * r)), int(round(w * r))
    resized = cv2.resize(img_rgb, (nw, nh), interpolation=cv2.INTER_LINEAR) if (nh, nw) != (h, w) else img_rgb
    px, py = (size - nw) // 2, (size - nh) // 2
    out = np.full((size, size, 3), pad, dtype=np.uint8)
    out[py:py + nh, px:px + nw] = resized
    return out, r, (px, py)


def preprocess(img_rgb: np.ndarray, size: int) -> tuple[np.ndarray, dict]:
    lb, r, (px, py) = letterbox(img_rgb, size)
    x = (lb.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
    return np.ascontiguousarray(x), {"scale": r, "pad": (px, py), "orig_hw": img_rgb.shape[:2], "size": size}


def _nms(boxes: np.ndarray, scores: np.ndarray, iou: float) -> list[int]:
    x1, y1, x2, y2 = boxes.T
    areas = (x2 - x1).clip(0) * (y2 - y1).clip(0)
    order = scores.argsort()[::-1]
    keep = []
    while order.size:
        i = order[0]
        keep.append(int(i))
        xx1 = np.maximum(x1[i], x1[order[1:]]); yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]]); yy2 = np.minimum(y2[i], y2[order[1:]])
        inter = (xx2 - xx1).clip(0) * (yy2 - yy1).clip(0)
        ov = inter / (areas[i] + areas[order[1:]] - inter + 1e-9)
        order = order[1:][ov <= iou]
    return keep


def postprocess(out: np.ndarray, meta: dict, conf: float = 0.25, iou: float = 0.45,
                nc: int = 80, kpt_shape: tuple[int, int] | None = None, classes=None,
                max_det: int = 300) -> list[dict]:
    """[1, 4+nc(+K*D), A] -> list of {cls, name, score, bbox_xyxy[, kpts]} in original pixels.

    Class-aware NMS (offset trick), like Ultralytics non_max_suppression(agnostic=False).
    """
    p = np.asarray(out, dtype=np.float32)
    if p.ndim == 3:
        p = p[0]
    exp_ch = 4 + nc + (kpt_shape[0] * kpt_shape[1] if kpt_shape else 0)
    if p.shape[0] != exp_ch:  # explicit, no guessing of transposed layouts
        if p.shape[1] == exp_ch:
            p = p.T
        else:
            raise ValueError(f"unexpected YOLO output shape {out.shape}, expected (1,{exp_ch},A)")
    boxes_cxcywh, cls_scores = p[:4].T, p[4:4 + nc].T
    cls_id = cls_scores.argmax(1)
    score = cls_scores[np.arange(len(cls_id)), cls_id]
    m = score > conf
    if classes is not None:
        m &= np.isin(cls_id, list(classes))
    idx = np.nonzero(m)[0]
    if idx.size == 0:
        return []
    b = boxes_cxcywh[idx]
    xyxy = np.stack([b[:, 0] - b[:, 2] / 2, b[:, 1] - b[:, 3] / 2, b[:, 0] + b[:, 2] / 2, b[:, 1] + b[:, 3] / 2], 1)
    keep = _nms(xyxy + (cls_id[idx] * 7680.0)[:, None], score[idx], iou)[:max_det]
    r, (px, py) = meta["scale"], meta["pad"]
    h, w = meta["orig_hw"]
    dets = []
    for k in keep:
        i = idx[k]
        x1, y1, x2, y2 = xyxy[k]
        bb = [float(np.clip((x1 - px) / r, 0, w)), float(np.clip((y1 - py) / r, 0, h)),
              float(np.clip((x2 - px) / r, 0, w)), float(np.clip((y2 - py) / r, 0, h))]
        d = {"cls": int(cls_id[i]), "name": COCO80[int(cls_id[i])] if nc == 80 else str(int(cls_id[i])),
             "score": float(score[i]), "bbox_xyxy": [round(v, 1) for v in bb]}
        if kpt_shape:
            kp = p[4 + nc:, i].reshape(kpt_shape).copy()
            kp[:, 0] = (kp[:, 0] - px) / r
            kp[:, 1] = (kp[:, 1] - py) / r
            d["kpts"] = [[round(float(v), 2) for v in row] for row in kp]
        dets.append(d)
    return dets


def iou_xyxy(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def match_dets(ref: list[dict], test: list[dict], iou_thr: float = 0.5) -> dict:
    """Greedy same-class matching ref (CPU) vs test (TPU)."""
    used, pairs = set(), []
    for r in sorted(ref, key=lambda d: -d["score"]):
        best, bj = 0.0, -1
        for j, t in enumerate(test):
            if j in used or t["cls"] != r["cls"]:
                continue
            v = iou_xyxy(r["bbox_xyxy"], t["bbox_xyxy"])
            if v > best:
                best, bj = v, j
        if bj >= 0 and best >= iou_thr:
            used.add(bj)
            pairs.append((r, test[bj], best))
    n_ref, n_test, n_m = len(ref), len(test), len(pairs)
    kpt_err = []
    for r, t, _ in pairs:
        if "kpts" in r and "kpts" in t:
            a, b = np.asarray(r["kpts"]), np.asarray(t["kpts"])
            vis = a[:, 2] > 0.5  # keypoints the fp32 model considers visible
            if vis.any():
                diag = float(np.hypot(r["bbox_xyxy"][2] - r["bbox_xyxy"][0], r["bbox_xyxy"][3] - r["bbox_xyxy"][1]))
                kpt_err.append(float(np.linalg.norm(a[vis, :2] - b[vis, :2], axis=1).mean()) / max(diag, 1.0))
    extra = {"mean_kpt_err_rel_diag": float(np.mean(kpt_err))} if kpt_err else {}
    return {
        **extra,
        "n_ref": n_ref, "n_test": n_test, "matched": n_m,
        "recall_vs_ref": n_m / n_ref if n_ref else 1.0,
        "precision_vs_ref": n_m / n_test if n_test else 1.0,
        "mean_iou": float(np.mean([p[2] for p in pairs])) if pairs else None,
        "mean_abs_score_diff": float(np.mean([abs(p[0]["score"] - p[1]["score"]) for p in pairs])) if pairs else None,
    }
