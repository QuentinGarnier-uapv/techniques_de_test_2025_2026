import math
from models.Point import Point
from models.Triangle import Triangle


def approx_points(p1: Point, p2: Point, rel_tol=1e-6):
    return math.isclose(p1.x, p2.x, rel_tol=rel_tol) and math.isclose(p1.y, p2.y, rel_tol=rel_tol)


def test_point_bytes():
    """Point.to_bytes -> Point.from_bytes bytes preserves coordinates."""
    p = Point(1.5, -2.25)
    b = p.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    p2 = Point.from_bytes(b)
    assert approx_points(p, p2)


def test_triangle_bytes():
    """Triangle.to_bytes -> Triangle.from_bytes preserves indices."""
    t = Triangle(0, 5, 2)
    b = t.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    t2 = Triangle.from_bytes(b)
    assert (t.a, t.b, t.c) == (t2.a, t2.b, t2.c)


def test_pointset_bytes():
    """PointSet.to_bytes -> PointSet.from_bytes preserves points."""


def test_pointset_empty_bytes():
    """Empty PointSet bytes."""


def test_triangles_bytes():
    """Triangles.to_bytes -> Triangles.from_bytes preserves points and indices."""

def test_triangles_empty_bytes():
    """Empty Triangles (no points, no triangles)."""

