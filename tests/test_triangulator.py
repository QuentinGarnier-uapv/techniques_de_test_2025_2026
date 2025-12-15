import pytest

from models.Point import Point
from models.PointSet import PointSet
from models.Triangles import Triangles
from Triangulator import Triangulator

from unittest.mock import MagicMock, patch
import urllib.error


tri = Triangulator()

def test_three_points_produces_one_triangle():
    """Given 3 non-colinear points, Triangulator should return exactly 1 triangle
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
    """Given 4 points forming a square (or rectangle), Triangulator should return 2 triangles.
    """
    points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) == 2

def test_regular_polygon_produces_n_minus_2_triangles():
    """Given a convex polygon with n points (n >= 3), Triangulator should return n - 2 triangles.
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
    """Given an empty point set, Triangulator should return zero triangles (empty result).
    """
    pset = PointSet([])
    result = tri.compute(pset)
    assert len(result.triangles) == 0
    assert len(result.points) == 0

def test_one_point_returns_empty_triangles():
    """Given a single point, Triangulator should return zero triangles.
    """
    pset = PointSet([Point(0.0, 0.0)])
    result = tri.compute(pset)
    assert len(result.triangles) == 0

def test_two_points_returns_empty_triangles():
    """Given two distinct points, Triangulator should return zero triangles.
    """
    pset = PointSet([Point(0.0, 0.0), Point(1.0, 1.0)])
    result = tri.compute(pset)
    assert len(result.triangles) == 0

def test_duplicate_points_handled_or_error():
    """Given point sets containing duplicate points, return triangles based on unique geometry
    or simply handle it gracefully without crashing.
    """
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(0, 0)]
    pset = PointSet(points)
    result = tri.compute(pset)
    assert len(result.triangles) <= 1

def test_colinear_points_no_triangles():
    """Given multiple colinear points, triangulation must produce zero triangles
    """
    points = [Point(0, 0), Point(1, 1), Point(2, 2)]
    pset = PointSet(points)
    with pytest.raises(ValueError, match="Collinear points"):
        tri.compute(pset)

def test_triangle_indices_within_pointset_range():
    """For any produced triangle, all vertex indices must be within [0, len(points)-1].
    """
    points = [Point(0, 0), Point(10, 0), Point(5, 5)]
    pset = PointSet(points)
    result = tri.compute(pset)
    max_index = len(points) - 1
    for t in result.triangles:
        assert 0 <= t.a <= max_index
        assert 0 <= t.b <= max_index
        assert 0 <= t.c <= max_index

def test_invalid_input_type_raises():
    """Test invalid input types handling.

    Given invalid input types (e.g. None, wrong structure), Triangulator should
    raise an Exception (AttributeError or TypeError).
    """
    with pytest.raises((AttributeError, TypeError)):
        tri.compute(None)


@patch("urllib.request.urlopen")
def test_get_point_set_success(mock_urlopen):
    """Test get_point_set successfully fetches and parses data."""
    data = b"\x01\x00\x00\x00" + b"\x00\x00\x00\x00\x00\x00\x00\x00"
    mock_response = MagicMock()
    mock_response.read.return_value = data
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    ps = tri.get_point_set("00000000-0000-0000-0000-000000000000")
    assert isinstance(ps, PointSet)
    assert len(ps.points) == 1


@patch("urllib.request.urlopen")
def test_get_point_set_404(mock_urlopen):
    """Test get_point_set handles 404 Not Found."""
    err = urllib.error.HTTPError(
        url="http://localhost:3000/...",
        code=404,
        msg="Not Found",
        hdrs={},
        fp=None
    )
    mock_urlopen.side_effect = err
    
    with pytest.raises(urllib.error.HTTPError):
        tri.get_point_set("00000000-0000-0000-0000-000000000000")


@patch("urllib.request.urlopen")
def test_get_point_set_503(mock_urlopen):
    """Test get_point_set handles 503 Service Unavailable."""
    err = urllib.error.HTTPError(
        url="http://localhost:3000/...",
        code=503,
        msg="Unavailable",
        hdrs={},
        fp=None
    )
    mock_urlopen.side_effect = err
    
    with pytest.raises(urllib.error.HTTPError):
        tri.get_point_set("00000000-0000-0000-0000-000000000000")


@patch("urllib.request.urlopen")
def test_get_point_set_other_http_error(mock_urlopen):
    """Test get_point_set handles other HTTP errors."""
    err = urllib.error.HTTPError(
        url="http://localhost:3000/...",
        code=500,
        msg="Internal Error",
        hdrs={},
        fp=None
    )
    mock_urlopen.side_effect = err
    
    with pytest.raises(urllib.error.HTTPError):
        tri.get_point_set("00000000-0000-0000-0000-000000000000")


@patch("urllib.request.urlopen")
def test_get_point_set_url_error(mock_urlopen):
    """Test get_point_set handles URLError."""
    err = urllib.error.URLError(reason="Connection refused")
    mock_urlopen.side_effect = err
    
    with pytest.raises(urllib.error.URLError):
        tri.get_point_set("00000000-0000-0000-0000-000000000000")

def test_check_collinearity_epsilon():
    """Test check_collinearity with extremely close points (epsilon check)."""
    
    p1 = Point(0, 0)
    p2 = Point(1e-10, 0) 
    p3 = Point(0, 1e-10)
    
    points = [p1, p2, p3]
    pset = PointSet(points)
    
    with pytest.raises(ValueError, match="Collinear points"):
        tri.compute(pset)