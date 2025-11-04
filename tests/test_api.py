import pytest
from triangulator_app import app


# REMEMBER => use monkeypatch pour fake les retours des methodes du PSM

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_triangulation_success_binary(client, monkeypatch):
    assert True


def test_invalid_uuid_returns_400(client):
    response = client.get("/triangulation/***invalid-uuid***")
    assert response.status_code == 400
    assert response.get_json() == {
        "code": "TRIANGULATION_FAILED",
        "message": "Triangulation could not be computed for the given point set."
    }

def test_pointset_not_found_returns_404(client, monkeypatch):
    assert True


def test_triangulation_internal_error_returns_500(client, monkeypatch):
    assert True


def test_pointset_manager_unavailable_returns_503(client, monkeypatch):
    assert True
