import pytest

def test_three_points_produces_one_triangle():
    """
    Given 3 non-colinear points, Triangulator should return exactly 1 triangle
    and the triangle should reference the three input points.
    """
    raise NotImplementedError

def test_square_produces_two_triangles():
    """
    Given 4 points forming a square (or rectangle), Triangulator should return 2 triangles.
    """
    raise NotImplementedError

def test_regular_polygon_produces_n_minus_2_triangles():
    """
    Given a convex polygon with n points (n >= 3), Triangulator should return n - 2 triangles.
    Example: pentagon -> 3 triangles.
    """
    raise NotImplementedError

def test_no_points_returns_empty_triangles():
    """
    Given an empty point set, Triangulator should return zero triangles (empty result).
    """
    raise NotImplementedError

def test_one_point_returns_empty_triangles():
    """
    Given a single point, Triangulator should return zero triangles.
    """
    raise NotImplementedError

def test_two_points_returns_empty_triangles():
    """
    Given two distinct points, Triangulator should return zero triangles.
    """
    raise NotImplementedError

def test_duplicate_points_handled_or_error():
    """
    Given point sets containing duplicate points return zero/filtered triangles
    """
    raise NotImplementedError

def test_colinear_points_no_triangles():
    """
    Given multiple colinear points, triangulation must produce zero triangles
    """
    raise NotImplementedError

def test_triangle_indices_within_pointset_range():
    """
    For any produced triangle, all vertex indices must be within [0, len(points)-1].
    """
    raise NotImplementedError

def test_invalid_input_type_raises():
    """
    Given invalid input types (e.g. None, wrong structure), Triangulator should
    raise a ValueError.
    """
    raise NotImplementedError
