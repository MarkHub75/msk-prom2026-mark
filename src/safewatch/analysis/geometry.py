"""Plane geometry on image pixels or floor meters (tech.md 7)."""

import math

from safewatch.types import Box, Point


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
