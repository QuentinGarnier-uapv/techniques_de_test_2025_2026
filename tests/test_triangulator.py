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