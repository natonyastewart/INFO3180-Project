import json
from app.models import Favourite


def test_get_profiles(client, auth_headers):
    """Test getting all profiles."""
    response = client.get("/api/profiles", headers=auth_headers)
    data = json.loads(response.data)

    print(data["data"])

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["biography"] == "This is a test biography for user 1"


def test_profile_create(client, auth_headers):
    """Test creating a profile."""
    body = {
        "description": "Test description",
        "parish": "Test parish",
        "biography": "Test 2 biography for user 1",
        "sex": "Male",
        "race": "Test race",
        "birth_year": 1990,
        "height": 180.5,
        "fav_cuisine": "Italian",
        "fav_colour": "Blue",
        "fav_school_subject": "Math",
        "political": True,
        "religious": False,
        "family_oriented": True,
    }

    response = client.post(
        "/api/profiles",
        data=json.dumps(body),
        content_type="application/json",
        headers=auth_headers,
    )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["success"] is True
    assert data["data"]["user"]["id"] == 1

    # Test fetching
    response = client.get("/api/profiles", headers=auth_headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data["data"]) == 2

    # Create another one
    body["description"] = "Test 3 biography for user 1"

    response = client.post(
        "/api/profiles",
        data=json.dumps(body),
        content_type="application/json",
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert data["success"] is True

    # Test fetching
    response = client.get("/api/profiles", headers=auth_headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data["data"]) == 3

    # This should fail
    response = client.post(
        "/api/profiles",
        data=json.dumps(body),
        content_type="application/json",
        headers=auth_headers,
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["success"] is False


def test_get_profiles_detail(client, auth_headers):
    """Test getting a specific profile by ID."""
    # Test with valid profile ID
    response = client.get("/api/profiles/1", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["user"]["id"] == 1
    assert data["data"]["parish"] == "Kingston"
    assert data["data"]["sex"] == "Male"

    # Test with non-existent profile ID
    response = client.get("/api/profiles/999", headers=auth_headers)
    assert response.status_code == 404


def test_add_favourite(client, auth_headers):
    """Test adding a favourite."""
    # Test adding a new favourite
    payload = {"profileId": 3}  # User being favourited

    response = client.post(
        "/api/profiles/favourite",
        data=json.dumps(payload),
        content_type="application/json",
        headers=auth_headers,
    )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["success"] is True
    assert data["data"]["user_id"] == 1
    assert data["data"]["fav_profile_id"] == 3

    # Verify the favourite was added to the database
    with client.application.app_context():
        favourite = Favourite.query.filter_by(user_id_fk=1, fav_profile_id_fk=3).first()
        assert favourite is not None


def test_get_matches(client, auth_headers):
    """Test getting matches for a specific profile based on matching criteria."""
    response = client.get("/api/profiles/matches/1", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "data" in data

    # We should have exactly 2 matches based on our test data
    # Profile 3 and Profile 7 should match Profile 1
    assert len(data["data"]) == 2

    # Check that the matches are the expected profiles
    match_user_ids = [match["user"]["id"] for match in data["data"]]
    assert 3 in match_user_ids  # Profile 3 should match
    assert 7 in match_user_ids  # Profile 7 should match

    # Verify that profiles that shouldn't match are not included
    assert 4 not in match_user_ids  # Profile 4 shouldn't match (age outside range)
    assert (
        5 not in match_user_ids
    )  # Profile 5 shouldn't match (height difference too small)
    assert (
        6 not in match_user_ids
    )  # Profile 6 shouldn't match (insufficient preference matches)

    # Check that user info is included in the response
    for match in data["data"]:
        assert "user" in match
        assert "name" in match["user"]
        assert "photo" in match["user"]
        assert "id" in match["user"]


def test_search_profiles_no_filters(client, auth_headers):
    """Test searching profiles with no filters."""
    response = client.get("/api/search", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 6  # Should return all profiles but self
    assert len(list(filter(lambda x: x["user"]["id"] == 1, data["data"]))) == 0
    assert "Found 6 matching profiles" in data["message"]


def test_search_profiles_by_name(client, auth_headers):
    """Test searching profiles by name."""
    response = client.get("/api/search?name=Test User 2", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["user"]["id"] == 2


def test_search_profiles_by_birth_year(client, auth_headers):
    """Test searching profiles by birth year."""
    response = client.get("/api/search?birth_year=1988", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["birth_year"] == 1988


def test_search_profiles_by_sex(client, auth_headers):
    """Test searching profiles by sex."""
    response = client.get("/api/search?sex=Female", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 6
    assert data["data"][0]["sex"] == "Female"


def test_search_profiles_by_race(client, auth_headers):
    """Test searching profiles by race."""
    response = client.get("/api/search?race=Black", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["race"] == "Black"


def test_search_profiles_combined_filters(client, auth_headers):
    """Test searching profiles with multiple filters."""
    response = client.get("/api/search?sex=Female&race=Black", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["sex"] == "Female"
    assert data["data"][0]["race"] == "Black"


def test_get_user(client, auth_headers):
    """Test getting a specific user by ID."""
    # Test with valid user ID
    response = client.get("/api/users/1", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["username"] == "testuser1"
    assert data["data"]["name"] == "Test User 1"

    # Test with non-existent user ID
    response = client.get("/api/users/999", headers=auth_headers)
    assert response.status_code == 404


def test_get_user_favourites(client, auth_headers):
    """Test getting favourites for a specific user."""
    response = client.get("/api/users/favourites", headers=auth_headers)
    data = json.loads(response.data)

    print("data: ", data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["user_id"] == 1
    assert data["data"][0]["fav_profile_id"] == 1


def test_get_top_favourites_valid(client, auth_headers):
    """Test getting top favourites with valid threshold."""
    response = client.get("/api/users/favourites/2", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) <= 2  # Should return at most 2 users


def test_get_top_favourites_invalid_threshold(client, auth_headers):
    """Test getting top favourites with invalid threshold."""
    # Test with threshold below minimum
    response = client.get("/api/users/favourites/0", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["success"] is False
    assert "Threshold must be between 1 and 100" in data["errors"]["error"]

    # Test with threshold above maximum
    response = client.get("/api/users/favourites/101", headers=auth_headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["success"] is False
    assert "Threshold must be between 1 and 100" in data["errors"]["error"]


def test_unauthenticated_requests(client):
    """Test that unauthenticated requests are rejected."""
    # Test various endpoints without authentication
    endpoints = [
        "/api/profiles/1",
        "/api/search",
        "/api/users/1",
        "/api/users/favourites",
        "/api/users/favourites/5",
        "/api/profiles/matches/1",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data["success"] is False
        assert "Authentication token is missing" in data["message"]


def test_profile_required_routes(client, app):
    """Test that routes requiring a profile reject users without profiles."""
    # Create a user without a profile
    from app.utils import generate_token

    with app.app_context():
        from app.models import User, db

        # Create a new user without a profile
        user_no_profile = User(
            username="noprofile",
            password="password123",
            name="User Without Profile",
            email="noprofile@example.com",
        )
        db.session.add(user_no_profile)
        db.session.commit()

        # Generate token for this user
        token = generate_token(user_no_profile.id)
        headers = {"Authorization": f"Bearer {token}"}

    # Test endpoints that require a profile
    profile_required_endpoints = [
        "/api/profiles/favourite",
        "/api/profiles/matches/1",
        "/api/users/favourites",
    ]

    for endpoint in profile_required_endpoints:
        if endpoint == "/api/profiles/favourite":
            # For POST endpoint
            payload = {
                "user_id": 10,
                "user_id_fk": user_no_profile.id,
                "fav_profile_id_fk": 1,
            }
            response = client.post(
                endpoint,
                data=json.dumps(payload),
                content_type="application/json",
                headers=headers,
            )
        else:
            # For GET endpoints
            response = client.get(endpoint, headers=headers)

        data = json.loads(response.data)

        assert response.status_code == 403
        assert data["success"] is False
        assert "Profile required" in data["message"]
