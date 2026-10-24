"""Slice 4: geometry of tech.md 7 (property-based, tech.md 10)."""

import math

from hypothesis import given
from hypothesis import strategies as st

from safewatch.analysis.geometry import ioa, iou, point_in_polygon, segment_crossing


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


_box = st.tuples(st.floats(-100, 100), st.floats(-100, 100), st.floats(1, 100), st.floats(1, 100))


@given(a=_box, b=_box)
def test_ioa_properties(a: tuple[float, ...], b: tuple[float, ...]) -> None:
    """Slice 10: share of `a` inside `b`, in [0, 1]; both shares weigh the same overlap."""
    ra = (a[0], a[1], a[0] + a[2], a[1] + a[3])
    rb = (b[0], b[1], b[0] + b[2], b[1] + b[3])
    assert 0.0 <= ioa(ra, rb) <= 1.0 + 1e-9
    assert math.isclose(ioa(ra, ra), 1.0)
    assert math.isclose(ioa(ra, rb) * a[2] * a[3], ioa(rb, ra) * b[2] * b[3], abs_tol=1e-6)
    outer = (ra[0] - 1, ra[1] - 1, ra[2] + 1, ra[3] + 1)
    assert math.isclose(ioa(ra, outer), 1.0)
    assert ioa(ra, (ra[2], ra[1], ra[2] + 5, ra[3])) == 0.0  # touching edge


@given(
    a=st.tuples(st.floats(-50, 50), st.floats(-50, 50)),
    angle=st.floats(0, 2 * math.pi),
    length=st.floats(1, 50),
    t=st.floats(0.01, 0.99),
    d1=st.floats(0.01, 20),
    d2=st.floats(0.01, 20),
)
def test_segment_crossing_properties(
    a: tuple[float, float], angle: float, length: float, t: float, d1: float, d2: float
) -> None:
    """Slice 10: a move across the segment crosses it, along one side or past its end does not."""
    ux, uy = math.cos(angle), math.sin(angle)
    b = (a[0] + length * ux, a[1] + length * uy)
    m = (a[0] + t * length * ux, a[1] + t * length * uy)
    nx, ny = -uy, ux

    def at(base: tuple[float, float], s: float) -> tuple[float, float]:
        return (base[0] + s * nx, base[1] + s * ny)

    p, q = at(m, -d1), at(m, d2)
    assert segment_crossing(p, q, a, b) and segment_crossing(q, p, a, b)
    assert segment_crossing(p, q, b, a)
    assert not segment_crossing(at(m, d1), at(m, d1 + d2), a, b)  # stays on one side
    beyond = (a[0] + (length + 1) * ux, a[1] + (length + 1) * uy)
    assert not segment_crossing(at(beyond, -d1), at(beyond, d2), a, b)  # the line, not the segment
    assert not segment_crossing(p, p, a, b)
