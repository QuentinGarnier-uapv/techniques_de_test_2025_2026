import pytest
from unittest.mock import MagicMock, patch
import urllib.error
from models.PointSet import PointSet
from Triangulator import Triangulator

tri = Triangulator()

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
