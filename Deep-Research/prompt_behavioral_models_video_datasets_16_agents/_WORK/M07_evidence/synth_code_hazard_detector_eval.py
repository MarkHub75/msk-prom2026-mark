"""
Suspended-load hazard detection evaluation — ACM MM 2026 dataset.

Runs YOLO World and/or Grounding DINO on 227 synthetic videos,
reads ground-truth labels from a CSV, and produces per-video results
and confusion matrices (overall + per-tier) with F2, F1, precision,
recall, specificity, and bootstrap confidence intervals.

Usage:
    python detection_eval.py --model yolo_world
    python detection_eval.py --model grounding_dino
    python detection_eval.py --model both
    python detection_eval.py --model yolo_world --annotate   # also save annotated output videos
"""

import argparse
import csv
import math
import time
from collections import defaultdict, deque
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from tqdm import tqdm

# =========================================================
# PATHS
# =========================================================

DATASET_ROOT = Path("./dataset")
VIDEOS_DIR = DATASET_ROOT / "videos"
LABELS_CSV = DATASET_ROOT / "synthetic_video_labels.csv"
OUTPUT_DIR = Path("./hazard_detection")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}

# =========================================================
# LABEL LOADING
# =========================================================

def load_labels(csv_path: Path = LABELS_CSV) -> list[dict]:
    """Load ground-truth labels from CSV.

    Returns list of {filename, tier, ground_truth} where ground_truth
    is 'UNSAFE' (True_Positive) or 'SAFE' (False_Positive).
    """
    entries = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            resolved = row["resolved_label"].strip()
            gt = "UNSAFE" if resolved == "True_Positive" else "SAFE"
            entries.append({
                "filename": row["filename"].strip(),
                "tier": int(row["tier"]),
                "ground_truth": gt,
            })
    return entries


# =========================================================
# METRICS
# =========================================================

def compute_metrics(y_true: list[int], y_pred: list[int]) -> dict:
    """Compute F2, F1, precision, recall, specificity, counts."""
    yt = np.asarray(y_true, dtype=int)
    yp = np.asarray(y_pred, dtype=int)

    tp = int(np.sum((yp == 1) & (yt == 1)))
    fp = int(np.sum((yp == 1) & (yt == 0)))
    fn = int(np.sum((yp == 0) & (yt == 1)))
    tn = int(np.sum((yp == 0) & (yt == 0)))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    beta = 2
    f2 = ((1 + beta**2) * precision * recall / (beta**2 * precision + recall)
          if (beta**2 * precision + recall) > 0 else 0.0)

    return {
        "n": len(yt), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall, "specificity": specificity,
        "f1": f1, "f2": f2,
    }


def bootstrap_ci(
    y_true: list[int], y_pred: list[int],
    n_bootstrap: int = 1000, confidence: float = 0.95, seed: int = 42,
) -> tuple[float, float]:
    """Bootstrap 95% CI for F2."""
    rng = np.random.RandomState(seed)
    yt = np.asarray(y_true, dtype=int)
    yp = np.asarray(y_pred, dtype=int)
    n = len(yt)
    if n == 0:
        return (0.0, 0.0)
    scores = []
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, size=n)
        m = compute_metrics(yt[idx].tolist(), yp[idx].tolist())
        scores.append(m["f2"])
    alpha = 1 - confidence
    return (float(np.percentile(scores, 100 * alpha / 2)),
            float(np.percentile(scores, 100 * (1 - alpha / 2))))


# =========================================================
# YOLO WORLD PIPELINE
# =========================================================

# --- Parameters (identical to previous evaluation) ---
YW_MODEL_NAME = "yolov8x-worldv2.pt"
YW_CUSTOM_CLASSES = [
    "person", "hoisted load with crane hook",
    "excavators", "trucks", "Tower crane", "Truck crane",
    "Roller", "Bulldozer", "Excavator", "Truck",
    "Loader", "Pump truck", "Concrete truck", "Pile truck",
]
YW_PERSON_CLASS = "person"
YW_LOAD_CLASS = "hoisted load with crane hook"
YW_CONF = 0.30
YW_IOU = 0.40
YW_SUSPENDED_CLEARANCE_RATIO = 0.12
YW_NEARBY_WORKER_X_EXPANSION = 1.25
YW_ASSUMED_WORKER_HEIGHT_M = 1.75
YW_GRAVITY = 9.81
YW_V_DRIFT_MIN = 0.4
YW_VELOCITY_BUFFER_SIZE = 8
YW_MIN_HAZARD_EXPANSION_PX = 30
YW_USE_VERTICAL_GATE = True
YW_VERTICAL_GATE_PX = 40
YW_WINDOW_SECONDS = 1.0
YW_K_THRESHOLD = 12
YW_GAP_FILL = True
YW_MAX_NEG_GAP = 2


def _yw_footpoint(xyxy):
    x1, y1, x2, y2 = xyxy.astype(float)
    return ((x1 + x2) / 2.0, y2)


def _yw_center(xyxy):
    x1, y1, x2, y2 = xyxy.astype(float)
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def _yw_wh(xyxy):
    x1, y1, x2, y2 = xyxy.astype(float)
    return (max(1.0, x2 - x1), max(1.0, y2 - y1))


def _yw_filter_class(dets: sv.Detections, cid: int) -> sv.Detections:
    if len(dets) == 0:
        return dets
    return dets[dets.class_id == cid]


def _yw_fill_gaps(seq: list[int], max_gap: int) -> list[int]:
    arr = seq[:]
    n = len(arr)
    i = 0
    while i < n:
        if arr[i] == 0:
            start = i
            while i < n and arr[i] == 0:
                i += 1
            end = i - 1
            gap_len = end - start + 1
            left_ok = start - 1 >= 0 and arr[start - 1] == 1
            right_ok = i < n and arr[i] == 1
            if left_ok and right_ok and gap_len <= max_gap:
                for j in range(start, end + 1):
                    arr[j] = 1
        else:
            i += 1
    return arr


def _yw_ppm(person_dets):
    if len(person_dets) == 0:
        return None
    heights = [_yw_wh(person_dets.xyxy[i])[1] for i in range(len(person_dets))]
    med = float(np.median(heights))
    return med / YW_ASSUMED_WORKER_HEIGHT_M if med >= 10 else None


def _yw_ground_y(person_dets):
    if len(person_dets) == 0:
        return None
    return float(np.median([_yw_footpoint(person_dets.xyxy[i])[1]
                            for i in range(len(person_dets))]))


def _yw_update_vel(vel_hist, load_dets, prev_pos, fps):
    cur = {}
    dt = 1.0 / max(fps, 1.0)
    for i in range(len(load_dets)):
        tid = (int(load_dets.tracker_id[i])
               if load_dets.tracker_id is not None and load_dets.tracker_id[i] is not None
               else -1)
        if tid == -1:
            continue
        cx, _ = _yw_center(load_dets.xyxy[i])
        cur[tid] = cx
        if tid in prev_pos:
            dx = abs(cx - prev_pos[tid])
            if tid not in vel_hist:
                vel_hist[tid] = deque(maxlen=YW_VELOCITY_BUFFER_SIZE)
            vel_hist[tid].append(dx / dt)
    return cur


def _yw_get_vel(vel_hist, tid):
    if tid not in vel_hist or len(vel_hist[tid]) == 0:
        return 0.0
    return float(max(vel_hist[tid]))


def _yw_suspended_loads(load_dets, person_dets, ppm, ground_y_fb, vel_hist):
    infos = []
    pboxes = person_dets.xyxy if len(person_dets) > 0 else np.empty((0, 4))
    for li in range(len(load_dets)):
        lbox = load_dets.xyxy[li]
        lconf = float(load_dets.confidence[li]) if load_dets.confidence is not None else 0.0
        ltid = (int(load_dets.tracker_id[li])
                if load_dets.tracker_id is not None and load_dets.tracker_id[li] is not None
                else -1)
        x1, y1, x2, y2 = lbox.astype(float)
        lcx, _ = _yw_center(lbox)
        lw, _ = _yw_wh(lbox)

        best_cr = -999.0
        best_fy = None
        for wi in range(len(pboxes)):
            fx, fy = _yw_footpoint(pboxes[wi])
            if abs(fx - lcx) <= YW_NEARBY_WORKER_X_EXPANSION * lw:
                _, wh = _yw_wh(pboxes[wi])
                cr = (fy - y2) / max(wh, 1.0)
                if cr > best_cr:
                    best_cr = cr
                    best_fy = fy

        suspended = best_cr >= YW_SUSPENDED_CLEARANCE_RATIO
        local_gy = best_fy if best_fy is not None else (ground_y_fb if ground_y_fb is not None else float(y2))
        lh_px = max(0.0, local_gy - y2)
        if ppm and ppm > 0:
            lh_m = lh_px / ppm
        else:
            ppm_local = None
            lh_m = 0.0

        ft = math.sqrt(2.0 * lh_m / YW_GRAVITY) if lh_m > 0 else 0.0
        vpx = _yw_get_vel(vel_hist, ltid)
        v_obs = (vpx / ppm) if (ppm and ppm > 0) else 0.0
        v_eff = max(YW_V_DRIFT_MIN, v_obs)
        lat_m = v_eff * ft
        lat_px = (lat_m * ppm) if (ppm and ppm > 0) else 0.0
        lat_px = max(lat_px, YW_MIN_HAZARD_EXPANSION_PX)

        infos.append({
            "lconf": lconf, "ltid": ltid,
            "lcx": lcx, "lbot_y": y2, "lw": lw,
            "gy": local_gy, "suspended": suspended,
            "ztop_hw": lw / 2.0 + YW_MIN_HAZARD_EXPANSION_PX,
            "zbot_hw": lw / 2.0 + lat_px,
        })
    return infos


def _yw_zone_hw(info, foot_y):
    span = info["gy"] - info["lbot_y"]
    if span <= 0:
        return info["zbot_hw"]
    t = max(0.0, min(1.0, (foot_y - info["lbot_y"]) / span))
    return info["ztop_hw"] + t * (info["zbot_hw"] - info["ztop_hw"])


def _yw_hazard_pairs(infos, person_dets):
    if len(person_dets) == 0 or not infos:
        return False
    for li in infos:
        if not li["suspended"]:
            continue
        for wi in range(len(person_dets)):
            fx, fy = _yw_footpoint(person_dets.xyxy[wi])
            hw = _yw_zone_hw(li, fy)
            if abs(fx - li["lcx"]) <= hw:
                if not YW_USE_VERTICAL_GATE or fy > (li["lbot_y"] - YW_VERTICAL_GATE_PX):
                    return True
    return False


def yw_classify_video(model, video_path: Path, person_cid: int, load_cid: int) -> dict:
    """Run full YOLO World pipeline on one video. Returns classification dict."""
    info = sv.VideoInfo.from_video_path(str(video_path))
    fps = info.fps
    if fps == 0 or np.isnan(fps) or fps > 120:
        fps = 30

    tracker = sv.ByteTrack()
    ws = max(1, int(round(fps * YW_WINDOW_SECONDS)))
    hist = deque(maxlen=ws)
    vel_hist: dict[int, deque] = defaultdict(lambda: deque(maxlen=YW_VELOCITY_BUFFER_SIZE))
    prev_pos: dict[int, float] = {}

    clip_unsafe = False
    total = 0
    haz_frames = 0
    first_unsafe = None

    for frame in sv.get_video_frames_generator(str(video_path)):
        total += 1
        results = model.predict(frame, conf=YW_CONF, iou=YW_IOU, verbose=False)[0]
        dets = sv.Detections.from_ultralytics(results)
        dets = tracker.update_with_detections(dets)

        if len(dets) > 0:
            keep = np.isin(dets.class_id, [person_cid, load_cid])
            dets = dets[keep]

        pdets = _yw_filter_class(dets, person_cid)
        ldets = _yw_filter_class(dets, load_cid)

        ppm = _yw_ppm(pdets)
        gyf = _yw_ground_y(pdets)
        prev_pos = _yw_update_vel(vel_hist, ldets, prev_pos, fps)

        infos = _yw_suspended_loads(ldets, pdets, ppm, gyf, vel_hist)
        fh = _yw_hazard_pairs(infos, pdets)

        if fh:
            haz_frames += 1

        hist.append(1 if fh else 0)
        h_eval = _yw_fill_gaps(list(hist), YW_MAX_NEG_GAP) if YW_GAP_FILL else list(hist)
        wpc = int(sum(h_eval))

        if not clip_unsafe and len(h_eval) == ws and wpc >= YW_K_THRESHOLD:
            clip_unsafe = True
            first_unsafe = total

    return {
        "total_frames": total,
        "fps": fps,
        "hazard_frames": haz_frames,
        "hazard_frame_pct": round(100.0 * haz_frames / max(total, 1), 1),
        "first_unsafe_frame": first_unsafe,
        "prediction": "UNSAFE" if clip_unsafe else "SAFE",
    }


# =========================================================
# GROUNDING DINO PIPELINE
# =========================================================

# --- Parameters (identical to previous Path A evaluation) ---
GD_MODEL_ID = "IDEA-Research/grounding-dino-base"
GD_MODEL_CACHE = Path("./models/cache")
GD_BOX_CONF = 0.3
GD_TEXT_THRESH = 0.25
GD_LL_BOX_CONF = 0.2
GD_LL_TEXT_THRESH = 0.15
GD_TARGET_PROMPT = "person . worker . construction worker"
GD_HAZARD_PROMPT = "chain hoist . concrete bucket . concrete skip . lifted container . hanging bucket . steel beam"
GD_SAMPLE_FPS = 1
GD_LOAD_MAX_HEIGHT = 0.35
GD_LOAD_MIN_AREA = 0.004
GD_LOAD_PROXIMITY = 0.40
GD_LOAD_MIN_SCORE = 0.30
GD_MIN_VIOL_FRAMES = 2
GD_VIOL_RATIO = 0.20


def _gd_extract_frames(path: Path, sample_fps: float = GD_SAMPLE_FPS) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open: {path}")
    vfps = cap.get(cv2.CAP_PROP_FPS)
    if vfps <= 0:
        cap.release()
        raise ValueError(f"Invalid FPS for: {path}")
    interval = max(1, int(round(vfps / sample_fps)))
    frames = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            frames.append(frame)
        idx += 1
    cap.release()
    return frames


class GDDetector:
    """Grounding DINO wrapper (HuggingFace, no CUDA compilation)."""

    def __init__(self, model_id=GD_MODEL_ID, device=None):
        import torch
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(
            model_id, cache_dir=str(GD_MODEL_CACHE))
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(
            model_id, cache_dir=str(GD_MODEL_CACHE)).to(self.device)
        self.model.eval()

    def detect(self, frame, text_prompt, box_threshold, text_threshold):
        import torch
        from PIL import Image

        image = Image.fromarray(frame[:, :, ::-1])
        h, w = frame.shape[:2]
        inputs = self.processor(images=image, text=text_prompt, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        results = self.processor.post_process_grounded_object_detection(
            outputs, inputs["input_ids"],
            threshold=box_threshold, text_threshold=text_threshold,
            target_sizes=[(h, w)],
        )[0]
        dets = []
        for box, score, label in zip(results["boxes"], results["scores"], results["text_labels"]):
            x1, y1, x2, y2 = box.cpu().tolist()
            dets.append({"box": [x1 / w, y1 / h, x2 / w, y2 / h],
                         "score": float(score.cpu()), "label": label})
        return dets


def _gd_check_lifted_load(targets, hazards):
    """5-stage spatial filter cascade, returns list of violations."""
    violations = []
    for h in hazards:
        if h.get("score", 1.0) < GD_LOAD_MIN_SCORE:
            continue
        hh = h["box"][3] - h["box"][1]
        hw = h["box"][2] - h["box"][0]
        if hh > GD_LOAD_MAX_HEIGHT:
            continue
        if hw * hh < GD_LOAD_MIN_AREA:
            continue
        h_bot_y = h["box"][3]
        hcx = (h["box"][0] + h["box"][2]) / 2
        hcy = (h["box"][1] + h["box"][3]) / 2
        for t in targets:
            t_top_y = t["box"][1]
            tcx = (t["box"][0] + t["box"][2]) / 2
            tcy = (t["box"][1] + t["box"][3]) / 2
            if h_bot_y > t_top_y:
                continue
            dist = math.hypot(tcx - hcx, tcy - hcy)
            if dist > GD_LOAD_PROXIMITY:
                continue
            violations.append(True)
    return violations


def _gd_aggregate(frame_violations: list[bool]) -> int:
    if not frame_violations:
        return 0
    count = sum(frame_violations)
    total = len(frame_violations)
    if count >= GD_MIN_VIOL_FRAMES or (count / total) >= GD_VIOL_RATIO:
        return 1
    return 0


def gd_classify_video(detector: GDDetector, video_path: Path) -> dict:
    """Run Grounding DINO pipeline on one video."""
    frames = _gd_extract_frames(video_path)
    frame_violations = []

    for frame in frames:
        targets = detector.detect(frame, GD_TARGET_PROMPT, GD_BOX_CONF, GD_TEXT_THRESH)
        hazards = detector.detect(frame, GD_HAZARD_PROMPT, GD_LL_BOX_CONF, GD_LL_TEXT_THRESH)
        viols = _gd_check_lifted_load(targets, hazards)
        frame_violations.append(len(viols) > 0)

    verdict = _gd_aggregate(frame_violations)
    viol_count = sum(frame_violations)
    return {
        "total_frames": len(frame_violations),
        "hazard_frames": viol_count,
        "hazard_frame_pct": round(100.0 * viol_count / max(len(frame_violations), 1), 1),
        "prediction": "UNSAFE" if verdict == 1 else "SAFE",
    }


# =========================================================
# RESULTS OUTPUT
# =========================================================

def write_per_video_csv(rows: list[dict], path: Path, model_name: str):
    fields = [
        "filename", "tier", "ground_truth", "prediction", "correct",
        "total_frames", "hazard_frames", "hazard_frame_pct",
    ]
    if model_name == "yolo_world":
        fields += ["fps", "first_unsafe_frame"]

    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  Per-video results: {path}")


def write_confusion_matrix(rows: list[dict], path: Path, model_name: str):
    """Write confusion matrix CSV: overall + per-tier."""
    all_sections = []

    def section(label, subset):
        yt = [1 if r["ground_truth"] == "UNSAFE" else 0 for r in subset]
        yp = [1 if r["prediction"] == "UNSAFE" else 0 for r in subset]
        m = compute_metrics(yt, yp)
        ci_lo, ci_hi = bootstrap_ci(yt, yp)
        return {**m, "label": label, "f2_ci_lo": ci_lo, "f2_ci_hi": ci_hi}

    all_sections.append(section("Overall", rows))
    tiers = sorted(set(r["tier"] for r in rows))
    for t in tiers:
        all_sections.append(section(f"Tier {t}", [r for r in rows if r["tier"] == t]))

    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([f"Suspended Load Hazard Detection — {model_name}"])
        w.writerow([])

        for sec in all_sections:
            w.writerow([sec["label"]])
            w.writerow(["", "Predicted UNSAFE", "Predicted SAFE"])
            w.writerow(["Actual UNSAFE", sec["tp"], sec["fn"]])
            w.writerow(["Actual SAFE", sec["fp"], sec["tn"]])
            w.writerow([])
            w.writerow(["Metric", "Value"])
            w.writerow(["Total videos", sec["n"]])
            w.writerow(["True Positives", sec["tp"]])
            w.writerow(["True Negatives", sec["tn"]])
            w.writerow(["False Positives", sec["fp"]])
            w.writerow(["False Negatives", sec["fn"]])
            w.writerow(["Precision", f"{sec['precision']:.4f}"])
            w.writerow(["Recall (Sensitivity)", f"{sec['recall']:.4f}"])
            w.writerow(["Specificity", f"{sec['specificity']:.4f}"])
            w.writerow(["F1 Score", f"{sec['f1']:.4f}"])
            w.writerow(["F2 Score", f"{sec['f2']:.4f}"])
            w.writerow(["F2 95% CI", f"[{sec['f2_ci_lo']:.4f}, {sec['f2_ci_hi']:.4f}]"])
            w.writerow([])

    print(f"  Confusion matrix: {path}")


def print_summary(rows: list[dict], model_name: str):
    yt = [1 if r["ground_truth"] == "UNSAFE" else 0 for r in rows]
    yp = [1 if r["prediction"] == "UNSAFE" else 0 for r in rows]
    m = compute_metrics(yt, yp)
    ci_lo, ci_hi = bootstrap_ci(yt, yp)

    print(f"\n{'='*55}")
    print(f"  {model_name} — OVERALL ({m['n']} videos)")
    print(f"{'='*55}")
    print(f"                  Pred UNSAFE   Pred SAFE")
    print(f"  Actual UNSAFE       {m['tp']:>3}           {m['fn']:>3}")
    print(f"  Actual SAFE         {m['fp']:>3}           {m['tn']:>3}")
    print(f"{'='*55}")
    print(f"  Precision:    {m['precision']:.4f}")
    print(f"  Recall:       {m['recall']:.4f}")
    print(f"  Specificity:  {m['specificity']:.4f}")
    print(f"  F1 Score:     {m['f1']:.4f}")
    print(f"  F2 Score:     {m['f2']:.4f}  [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"{'='*55}")

    tiers = sorted(set(r["tier"] for r in rows))
    for t in tiers:
        sub = [r for r in rows if r["tier"] == t]
        syt = [1 if r["ground_truth"] == "UNSAFE" else 0 for r in sub]
        syp = [1 if r["prediction"] == "UNSAFE" else 0 for r in sub]
        sm = compute_metrics(syt, syp)
        sci_lo, sci_hi = bootstrap_ci(syt, syp)
        print(f"\n  Tier {t} ({sm['n']} videos): "
              f"F2={sm['f2']:.3f} [{sci_lo:.3f}, {sci_hi:.3f}]  "
              f"P={sm['precision']:.3f}  R={sm['recall']:.3f}  "
              f"TP={sm['tp']} FP={sm['fp']} FN={sm['fn']} TN={sm['tn']}")


# =========================================================
# MAIN
# =========================================================

def run_yolo_world(entries: list[dict], annotate: bool = False):
    from ultralytics import YOLOWorld

    print("\n" + "=" * 60)
    print("  YOLO WORLD EVALUATION")
    print("=" * 60)

    model = YOLOWorld(YW_MODEL_NAME)
    model.set_classes(YW_CUSTOM_CLASSES)
    person_cid = YW_CUSTOM_CLASSES.index(YW_PERSON_CLASS)
    load_cid = YW_CUSTOM_CLASSES.index(YW_LOAD_CLASS)

    rows = []
    for entry in tqdm(entries, desc="YOLO World"):
        vpath = VIDEOS_DIR / entry["filename"]
        if not vpath.exists():
            tqdm.write(f"  SKIP (not found): {entry['filename']}")
            continue

        info = yw_classify_video(model, vpath, person_cid, load_cid)
        correct = info["prediction"] == entry["ground_truth"]
        row = {
            "filename": entry["filename"],
            "tier": entry["tier"],
            "ground_truth": entry["ground_truth"],
            "prediction": info["prediction"],
            "correct": correct,
            "total_frames": info["total_frames"],
            "fps": info["fps"],
            "hazard_frames": info["hazard_frames"],
            "hazard_frame_pct": info["hazard_frame_pct"],
            "first_unsafe_frame": info["first_unsafe_frame"] or "",
        }
        rows.append(row)
        status = "OK" if correct else "WRONG"
        tqdm.write(f"  [{status}] {entry['filename']}: "
                   f"GT={entry['ground_truth']} PRED={info['prediction']} "
                   f"haz={info['hazard_frame_pct']:.1f}%")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    write_per_video_csv(rows, OUTPUT_DIR / f"results_yolo_world_{timestamp}.csv", "yolo_world")
    write_confusion_matrix(rows, OUTPUT_DIR / f"confusion_matrix_yolo_world_{timestamp}.csv", "YOLO World")
    print_summary(rows, "YOLO World")
    return rows


def run_grounding_dino(entries: list[dict]):
    print("\n" + "=" * 60)
    print("  GROUNDING DINO EVALUATION")
    print("=" * 60)

    detector = GDDetector()

    rows = []
    for entry in tqdm(entries, desc="Grounding DINO"):
        vpath = VIDEOS_DIR / entry["filename"]
        if not vpath.exists():
            tqdm.write(f"  SKIP (not found): {entry['filename']}")
            continue

        info = gd_classify_video(detector, vpath)
        correct = info["prediction"] == entry["ground_truth"]
        row = {
            "filename": entry["filename"],
            "tier": entry["tier"],
            "ground_truth": entry["ground_truth"],
            "prediction": info["prediction"],
            "correct": correct,
            "total_frames": info["total_frames"],
            "hazard_frames": info["hazard_frames"],
            "hazard_frame_pct": info["hazard_frame_pct"],
        }
        rows.append(row)
        status = "OK" if correct else "WRONG"
        tqdm.write(f"  [{status}] {entry['filename']}: "
                   f"GT={entry['ground_truth']} PRED={info['prediction']} "
                   f"haz={info['hazard_frame_pct']:.1f}%")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    write_per_video_csv(rows, OUTPUT_DIR / f"results_grounding_dino_{timestamp}.csv", "grounding_dino")
    write_confusion_matrix(rows, OUTPUT_DIR / f"confusion_matrix_grounding_dino_{timestamp}.csv", "Grounding DINO")
    print_summary(rows, "Grounding DINO")
    return rows


def main():
    parser = argparse.ArgumentParser(description="Evaluate hazard detection on ACM MM 2026 dataset")
    parser.add_argument("--model", choices=["yolo_world", "grounding_dino", "both"],
                        default="both", help="Which model(s) to evaluate")
    parser.add_argument("--annotate", action="store_true",
                        help="Also produce annotated output videos (YOLO World only)")
    args = parser.parse_args()

    entries = load_labels()
    print(f"Loaded {len(entries)} video entries from {LABELS_CSV}")
    n_unsafe = sum(1 for e in entries if e["ground_truth"] == "UNSAFE")
    n_safe = sum(1 for e in entries if e["ground_truth"] == "SAFE")
    print(f"  UNSAFE (True Positive): {n_unsafe}")
    print(f"  SAFE (False Positive):  {n_safe}")

    if args.model in ("yolo_world", "both"):
        run_yolo_world(entries, annotate=args.annotate)

    if args.model in ("grounding_dino", "both"):
        run_grounding_dino(entries)


if __name__ == "__main__":
    main()
