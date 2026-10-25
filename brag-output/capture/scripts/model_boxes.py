"""Reads the boxes the extra models drew (yellow helmet box, green smoke box) from the «readable» clips,
frame by frame, in the coordinates of the promo crop, so the Russian plates can sit exactly on them.
Writes composition/assets/private/model-boxes.js → window.MODEL_BOXES = {helmet: [[t, x1, y1, x2, y2]|[t]], smoke: …}
(normalised to the crop; [t] = no box in that frame)."""
import json
import pathlib

import cv2
import numpy as np

HAC = pathlib.Path(r"C:\Users\User\Desktop\hac trash")
PRIVATE = pathlib.Path(__file__).resolve().parents[2] / "composition" / "assets" / "private"
JOBS = {
    # name: (file, start s, dur s, crop x, y, w, h, hsv lower, hsv upper)
    "helmet": ("Helmet_pretrained_readable.mp4", 1.5, 2.4, 208, 77, 344, 405, (15, 120, 120), (40, 255, 255)),
    "smoke": ("Smoke_positive_readable.mp4", 1.9, 2.4, 218, 77, 344, 405, (45, 150, 120), (75, 255, 255)),
}
out = {}
for name, (f, start, dur, cx, cy, cw, ch, lo, hi) in JOBS.items():
    cap = cv2.VideoCapture(str(HAC / f))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    rows = []
    t = 0.0
    while t < dur:
        ok, img = cap.read()
        if not ok:
            break
        crop = img[cy:cy + ch, cx:cx + cw]
        mask = cv2.inRange(cv2.cvtColor(crop, cv2.COLOR_BGR2HSV), np.array(lo), np.array(hi))
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # the box outline: the biggest roughly rectangular contour (label text is small and thin)
        # a drawn box is a hollow outline: little of its rectangle is filled (solid yellow objects are not)
        best = None
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            fill = cv2.countNonZero(mask[y:y + h, x:x + w]) / float(w * h)
            # helmet: the head box near the person in the aisle, not the yellow machine frame at the left edge
            if name == "helmet" and not (0.3 * cw < x < 0.8 * cw and w < 60 and h < 60):
                continue
            if w >= 10 and h >= 10 and fill < 0.45 and (best is None or w * h > best[2] * best[3]):
                best = (x, y, w, h)
        if best:
            x, y, w, h = best
            rows.append([round(t, 3), round(x / cw, 4), round(y / ch, 4), round((x + w) / cw, 4), round((y + h) / ch, 4)])
        else:
            rows.append([round(t, 3)])
        t += 1 / fps
    out[name] = rows
    seen = [r for r in rows if len(r) > 1]
    print(name, f"fps {fps:.2f}", len(rows), "frames,", len(seen), "with a box; first", seen[0] if seen else None, "last", seen[-1] if seen else None)
(PRIVATE / "model-boxes.js").write_text("window.MODEL_BOXES = " + json.dumps(out) + ";\n", encoding="utf-8")
