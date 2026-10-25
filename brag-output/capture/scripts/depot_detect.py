"""People (pose) and rolling stock detections with ByteTrack tracks for the depot clips.

Runs YOLOv8m-pose (people + 17 keypoints) and YOLOv8m (COCO class «train») on a local GPU.
These are NOT LinQ detections: the promo never labels the depot overlays as LinQ.
Output: composition/assets/private/<clip>.det.json — kept out of git with the clips themselves.

usage: py -3.12 depot_detect.py d-hero d-loco ...
"""
import json
import pathlib
import sys

from ultralytics import YOLO

PRIVATE = pathlib.Path(__file__).resolve().parents[2] / "composition" / "assets" / "private"


def run(name: str, pose_w: str = "yolov8m-pose.pt", size: int = 960, conf: float = 0.25) -> None:
    src = PRIVATE / f"{name}.mp4"
    pose = YOLO(pose_w)
    det = YOLO("yolov8m.pt")
    people = pose.track(str(src), stream=True, persist=True, tracker="bytetrack.yaml", conf=conf, imgsz=size, verbose=False, device=0)
    trains = det.track(str(src), stream=True, persist=True, tracker="bytetrack.yaml", conf=0.3, imgsz=960, classes=[6], verbose=False, device=0)
    frames = []
    for i, (rp, rt) in enumerate(zip(people, trains)):
        h, w = rp.orig_shape
        objs = []
        if rp.boxes is not None and rp.boxes.id is not None:
            kp = rp.keypoints.data.cpu().numpy() if rp.keypoints is not None else None
            for j, (b, tid, c) in enumerate(zip(rp.boxes.xyxy.cpu().numpy(), rp.boxes.id.int().cpu().numpy(), rp.boxes.conf.cpu().numpy())):
                k = [[round(float(x) / w, 4), round(float(y) / h, 4), round(float(s), 2)] for x, y, s in kp[j]] if kp is not None else None
                objs.append({"id": int(tid), "kind": "person", "conf": round(float(c), 2),
                             "box": [round(float(b[0]) / w, 4), round(float(b[1]) / h, 4), round(float(b[2]) / w, 4), round(float(b[3]) / h, 4)], "kp": k})
        if rt.boxes is not None and rt.boxes.id is not None:
            for b, tid, c in zip(rt.boxes.xyxy.cpu().numpy(), rt.boxes.id.int().cpu().numpy(), rt.boxes.conf.cpu().numpy()):
                objs.append({"id": 1000 + int(tid), "kind": "train", "conf": round(float(c), 2),
                             "box": [round(float(b[0]) / w, 4), round(float(b[1]) / h, 4), round(float(b[2]) / w, 4), round(float(b[3]) / h, 4)], "kp": None})
        frames.append({"i": i, "t": round(i / 30, 4), "objs": objs})
    out = PRIVATE / f"{name}.det.json"
    out.write_text(json.dumps({"clip": name, "fps": 30, "w": w, "h": h, "frames": frames}, ensure_ascii=False), encoding="utf-8")
    n_people = len({o["id"] for f in frames for o in f["objs"] if o["kind"] == "person"})
    n_trains = len({o["id"] for f in frames for o in f["objs"] if o["kind"] == "train"})
    print(name, len(frames), "frames;", n_people, "person tracks;", n_trains, "train tracks")


if __name__ == "__main__":
    # «big» clips: small people far from the camera need the x-model and a 1920 input
    for clip in sys.argv[1:]:
        name, _, mode = clip.partition(":")
        if mode == "big":
            run(name, "yolov8x-pose.pt", 1920, 0.15)
        else:
            run(name)
