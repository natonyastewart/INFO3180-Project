import json
from app.models import User, db


def test_register_validation(client):
    """Test registration endpoint validation"""
    # Test with valid data
    valid_data = {
        "username": "newuser",
        "password": "password123",
        "name": "New User",
        "email": "newuser@example.com",
    }

    response = client.post(
        "/api/register", data=json.dumps(valid_data), content_type="application/json"
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] is True
    assert "User registered successfully" in data["message"]

    # Test with invalid data - username too short
    invalid_data = valid_data.copy()
    invalid_data["username"] = "nu"

    response = client.post(
        "/api/register", data=json.dumps(invalid_data), content_type="application/json"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]
    assert "username" in data["errors"]

    # Test with invalid data - invalid email
    invalid_data = valid_data.copy()
    invalid_data["email"] = "not-an-email"

    response = client.post(
        "/api/register", data=json.dumps(invalid_data), content_type="application/json"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]
    assert "email" in data["errors"]


def test_login_validation(client):
    """Test login endpoint validation"""
    # Create a test user first
    with client.application.app_context():
        user = User(
            username="logintest",
            password="password123",
            name="Login Test",
            email="logintest@example.com",
        )
        db.session.add(user)
        db.session.commit()

    # Test with valid data
    valid_data = {"username": "logintest", "password": "password123"}

    response = client.post(
        "/api/auth/login", data=json.dumps(valid_data), content_type="application/json"
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert "Login successful" in data["message"]

    # Test with invalid data - missing password
    invalid_data = {"username": "logintest"}

    response = client.post(
        "/api/auth/login",
        data=json.dumps(invalid_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]
    assert "password" in data["errors"]


def test_add_favourite_validation(client, auth_headers):
    """Test add favourite endpoint validation"""
    # Test with valid data
    valid_data = {"profileId": 3}

    response = client.post(
        "/api/profiles/favourite",
        data=json.dumps(valid_data),
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] is True

    # Test with invalid data - missing profileId
    invalid_data = {}

    response = client.post(
        "/api/profiles/favourite",
        data=json.dumps(invalid_data),
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]
    assert "profileId" in data["errors"]

    # Test with invalid data - profileId not an integer
    invalid_data = {"profileId": "not-an-integer"}

    response = client.post(
        "/api/profiles/favourite",
        data=json.dumps(invalid_data),
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]


def test_search_validation(client, auth_headers):
    """Test search endpoint validation"""
    # Test with valid data
    response = client.get("/api/search?birth_year=1990", headers=auth_headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True

    # Test with invalid data - birth_year not an integer
    response = client.get("/api/search?birth_year=not-an-integer", headers=auth_headers)

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Validation error" in data["message"]
    assert "birth_year" in data["errors"]
