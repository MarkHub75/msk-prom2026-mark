"""Video files through OpenCV (tech.md 7): blocking, called from `services` via `to_thread`."""

import logging
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from pydantic import BaseModel

from safewatch.config import TranscodeConfig

log = logging.getLogger(__name__)

BROWSER_CODECS = ("avc1", "h264", "vp09", "av01")
# OpenCV reports FFmpeg codec names for some streams; the file itself is tagged otherwise.
CODEC_ALIASES = {"fmp4": "mp4v"}
WEB_SUFFIX = ".web.mp4"


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
        codec = CODEC_ALIASES.get(codec, codec)
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


def transcode(src: Path, dst: Path, cfg: TranscodeConfig) -> bool:
    """H.264 copy of `src` for the browser (tech.md 8.20); `False` and no `dst` on any failure."""
    # ffmpeg writes beside `dst`: a killed run never leaves a half file under the final name.
    part = dst.with_name(dst.name + ".part")
    try:
        cmd = [
            imageio_ffmpeg.get_ffmpeg_exe(),
            *("-y", "-v", "error", "-i", str(src)),
            *("-c:v", "libx264", "-preset", cfg.preset, "-crf", str(cfg.crf)),
            *("-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", "-f", "mp4", str(part)),
        ]
        done = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=cfg.timeout_s,
            check=False,
        )
        if done.returncode != 0:
            log.warning("transcode: ffmpeg exit %s on %s", done.returncode, src.name)
            return False
        probe = probe_video(part)
        if probe is None or probe.codec not in BROWSER_CODECS:
            log.warning("transcode: the copy of %s does not play in a browser", src.name)
            return False
        part.replace(dst)
        return True
    except subprocess.TimeoutExpired:
        log.warning("transcode: timeout %s s on %s", cfg.timeout_s, src.name)
        return False
    except (OSError, RuntimeError) as exc:  # RuntimeError: imageio-ffmpeg found no ffmpeg
        log.warning("transcode: %s", exc)
        return False
    finally:
        part.unlink(missing_ok=True)


def read_frame(path: Path, frame_idx: int) -> np.ndarray:
    """BGR frame `frame_idx` of the video."""
    cap = cv2.VideoCapture(str(path))
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, img = cap.read()
    finally:
        cap.release()
    if not ok:
        raise ValueError(f"frame {frame_idx} of {path.name} is not readable")
    frame: np.ndarray = img
    return frame


def encode_jpeg(img: np.ndarray, quality: int, max_width: int) -> bytes:
    """JPEG of `img`, scaled down to `max_width` keeping the aspect ratio."""
    h, w = img.shape[:2]
    if w > max_width:
        img = cv2.resize(img, (max_width, round(h * max_width / w)), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return bytes(buf.tobytes())


LUMA_WIDTH = 160  # brightness statistics need no detail; a small frame is cheap to read


def sample_luma(path: Path, every_s: float) -> list[tuple[int, float, float]]:
    """`(ts_ms, mean, std)` of a grey, downscaled frame every `every_s`; `[]` if unreadable."""
    cap = cv2.VideoCapture(str(path))
    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS)) if cap.isOpened() else 0.0
        if fps <= 0:
            return []
        step, idx, out = max(1, round(every_s * fps)), 0, []
        while cap.grab():
            if idx % step == 0:
                ok, img = cap.retrieve()
                if ok:
                    h, w = img.shape[:2]
                    size = (LUMA_WIDTH, max(1, round(h * LUMA_WIDTH / w)))
                    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Nearest keeps the spread of pixels; averaging would flatten texture and noise.
                    grey = cv2.resize(grey, size, interpolation=cv2.INTER_NEAREST)
                    out.append((round(idx * 1000 / fps), float(grey.mean()), float(grey.std())))
            idx += 1
        return out
    finally:
        cap.release()
