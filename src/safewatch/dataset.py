"""False alarm dataset files (tech.md 8.26): `datasets/false_alarms/<event_id>/` and the zip.

Blocking file work for `services` (in `asyncio.to_thread`) and the CLI; the database stays out.
"""

import json
import shutil
import zipfile
from pathlib import Path

from safewatch import config, media
from safewatch.types import DatasetItem, Episode, EventSummary

MANIFEST = "manifest.json"


def item_path(event_id: int) -> str:
    """Folder of the event's item, from `data_dir` (column `dataset_items.path`)."""
    return f"datasets/false_alarms/{event_id}/"


def _lines(path: Path, frames: set[int]) -> str:
    """Lines of a JSONL file whose `frame_idx` is one of `frames`, as they are."""
    with path.open(encoding="utf-8") as f:
        return "".join(line for line in f if json.loads(line)["frame_idx"] in frames)


def build_item(
    root: Path,
    event: EventSummary,
    episode: Episode,
    video: Path,
    det: Path,
    pose: Path | None,
    hud: Path,
    frame_ms: list[int],
    label: dict[str, object],
) -> int:
    """Write the item of the analyzed frames at `frame_ms`; any read error leaves no files."""
    times = set(frame_ms)
    with hud.open(encoding="utf-8") as f:
        hud_lines = [line for line in f if json.loads(line)["ts_ms"] in times]
    frames = [json.loads(line)["frame_idx"] for line in hud_lines]
    quality = config.get_settings().evidence.jpeg_quality
    jpegs = {}
    for frame_idx in frames:  # every frame is read before the folder changes
        img = media.read_frame(video, frame_idx)
        jpegs[frame_idx] = media.encode_jpeg(img, quality, img.shape[1])
    wanted = set(frames)
    files = {"detections.jsonl": _lines(det, wanted), "hud.jsonl": "".join(hud_lines)}
    if pose is not None:
        files["pose.jsonl"] = _lines(pose, wanted)
    found = {"event_id": event.id, "label": "false_alarm", "scenario": event.scenario}
    found |= {"level": event.level, "reason_text": event.reason_text, **label}
    found |= {"start_ms": episode.start_ms, "end_ms": episode.end_ms}  # the episode, video time
    files["label.json"] = json.dumps(found, ensure_ascii=False, indent=2) + "\n"
    folder = root / item_path(event.id)
    shutil.rmtree(folder, ignore_errors=True)  # a tick that failed while writing left a part
    (folder / "frames").mkdir(parents=True)
    for frame_idx, data in jpegs.items():
        (folder / "frames" / f"{frame_idx}.jpg").write_bytes(data)
    for name, text in files.items():
        (folder / name).write_text(text, encoding="utf-8", newline="\n")
    return len(frames)


def export_zip(root: Path, items: list[DatasetItem], out: Path) -> Path:
    """Zip of `manifest.json` (the items) and every file of each item, at its path from root."""
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.dumps([i.model_dump(mode="json") for i in items], ensure_ascii=False, indent=2)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MANIFEST, manifest + "\n")
        for item in items:
            for path in sorted((root / item.path).rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(root).as_posix())
    return out
