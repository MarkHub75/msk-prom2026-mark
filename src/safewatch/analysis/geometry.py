"""Plane geometry on image pixels or floor meters (tech.md 7)."""

import math

import cv2
import numpy as np

from safewatch.types import Box, Point

MIN_CAL_POINTS = 4
MAX_CAL_POINTS = 8
MIN_AREA = 1e-4  # normalized frame area: a smaller zone or calibration triangle is degenerate


def point_in_polygon(p: Point, polygon: list[Point]) -> bool:
    """Even-odd ray casting; a point on the border may land on either side."""
    x, y = p
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def iou(a: Box, b: Box) -> float:
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def point_rect_distance(p: Point, box: Box) -> float:
    """Distance from a point to a rectangle, 0 inside it."""
    dx = max(box[0] - p[0], 0.0, p[0] - box[2])
    dy = max(box[1] - p[1], 0.0, p[1] - box[3])
    return math.hypot(dx, dy)


def point_segment_distance(p: Point, a: Point, b: Point) -> float:
    ax, ay = b[0] - a[0], b[1] - a[1]
    length2 = ax * ax + ay * ay
    t = 0.0 if length2 == 0 else ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / length2
    t = min(1.0, max(0.0, t))
    return math.dist(p, (a[0] + t * ax, a[1] + t * ay))


def polygon_area(points: list[Point]) -> float:
    """Shoelace area, always non-negative."""
    n = len(points)
    twice = sum(
        points[i][0] * points[(i + 1) % n][1] - points[(i + 1) % n][0] * points[i][1]
        for i in range(n)
    )
    return abs(twice) / 2


def homography(image_pts: list[Point], world_pts: list[Point]) -> np.ndarray | None:
    """3x3 least-squares fit (tech.md 8.11): normalized frame → floor meters; None if degenerate."""
    h, _ = cv2.findHomography(np.array(image_pts, np.float64), np.array(world_pts, np.float64), 0)
    return None if h is None else np.asarray(h, np.float64)


def apply_h(h: np.ndarray, p: Point) -> Point:
    x, y, w = h @ np.array([p[0], p[1], 1.0])
    return (float(x / w), float(y / w))


def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull_contains(points: list[Point], p: Point) -> bool:
    """`p` inside or on the convex hull of `points` (Andrew's monotone chain)."""
    pts = sorted(set(points))
    lower: list[Point] = []
    upper: list[Point] = []
    for chain, seq in ((lower, pts), (upper, pts[::-1])):
        for q in seq:
            while len(chain) >= 2 and _cross(chain[-2], chain[-1], q) <= 0:
                chain.pop()
            chain.append(q)
    hull = lower[:-1] + upper[:-1]  # counter-clockwise
    n = len(hull)
    return n >= 3 and all(_cross(hull[i], hull[(i + 1) % n], p) >= 0 for i in range(n))


def _clip(a: Point, b: Point) -> tuple[Point, Point] | None:
    """Liang-Barsky: the part of segment a-b inside the unit square."""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for q, d in ((a[0], -dx), (1 - a[0], dx), (a[1], -dy), (1 - a[1], dy)):
        if d == 0:
            if q < 0:
                return None
            continue
        t = q / d
        if d < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 > t1:
        return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


def grid_segments(h: np.ndarray, world_pts: list[Point]) -> list[tuple[Point, Point]]:
    """Floor lines every 1 m inside the box of the world points, back in the frame, in [0, 1]."""
    inv = np.linalg.inv(h)
    xs, ys = [p[0] for p in world_pts], [p[1] for p in world_pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    lines = [((float(x), y0), (float(x), y1)) for x in range(math.ceil(x0), math.floor(x1) + 1)]
    lines += [((x0, float(y)), (x1, float(y))) for y in range(math.ceil(y0), math.floor(y1) + 1)]
    out = []
    for a, b in lines:
        clipped = _clip(apply_h(inv, a), apply_h(inv, b))
        if clipped is not None:
            out.append(clipped)
    return out
