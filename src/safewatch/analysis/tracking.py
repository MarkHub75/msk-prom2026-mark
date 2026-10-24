"""ByteTrack-like tracker (tech.md 8.2 item 4): two score stages, IoU cost, TTL on source time."""

import itertools
from dataclasses import dataclass

import numpy as np
from scipy.optimize import linear_sum_assignment

from safewatch.analysis.geometry import iou
from safewatch.config import TrackerConfig
from safewatch.types import Box, Detection


@dataclass
class _Track:
    box: Box
    last_seen: int  # ms of the source
    hits: int  # matches in a row while tentative
    track_id: int | None  # None until confirmed: ids stay dense
    prev: tuple[Box, int] | None = None  # the update before the last one

    def predict(self, ts_ms: int) -> Box:
        """Constant velocity of the center from the two last updates, the size unchanged."""
        if self.prev is None or self.last_seen == self.prev[1]:
            return self.box
        old, old_ts = self.prev
        k = (ts_ms - self.last_seen) / (self.last_seen - old_ts)
        dx = ((self.box[0] + self.box[2]) - (old[0] + old[2])) / 2 * k
        dy = ((self.box[1] + self.box[3]) - (old[1] + old[3])) / 2 * k
        x1, y1, x2, y2 = self.box
        return (x1 + dx, y1 + dy, x2 + dx, y2 + dy)

    def update(self, box: Box, ts_ms: int) -> None:
        self.prev = (self.box, self.last_seen)
        self.box, self.last_seen = box, ts_ms


class Tracker:
    """One instance per object family; `ids` is shared, so people and vehicles never collide."""

    def __init__(self, cfg: TrackerConfig, ids: "itertools.count[int]") -> None:
        self.cfg = cfg
        self.ids = ids
        self.tracks: list[_Track] = []

    def _match(
        self, tracks: list[_Track], dets: list[Detection], ts_ms: int
    ) -> list[tuple[_Track, Detection]]:
        if not tracks or not dets:
            return []
        ious = np.array([[iou(t.predict(ts_ms), d.bbox_xyxy) for d in dets] for t in tracks])
        rows, cols = linear_sum_assignment(1 - ious)
        return [
            (tracks[r], dets[c])
            for r, c in zip(rows, cols, strict=True)
            if ious[r, c] >= self.cfg.min_iou
        ]

    def update(self, ts_ms: int, dets: list[Detection]) -> list[tuple[int, Detection]]:
        """Confirmed tracks matched in this frame with their detections; a prediction is not one."""
        cfg = self.cfg
        max_lost_ms = cfg.max_lost_s * 1000
        self.tracks = [t for t in self.tracks if ts_ms - t.last_seen <= max_lost_ms]
        high = [d for d in dets if d.score >= cfg.high_thresh]
        low = [d for d in dets if cfg.low_thresh <= d.score < cfg.high_thresh]
        pairs = self._match(self.tracks, high, ts_ms)
        used = {id(t) for t, _ in pairs}
        pairs += self._match([t for t in self.tracks if id(t) not in used], low, ts_ms)
        matched = {id(t) for t, _ in pairs}
        taken = {id(d) for _, d in pairs}
        # A tentative track that missed a frame is dropped: confirmation needs hits in a row.
        self.tracks = [t for t in self.tracks if t.track_id is not None or id(t) in matched]
        for det in dets:
            if id(det) not in taken and det.score >= cfg.new_track_thresh:
                track = _Track(box=det.bbox_xyxy, last_seen=ts_ms, hits=0, track_id=None)
                self.tracks.append(track)
                pairs.append((track, det))
        out: list[tuple[int, Detection]] = []
        for track, det in pairs:
            if track.hits:  # the opening detection is the first hit, not an update
                track.update(det.bbox_xyxy, ts_ms)
            if track.track_id is None:
                track.hits += 1
                if track.hits >= cfg.min_hits:
                    track.track_id = next(self.ids)
            if track.track_id is not None:
                out.append((track.track_id, det))
        return out
