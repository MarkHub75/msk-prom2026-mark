"""Atomic snapshots of the exact analyzed frame, never a newer video frame."""
import os
from pathlib import Path
from uuid import uuid4
from PIL import Image, ImageDraw


def save_snapshot(root, batch, frame):
    directory = Path(root) / 'evidence'
    directory.mkdir(parents=True, exist_ok=True)
    # Never interpolate camera IDs from remote input into filesystem paths.
    name = str(uuid4()) + '.jpg'
    final, temp = directory / name, directory / (name + '.tmp')
    im = Image.fromarray(frame).convert('RGB')
    draw = ImageDraw.Draw(im)
    for d in batch['detections']:
        draw.rectangle(d['bbox_xyxy'], outline='red', width=3)
        draw.text((d['bbox_xyxy'][0], max(0, d['bbox_xyxy'][1] - 12)), d['class_name'], fill='red')
    try:
        with open(temp, 'wb') as f:
            im.save(f, format='JPEG', quality=90)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, final)
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        temp.unlink(missing_ok=True)
    return 'evidence/' + name
