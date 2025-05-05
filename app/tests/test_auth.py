import json
import pytest
from app import create_app
from app.models import db, User
from app.utils import decode_token


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com",
        "name": "Test User",
    }


@pytest.fixture
def create_user(client, user_data):
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        name=user_data["name"],
        password=user_data["password"],
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_register(client, user_data):
    """Test user registration"""
    response = client.post(
        "/api/register",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["success"] is True
    assert "token" in data["data"]
    assert "refreshToken" in data["data"]
    assert data["data"]["user"]["username"] == user_data["username"]

    # Verify token type
    token_payload = decode_token(data["data"]["token"])
    assert token_payload["type"] == "access"

    # Verify refresh token type
    refresh_token_payload = decode_token(data["data"]["refreshToken"])
    assert refresh_token_payload["type"] == "refresh"


def test_login(client, create_user, user_data):
    """Test user login"""
    response = client.post(
        "/api/auth/login",
        data=json.dumps(
            {
                "username": user_data["username"],
                "password": user_data["password"],
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert "token" in data["data"]
    assert "refreshToken" in data["data"]
    assert data["data"]["user"]["username"] == user_data["username"]

    # Verify token type
    token_payload = decode_token(data["data"]["token"])
    assert token_payload["type"] == "access"

    # Verify refresh token type
    refresh_token_payload = decode_token(data["data"]["refreshToken"])
    assert refresh_token_payload["type"] == "refresh"


def test_refresh_token(client, create_user):
    """Test token refresh"""
    # First login to get a refresh token
    response = client.post(
        "/api/auth/login",
        data=json.dumps(
            {
                "username": "testuser",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    login_data = json.loads(response.data)
    refresh_token = login_data["data"]["refreshToken"]

    # Use refresh token to get a new access token
    response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert "token" in data["data"]

    # Verify new token is an access token
    token_payload = decode_token(data["data"]["token"])
    assert token_payload["type"] == "access"


def test_refresh_with_access_token_fails(client, create_user):
    """Test that using an access token for refresh fails"""
    # First login to get an access token
    response = client.post(
        "/api/auth/login",
        data=json.dumps(
            {
                "username": "testuser",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    login_data = json.loads(response.data)
    access_token = login_data["data"]["token"]

    # Try to use access token for refresh
    response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401


def test_access_protected_route_with_refresh_token_fails(client, create_user):
    """Test that using a refresh token for a protected route fails"""
    # First login to get a refresh token
    response = client.post(
        "/api/auth/login",
        data=json.dumps(
            {
                "username": "testuser",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    login_data = json.loads(response.data)
    refresh_token = login_data["data"]["refreshToken"]

    # Try to use refresh token for a protected route
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == 401
