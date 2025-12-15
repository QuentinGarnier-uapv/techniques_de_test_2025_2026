import math
import pytest
import struct

from models.Point import Point
from models.PointSet import PointSet
from models.Triangle import Triangle
from models.Triangles import Triangles


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
    pts = [Point(0.0, 0.0), Point(1.0, 2.0), Point(-3.5, 4.25)]
    ps = PointSet(points=pts)
    b = ps.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    ps2 = PointSet.from_bytes(b)
    assert len(ps.points) == len(ps2.points)
    for a, bpt in zip(ps.points, ps2.points):
        assert approx_points(a, bpt)


def test_pointset_empty_bytes():
    """Empty PointSet bytes."""
    ps = PointSet(points=[])
    b = ps.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    ps2 = PointSet.from_bytes(b)
    assert ps2.points == []


def test_triangles_bytes():
    """Triangles.to_bytes -> Triangles.from_bytes preserves points and indices."""
    pts = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0), Point(1.0, 1.0)]
    tris = [Triangle(0, 1, 2), Triangle(1, 3, 2)]
    T = Triangles(points=pts, triangles=tris)
    b = T.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    T2 = Triangles.from_bytes(b)
    assert len(T.points) == len(T2.points)
    assert len(T.triangles) == len(T2.triangles)
    for p_old, p_new in zip(T.points, T2.points):
        assert approx_points(p_old, p_new)
    for t_old, t_new in zip(T.triangles, T2.triangles):
        assert (t_old.a, t_old.b, t_old.c) == (t_new.a, t_new.b, t_new.c)


def test_triangles_empty_bytes():
    """Empty Triangles (no points, no triangles)."""
    T = Triangles(points=[], triangles=[])
    b = T.to_bytes()
    assert isinstance(b, (bytes, bytearray))
    T2 = Triangles.from_bytes(b)
    assert T2.points == []
    assert T2.triangles == []


def test_point_from_bytes_invalid():
    """Test Point.from_bytes with invalid data raises ValueError."""
    with pytest.raises(ValueError, match="Invalid byte sequence for Point"):
        Point.from_bytes(b"\x00\x00\x00")


def test_point_to_tuple():
    """Test Point.to_tuple."""
    p = Point(1.0, 2.0)
    assert p.to_tuple() == (1.0, 2.0)


def test_pointset_from_bytes_too_short():
    """Test PointSet.from_bytes with data too short for header."""
    with pytest.raises(ValueError, match="Data too short"):
        PointSet.from_bytes(b"\x00\x00")


def test_pointset_from_bytes_points_truncated():
    """Test PointSet.from_bytes with correct count but missing point data."""
    data = struct.pack("<I", 1)
    with pytest.raises(ValueError, match="Data too short for points"):
        PointSet.from_bytes(data)


def test_triangle_from_bytes_invalid_len():
    """Test Triangle.from_bytes with data too short."""
    with pytest.raises(ValueError, match="Invalid byte sequence for Triangle"):
        Triangle.from_bytes(b"\x00" * 11)


def test_triangles_from_bytes_too_short_header():
    """Test Triangles.from_bytes with data too short for PointSet count."""
    with pytest.raises(ValueError, match="Data too short"):
        Triangles.from_bytes(b"\x00")


def test_triangles_from_bytes_too_short_pointset():
    """Test Triangles.from_bytes when PointSet data is truncated."""
    data = struct.pack("<I", 1) 
    with pytest.raises(ValueError, match="Data too short for PointSet"):
        Triangles.from_bytes(data)


def test_triangles_from_bytes_too_short_triangle_count():
    """Test Triangles.from_bytes when missing triangle count header."""
    data = struct.pack("<I", 0)
    with pytest.raises(ValueError, match="Data too short for Triangle count"):
        Triangles.from_bytes(data)


def test_triangles_from_bytes_too_short_triangles_data():
    """Test Triangles.from_bytes when triangle data is truncated."""
    data = struct.pack("<II", 0, 1)
    with pytest.raises(ValueError, match="Data too short for expected triangles"):
        Triangles.from_bytes(data)
