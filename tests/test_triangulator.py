import pytest
from Triangulator import Triangulator
from models.Point import Point
from models.PointSet import PointSet

tri = Triangulator()

def test_three_points_produces_one_triangle():
    """
    Given 3 non-colinear points, Triangulator should return exactly 1 triangle
    and the triangle should reference the three input points.
    """
    points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) == 1
    t = result.triangles[0]
    indices = {t.a, t.b, t.c}
    assert indices == {0, 1, 2}

def test_square_produces_two_triangles():
    """
    Given 4 points forming a square (or rectangle), Triangulator should return 2 triangles.
    """
    points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) == 2

def test_regular_polygon_produces_n_minus_2_triangles():
    """
    Given a convex polygon with n points (n >= 3), Triangulator should return n - 2 triangles.
    Example: pentagon -> 3 triangles.
    """
    points = [
        Point(0, 10), Point(10, 0), Point(10, 10),
        Point(0, 0), Point(5, 15)
    ]
    pset = PointSet(points)
    result = tri.compute(pset)
    expected_triangles = len(points) - 2
    assert len(result.triangles) == expected_triangles

def test_no_points_returns_empty_triangles():
    """
    Given an empty point set, Triangulator should return zero triangles (empty result).
    """
    pset = PointSet([])
    result = tri.compute(pset)
    assert len(result.triangles) == 0
    assert len(result.points) == 0

def test_one_point_returns_empty_triangles():
    """
    Given a single point, Triangulator should return zero triangles.
    """
    pset = PointSet([Point(0.0, 0.0)])
    result = tri.compute(pset)
    assert len(result.triangles) == 0

def test_two_points_returns_empty_triangles():
    """
    Given two distinct points, Triangulator should return zero triangles.
    """
    pset = PointSet([Point(0.0, 0.0), Point(1.0, 1.0)])
    result = tri.compute(pset)
    assert len(result.triangles) == 0

def test_duplicate_points_handled_or_error():
    """
    Given point sets containing duplicate points, return triangles based on unique geometry
    or simply handle it gracefully without crashing.
    """
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(0, 0)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) <= 1

def test_colinear_points_no_triangles():
    """
    Given multiple colinear points, triangulation must produce zero triangles
    """
    points = [Point(0, 0), Point(1, 1), Point(2, 2)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) == 0