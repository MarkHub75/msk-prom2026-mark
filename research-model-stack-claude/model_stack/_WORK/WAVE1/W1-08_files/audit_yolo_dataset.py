#!/usr/bin/env python3
"""W1-08 pre-training audit of an Ultralytics-style YOLO detection dataset (research tool, NOT hackathon-developed code).

Pure PyYAML + Pillow + numpy; does not import ultralytics; does not execute anything from the dataset
(the data.yaml `download:` key is only reported, never exec'd).
Mirrors (by code reading, ultralytics v8.4.184) what verify_image_label/check_det_dataset silently drop or accept,
and adds checks Ultralytics does NOT do: train/val leakage by content hash, class-order mismatch across yamls,
tiny boxes after resize, EXIF/alpha/gray images, images/ -> labels/ pairing.

Usage: python -I audit_yolo_dataset.py DATA.yaml [--imgsz 640] [--min-px 4] [--compare OTHER.yaml] [--json out.json]
"""
import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import yaml
from PIL import Image

IMG = {"bmp", "dng", "jpeg", "jpg", "mpo", "png", "tif", "tiff", "webp", "pfm", "heic", "avif"}
findings = []  # (severity, code, message)


def F(sev, code, msg):
    findings.append((sev, code, msg))


def load_names(y):
    n = y.get("names")
    if n is None:
        F("ERROR", "NAMES_MISSING", "names missing")
        return {}
    d = dict(enumerate(n)) if isinstance(n, list) else dict(n)
    out = {}
    for k, v in d.items():
        if not isinstance(v, str):
            F("ERROR", "NAME_NOT_STR", f"class {k}: YAML parsed name as {type(v).__name__} {v!r} (YAML 1.1 bool/null/number); "
                                       f"Ultralytics str()s it -> {str(v)!r}. Quote it in the yaml")
        out[int(k)] = str(v)
    if sorted(out) != list(range(len(out))):
        F("ERROR", "NAMES_KEYS", f"names keys not contiguous 0..n-1: {sorted(out)}")
    low = Counter(v.strip().lower() for v in out.values())
    for v, c in low.items():
        if c > 1:
            F("WARN", "NAME_DUP", f"duplicate class name (case/space-insensitive): {v!r} x{c}")
    if "nc" in y and y["nc"] != len(out):
        F("ERROR", "NC_MISMATCH", f"nc={y['nc']} != len(names)={len(out)}")
    return out


def split_dirs(y, root, key):
    v = y.get(key)
    if not v:
        return []
    out = []
    for x in (v if isinstance(v, list) else [v]):
        p = (root / x).resolve()
        if not p.exists() and str(x).startswith("../"):
            p = (root / str(x)[3:]).resolve()  # same fallback as check_det_dataset
        out.append(p)
    return out


def img2label(p):  # same rule as ultralytics img2label_paths
    sa, sb = f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}"
    return sb.join(os.fspath(p).rsplit(sa, 1)).rsplit(".", 1)[0] + ".txt"


def audit_split(name, paths, nc, imgsz, min_px, stats):
    files = []
    for p in paths:
        if p.is_dir():
            files += [f for f in p.rglob("*") if f.is_file() and f.suffix[1:].lower() in IMG]
        elif p.is_file():
            files += [Path(line.strip()) for line in p.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        else:
            F("ERROR", "SPLIT_PATH", f"{name}: path not found {p}")
    files = sorted(files)
    if not files:
        F("ERROR", "NO_IMAGES", f"{name}: no images")
        return
    miss = empty = corrupt = tiny = oob = dups = 0
    cls_cnt = Counter()
    hashes = {}
    for f in files:
        try:
            with Image.open(f) as im:
                im.verify()
            with Image.open(f) as im:
                w, h = im.size
                mode = im.mode
                ori = im.getexif().get(274, 1)
        except Exception as e:
            corrupt += 1
            F("ERROR", "IMG_CORRUPT", f"{f}: {e}")
            continue
        if ori in (5, 6, 7, 8):
            F("WARN", "EXIF_ROTATED", f"{f}: EXIF orientation {ori}: Ultralytics trains on the ROTATED image "
                                      f"(cv2.imdecode applies EXIF); labels must be in the rotated frame")
            w, h = h, w
        if mode in ("RGBA", "LA", "P"):
            F("WARN", "IMG_MODE", f"{f}: mode {mode} (alpha/palette dropped/converted by cv2 IMREAD_COLOR)")
        if mode in ("L", "I;16", "I"):
            F("INFO", "IMG_GRAY", f"{f}: mode {mode} (loaded as 3-channel by default)")
        hashes.setdefault(hashlib.sha1(f.read_bytes()).hexdigest(), []).append(str(f))
        if "images" not in Path(f).parts:
            F("ERROR", "NO_IMAGES_DIR", f"{f}: path has no 'images' component, label path cannot be derived")
            miss += 1
            continue
        lf = img2label(f)
        if not os.path.isfile(lf):
            miss += 1
            continue
        rows = [ln.split() for ln in Path(lf).read_text(encoding="utf-8-sig").splitlines() if ln.strip()]
        if not rows:
            empty += 1
            continue
        seen = set()
        for r in rows:
            try:
                if len(r) == 5:
                    c, x, y_, bw, bh = map(float, r)
                    poly = False
                elif len(r) > 6 and len(r) % 2 == 1:
                    v = list(map(float, r))
                    c = v[0]
                    xs, ys = np.array(v[1::2]), np.array(v[2::2])
                    x, y_ = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
                    bw, bh = xs.max() - xs.min(), ys.max() - ys.min()
                    poly = True
                else:
                    raise ValueError(f"{len(r)} columns")
            except Exception as e:
                F("ERROR", "LABEL_PARSE", f"{lf}: {e} in row {' '.join(r)[:60]!r} (Ultralytics would DROP THE WHOLE IMAGE)")
                break
            if c != int(c) or c < 0 or c >= nc:
                F("ERROR", "CLASS_RANGE", f"{lf}: class {c} outside 0..{nc - 1} (Ultralytics drops the whole image)")
                continue
            if not poly and (max(x, y_, bw, bh) > 1.01 or min(x, y_, bw, bh) < -0.01):
                F("ERROR", "COORD_RANGE", f"{lf}: not normalized/out of range {r[1:5]}")
            if bw <= 0 or bh <= 0:
                F("ERROR", "BOX_NONPOS", f"{lf}: non-positive box size {r[3:5]}")
                continue
            if x - bw / 2 < -0.01 or x + bw / 2 > 1.01 or y_ - bh / 2 < -0.01 or y_ + bh / 2 > 1.01:
                oob += 1
            s = imgsz / max(w, h)  # long side -> imgsz (Ultralytics load_image rect_mode)
            if min(bw * w * s, bh * h * s) < min_px:
                tiny += 1
            key = tuple(r)
            if key in seen:
                dups += 1
            seen.add(key)
            cls_cnt[int(c)] += 1
    n = len(files)
    print(f"[{name}] images={n} label_missing(bg)={miss} label_empty(bg)={empty} corrupt={corrupt} "
          f"boxes={sum(cls_cnt.values())} tiny(<{min_px}px@{imgsz})={tiny} box_out_of_image={oob} exact_dup_rows={dups}")
    if miss / n > 0.5:
        F("ERROR" if miss == n else "WARN", "MOST_BG",
          f"{name}: {miss}/{n} images without label file (silent background). Check images/ -> labels/ layout")
    for cid in range(nc):
        if cls_cnt[cid] == 0:
            F("WARN", "CLASS_EMPTY", f"{name}: class {cid} has 0 instances")
    d = {h: v for h, v in hashes.items() if len(v) > 1}
    if d:
        F("WARN", "DUP_IMAGES_IN_SPLIT", f"{name}: {len(d)} byte-identical image groups")
    stats[name] = {"hashes": hashes, "cls": cls_cnt}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("yaml")
    a.add_argument("--imgsz", type=int, default=640)
    a.add_argument("--min-px", type=float, default=4)
    a.add_argument("--compare")
    a.add_argument("--json")
    o = a.parse_args()
    yp = Path(o.yaml).resolve()
    y = yaml.safe_load(yp.read_text(encoding="utf-8"))
    if "download" in y:
        F("WARN", "DOWNLOAD_KEY", "data.yaml has `download:` -> Ultralytics exec()s it as Python if the val path is missing. "
                                  "Remove it for untrusted yamls")
    names = load_names(y)
    nc = len(names)
    root = Path(y.get("path") or yp.parent)  # ultralytics: extract_dir or data["path"] or yaml_file.parent
    if not root.is_absolute():
        F("WARN", "PATH_RELATIVE", f"data.yaml `path: {root}` is relative: Ultralytics resolves it against the CWD "
                                   f"(if it exists) and otherwise against its DATASETS_DIR setting, NOT against the yaml folder")
        if not root.exists():
            root = (yp.parent / root).resolve()  # audit convenience only
    stats = {}
    for k in ("train", "val", "test"):
        ps = split_dirs(y, root, k)
        if ps:
            audit_split(k, ps, nc, o.imgsz, o.min_px, stats)
        elif k != "test":
            F("ERROR", "SPLIT_MISSING", f"{k} missing")
    if "train" in stats and "val" in stats:  # leakage check by content hash
        ht, hv = set(stats["train"]["hashes"]), set(stats["val"]["hashes"])
        if ht & hv:
            F("ERROR", "LEAK_TRAIN_VAL", f"{len(ht & hv)} byte-identical images in both train and val")
    if o.compare:
        other = load_names(yaml.safe_load(Path(o.compare).read_text(encoding="utf-8")))
        if other != names:
            F("ERROR", "ORDER_MISMATCH", f"names differ between yamls:\n  {names}\n  {other}\n  -> merging label files "
                                         f"without remap silently relabels classes")
    if "train" in stats and nc:
        c = stats["train"]["cls"]
        print("train class histogram:", {names.get(i, i): c[i] for i in range(nc)})
    for sev, code, msg in findings:
        print(f"{sev:5s} {code}: {msg}")
    ne = sum(1 for s, _, _ in findings if s == "ERROR")
    nw = sum(1 for s, _, _ in findings if s == "WARN")
    print(f"SUMMARY: {ne} errors, {nw} warnings")
    if o.json:
        Path(o.json).write_text(json.dumps(findings, indent=1), encoding="utf-8")
    sys.exit(1 if ne else 0)


main()
