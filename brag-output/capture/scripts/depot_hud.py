"""Turns <clip>.det.json into a HUD script for the composition: smoothed boxes, Russian labels, rule levels.

Rules (the same kinds АРГУС uses; computed here from the depot detections, not by LinQ):
- «поезд движется»: over 2 s the rolling-stock box centre moves > 2 % of the frame or its height changes > 4 %, held 1.5 s;
- proximity: a person next to a moving train, horizontal gap < GAP_RED person heights for ≥ 0.3 s → red,
  label «до поезда 0,3 роста» (АРГУС reports approach in person heights: «Сближение с грузовиком: 0,4 роста»);
- zone: a person whose foot point stays inside the clip's danger zone for ≥ DWELL s → red «в опасной зоне N с».
Posture: «присел» (knees near hips), else «идёт» (foot point moves > 0.25 heights/s), else «стоит».
Output: composition/assets/private/<clip>.hud.js → window.HUD["<clip>"] = {fps, zone, frames: [[t, [obj…]]]}
obj = [id, kind, x1, y1, x2, y2, level, label, kp|null]   (level: "" | "amber" | "red")
"""
import json
import pathlib
import sys

PRIVATE = pathlib.Path(__file__).resolve().parents[2] / "composition" / "assets" / "private"
GAP_RED, DWELL, CONFIRM = 0.6, 1.0, 0.3

# danger zones per clip, normalised polygon (x, y); None = no zone rule on this clip
ZONES = {
    "d-hero": {"name": "Путь перед локомотивом", "poly": [[0.60, 0.66], [0.93, 0.62], [1.0, 0.78], [1.0, 1.0], [0.66, 1.0]]},
}
MIN_CONF = {"person": 0.35, "train": 0.4}
# clips where the locomotive really moves (checked by eye); in the others it is parked and box jitter must not read as motion
MOVING_TRAIN_CLIPS = {"d-dark", "d-loco"}


def inside(p, poly):
    x, y, c = p[0], p[1], False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1:
            c = not c
    return c


def ru(v):
    return f"{v:.1f}".replace(".", ",")


def process(name):
    det = json.loads((PRIVATE / f"{name}.det.json").read_text(encoding="utf-8"))
    fps = det["fps"]
    zone = ZONES.get(name)
    # tracks: id -> list of (frame index, obj)
    tracks = {}
    for f in det["frames"]:
        for o in f["objs"]:
            b = o["box"]
            if o["conf"] < MIN_CONF[o["kind"]] or (b[3] - b[1]) < 0.03:
                continue
            if o["kind"] == "person" and b[2] < 0.06:   # dark wall at the left edge (false person)
                continue
            tracks.setdefault(o["id"], []).append((f["i"], o))
    n = len(det["frames"])
    state = {}   # (frame, id) -> obj row
    for tid, seq in tracks.items():
        if len(seq) < int(0.4 * fps):   # flickers shorter than 0.4 s are dropped
            continue
        # EMA-smoothed boxes; a lost track up to 0.8 s is bridged by linear interpolation (ByteTrack itself keeps lost tracks ~1 s)
        sm, last_i = None, None
        filled = []
        for i, o in seq:
            b = o["box"]
            sm = b if sm is None else [0.6 * a + 0.4 * c for a, c in zip(sm, b)]
            if last_i is not None and 1 < i - last_i <= int(0.8 * fps):
                pb, po = filled[-1][1], filled[-1][2]
                for k in range(last_i + 1, i):
                    w = (k - last_i) / (i - last_i)
                    filled.append((k, [x + (y - x) * w for x, y in zip(pb, sm)], po))
            filled.append((i, list(sm), o))
            last_i = i
        for i, b, o in filled:
            state[(i, tid)] = {"kind": o["kind"], "box": b, "kp": o["kp"]}
    # per-frame derived values
    def at(i, tid):
        return state.get((i, tid))

    half = int(0.5 * fps)
    out = []
    dwell, near, moving_until = {}, {}, {}
    for i in range(n):
        ids = [tid for (k, tid) in state if k == i]
        trains = []
        for tid in ids:
            s = at(i, tid)
            if s["kind"] != "train":
                continue
            p = at(max(0, i - 2 * fps), tid) or s
            b, pb = s["box"], p["box"]
            dc = abs((b[0] + b[2]) / 2 - (pb[0] + pb[2]) / 2) + abs((b[1] + b[3]) / 2 - (pb[1] + pb[3]) / 2)
            dh = abs((b[3] - b[1]) - (pb[3] - pb[1])) / max(1e-6, (b[3] - b[1]))
            if name in MOVING_TRAIN_CLIPS and (dc > 0.02 or dh > 0.04):
                moving_until[tid] = i + int(1.5 * fps)
            moving = i <= moving_until.get(tid, -1)
            trains.append((tid, b, moving))
        objs = []
        for tid, b, moving in trains:
            objs.append([tid, "train", *[round(v, 4) for v in b], "amber" if moving else "", "поезд · движется" if moving else "поезд · стоит", None])
        for tid in ids:
            s = at(i, tid)
            if s["kind"] != "person":
                continue
            b = s["box"]
            h = b[3] - b[1]
            foot = ((b[0] + b[2]) / 2, b[3])
            p = at(max(0, i - half), tid) or s
            pf = ((p["box"][0] + p["box"][2]) / 2, p["box"][3])
            speed = (abs(foot[0] - pf[0]) + abs(foot[1] - pf[1])) / max(1e-6, h) / 0.5
            posture = "идёт" if speed > 0.25 else "стоит"
            kp = s["kp"]
            if kp:
                hips = [kp[11], kp[12]]
                knees = [kp[13], kp[14]]
                if all(k[2] > 0.3 for k in hips + knees):
                    hip_y = (hips[0][1] + hips[1][1]) / 2
                    knee_y = (knees[0][1] + knees[1][1]) / 2
                    if knee_y - hip_y < 0.12 * h:
                        posture = "присел"
            level, label = "", f"человек · {posture}"
            # proximity to a moving train
            gaps = []
            for _, tb, mv in trains:
                if mv:
                    gap = max(0.0, tb[0] - b[2], b[0] - tb[2]) / max(1e-6, h)
                    gaps.append(gap)
            if gaps and min(gaps) < GAP_RED:
                near[tid] = near.get(tid, 0) + 1
                g = min(gaps)
                label = "вплотную к поезду" if g < 0.05 else f"до поезда {ru(g)} роста"
                level = "red" if near[tid] >= CONFIRM * fps else "amber"
            else:
                near[tid] = 0
            # dwell in the danger zone
            if zone and inside(foot, zone["poly"]):
                dwell[tid] = dwell.get(tid, 0) + 1
                sec = dwell[tid] / fps
                if level != "red":
                    level = "red" if sec >= DWELL else "amber"
                    label = f"в опасной зоне {ru(sec)} с"
            else:
                dwell[tid] = 0
            kpr = [[round(x, 3), round(y, 3), round(c, 2)] for x, y, c in kp] if kp else None
            objs.append([tid, "person", *[round(v, 4) for v in b], level, label, kpr])
        out.append([round(i / fps, 4), objs])
    data = {"fps": fps, "zone": zone, "frames": out}
    (PRIVATE / f"{name}.hud.js").write_text(
        "window.HUD = window.HUD || {};\nwindow.HUD[" + json.dumps(name) + "] = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")
    # a short report: when each person turns amber / red, and train motion
    first = {}
    for t, objs in out:
        for o in objs:
            key = (o[0], o[6])
            if o[6] and key not in first:
                first[key] = (t, o[7])
    print(name, {f"{k[0]}:{k[1]}": v for k, v in sorted(first.items(), key=lambda kv: kv[1][0])})


if __name__ == "__main__":
    for clip in sys.argv[1:]:
        process(clip)
