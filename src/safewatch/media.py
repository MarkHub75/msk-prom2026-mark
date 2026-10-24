"""Video files through OpenCV (tech.md 7): blocking, called from `services` via `to_thread`."""

from pathlib import Path

import cv2
from pydantic import BaseModel

BROWSER_CODECS = ("avc1", "h264", "vp09", "av01")


class VideoProbe(BaseModel):
    width: int
    height: int
    fps: float
    frame_count: int
    duration_ms: int
    codec: str  # FourCC in lower case
    browser_playable: bool


def probe_video(path: Path) -> VideoProbe | None:
    """Metadata of a readable video; `None` when OpenCV cannot open it or read a frame."""
    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            return None
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if fps <= 0 or frame_count <= 0:
            return None
        ok, _ = cap.read()
        if not ok:
            return None
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join(chr((fourcc >> (8 * i)) & 0xFF) for i in range(4)).strip("\x00 ").lower()
        return VideoProbe(
            width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            fps=fps,
            frame_count=frame_count,
            duration_ms=round(frame_count * 1000 / fps),
            codec=codec,
            browser_playable=codec in BROWSER_CODECS,
        )
    finally:
        cap.release()
