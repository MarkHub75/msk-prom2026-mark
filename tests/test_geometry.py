"""Slice 4: geometry of tech.md 7 (property-based, tech.md 10)."""

import math

from hypothesis import given
from hypothesis import strategies as st

from safewatch.analysis.geometry import iou, point_in_polygon


@st.composite
def _convex(draw: st.DrawFn) -> list[tuple[float, float]]:
    """A convex polygon: points on a circle at sorted, distinct angles."""
    cx, cy = draw(st.floats(-100, 100)), draw(st.floats(-100, 100))
    r = draw(st.floats(1, 100))
    angles = sorted(draw(st.sets(st.integers(0, 359), min_size=3, max_size=12)))
    return [
        (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in angles
    ]


@given(poly=_convex(), vertex=st.integers(0, 11), t=st.floats(0, 0.9), side=st.integers(0, 3))
def test_point_in_polygon_properties(
    poly: list[tuple[float, float]], vertex: int, t: float, side: int
) -> None:
    n = len(poly)
    centroid = (sum(x for x, _ in poly) / n, sum(y for _, y in poly) / n)
    vx, vy = poly[vertex % n]
    inside = (centroid[0] + t * (vx - centroid[0]), centroid[1] + t * (vy - centroid[1]))
    assert point_in_polygon(inside, poly)

    xs, ys = [x for x, _ in poly], [y for _, y in poly]
    outside = [
        (min(xs) - 1, centroid[1]),
        (max(xs) + 1, centroid[1]),
        (centroid[0], min(ys) - 1),
        (centroid[0], max(ys) + 1),
    ][side]
    assert not point_in_polygon(outside, poly)


def test_iou_values() -> None:
    a = (0.0, 0.0, 100.0, 100.0)
    assert iou(a, a) == 1.0
    assert iou(a, (0.0, 0.0, 100.0, 50.0)) == 0.5
    assert iou(a, (100.0, 0.0, 200.0, 100.0)) == 0.0  # touching edges do not overlap
