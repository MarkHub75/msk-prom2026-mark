"""Atomic snapshots of the exact analyzed frame, never a newer video frame."""
import os
from pathlib import Path
from uuid import uuid4
import hashlib
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
        from ml.pipeline.capture_recovery import save_json
        save_json(final.with_suffix('.json'),{
            'schema_version':'1.0','camera_id':batch['camera_id'],
            'stream_epoch':batch['stream_epoch'],'frame_id':batch['frame_id'],
            'media_time_ms':batch['media_time_ms'],'image_size':batch['image_size'],
            'source_sha256':batch.get('source_sha256'),
            'rgb_sha256':hashlib.sha256(frame.tobytes(order='C')).hexdigest(),
            'snapshot_sha256':hashlib.sha256(final.read_bytes()).hexdigest()})
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        temp.unlink(missing_ok=True)
    return 'evidence/' + name
