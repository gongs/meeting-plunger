"""Unit tests for the Meeting Plunger API."""

import sys
from pathlib import Path

# Add parent directory to path to import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Meeting Plunger API"
    assert data["status"] == "running"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_cors_credentials():
    """Test CORS credentials are enabled."""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


def test_transcribe_endpoint():
    """Test the transcribe endpoint with mock enabled."""
    # Enable mock with expected transcript
    mock_response = client.post(
        "/testability/mock", json={"enabled": True, "transcript": "Hello, how are you?"}
    )
    assert mock_response.status_code == 200

    # Create a dummy file
    files = {"file": ("test.wav", b"dummy audio content", "audio/wav")}
    response = client.post("/transcribe", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == "Hello, how are you?"

    # Disable mock for other tests
    client.post("/testability/mock", json={"enabled": False})


def test_reset_db():
    """Test the reset-db testability endpoint."""
    response = client.post("/testability/reset-db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_register_success():
    """Register returns token when username is new."""
    client.post("/testability/reset-db")
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0


def test_register_duplicate_username():
    """Register returns 409 and 用户名已存在 when username exists."""
    client.post("/testability/reset-db")
    client.post(
        "/auth/register",
        json={"username": "bob", "password": "secret123"},
    )
    response = client.post(
        "/auth/register",
        json={"username": "bob", "password": "other456"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "用户名已存在"


def test_login_success():
    """Login returns token for valid credentials."""
    client.post("/testability/reset-db")
    client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)


def test_login_invalid_password():
    """Login returns 401 for wrong password."""
    client.post("/testability/reset-db")
    client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "alice", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_unknown_user():
    """Login returns 401 for unknown username."""
    client.post("/testability/reset-db")
    response = client.post(
        "/auth/login",
        json={"username": "nobody", "password": "any"},
    )
    assert response.status_code == 401


def _register_and_token(username: str = "alice", password: str = "secret123"):
    """Reset DB, register user, return token."""
    client.post("/testability/reset-db")
    r = client.post("/auth/register", json={"username": username, "password": password})
    assert r.status_code == 200
    return r.json()["token"]


def test_venues_list_requires_auth():
    """GET /venues returns 401 without token."""
    client.post("/testability/reset-db")
    response = client.get("/venues")
    assert response.status_code == 401


def test_venues_list_returns_default_venue():
    """GET /venues returns at least default venue after login."""
    token = _register_and_token()
    response = client.get("/venues", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    default = next((v for v in data if v["name"] == "默认赛场"), None)
    assert default is not None
    assert "id" in default


def test_venues_create():
    """POST /venues creates venue and returns it."""
    token = _register_and_token()
    response = client.post(
        "/venues",
        json={"name": "New Arena"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Arena"
    assert "id" in data


def test_enter_venue_creates_participant():
    """POST /venues/{id}/enter creates participant and GET returns participants."""
    token = _register_and_token()
    list_r = client.get("/venues", headers={"Authorization": f"Bearer {token}"})
    venue_id = list_r.json()[0]["id"]
    enter_r = client.post(
        f"/venues/{venue_id}/enter",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert enter_r.status_code == 200
    get_r = client.get(
        f"/venues/{venue_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_r.status_code == 200
    data = get_r.json()
    assert data["participants"]
    me = next((p for p in data["participants"] if p["username"] == "alice"), None)
    assert me is not None
    assert me["position"] == 0
    assert me["condition"] == 6
    assert me["mode"] == "normal"
    assert me["won"] is False
    assert me["game_over"] is False


def test_get_venue_without_enter_returns_403():
    """GET /venues/{id} without having entered returns 403."""
    token = _register_and_token()
    # Create a second venue and do not enter it
    create_r = client.post(
        "/venues",
        json={"name": "Other"},
        headers={"Authorization": f"Bearer {token}"},
    )
    venue_id = create_r.json()["id"]
    # Enter default venue so we have one; then get "Other" without entering
    list_r = client.get("/venues", headers={"Authorization": f"Bearer {token}"})
    default_id = next(v["id"] for v in list_r.json() if v["name"] == "默认赛场")
    client.post(f"/venues/{default_id}/enter", headers={"Authorization": f"Bearer {token}"})
    get_r = client.get(
        f"/venues/{venue_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_r.status_code == 403


def test_roll_returns_dice_and_updates_state():
    """POST /venues/{id}/roll returns dice and updates participant state."""
    token = _register_and_token()
    list_r = client.get("/venues", headers={"Authorization": f"Bearer {token}"})
    venue_id = list_r.json()[0]["id"]
    client.post(f"/venues/{venue_id}/enter", headers={"Authorization": f"Bearer {token}"})
    roll_r = client.post(
        f"/venues/{venue_id}/roll",
        json={"mode": "normal"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert roll_r.status_code == 200
    data = roll_r.json()
    assert 1 <= data["dice"] <= 6
    assert data["steps"] in (1, 2)
    assert data["newPosition"] == data["steps"]
    assert data["newCondition"] == 6
    assert data["won"] is False
    assert data["gameOver"] is False
    get_r = client.get(f"/venues/{venue_id}", headers={"Authorization": f"Bearer {token}"})
    me = next(p for p in get_r.json()["participants"] if p["username"] == "alice")
    assert me["position"] == data["newPosition"]
    assert me["condition"] == 6
