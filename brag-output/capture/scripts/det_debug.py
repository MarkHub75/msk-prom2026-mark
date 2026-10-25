"""Debug sheet: detections drawn over frames of a private clip (boxes, ids, kind). usage: det_debug.py clip t1 t2 ... out.jpg"""
import json
import pathlib
import sys

import cv2
import numpy as np

PRIVATE = pathlib.Path(__file__).resolve().parents[2] / "composition" / "assets" / "private"
clip, times, out = sys.argv[1], [float(t) for t in sys.argv[2:-1]], sys.argv[-1]
det = json.loads((PRIVATE / f"{clip}.det.json").read_text(encoding="utf-8"))
cap = cv2.VideoCapture(str(PRIVATE / f"{clip}.mp4"))
tiles = []
for t in times:
    i = int(round(t * 30))
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ok, img = cap.read()
    h, w = img.shape[:2]
    for o in det["frames"][min(i, len(det["frames"]) - 1)]["objs"]:
        x1, y1, x2, y2 = [int(v * (w if k % 2 == 0 else h)) for k, v in enumerate(o["box"])]
        col = (60, 60, 230) if o["kind"] == "train" else (240, 240, 240)
        cv2.rectangle(img, (x1, y1), (x2, y2), col, 2)
        cv2.putText(img, f'{o["kind"][0]}{o["id"]} {o["conf"]}', (x1, max(12, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)
        if o["kp"]:
            for x, y, s in o["kp"]:
                if s > 0.3:
                    cv2.circle(img, (int(x * w), int(y * h)), 2, (0, 200, 255), -1)
    cv2.putText(img, f"{clip} t={t}", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    tiles.append(cv2.resize(img, (640, 360)))
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
cv2.imwrite(out, np.vstack(rows))
