import pytest
from app.schemas import (
    RegistrationRequestSchema,
    LoginRequestSchema,
    FavouriteRequestSchema,
    ProfileSchema,
    UserSchema,
)


def test_registration_schema_validation():
    """Test validation of registration schema"""
    schema = RegistrationRequestSchema()

    # Valid data
    valid_data = {
        "username": "testuser",
        "password": "password123",
        "name": "Test User",
        "email": "test@example.com",
    }
    result = schema.load(valid_data)
    assert result["username"] == "testuser"
    assert result["password"] == "password123"

    # Invalid data - missing required fields
    invalid_data = {"username": "testuser"}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)

    # Invalid data - username too short
    invalid_data = {
        "username": "te",
        "password": "password123",
        "name": "Test User",
        "email": "test@example.com",
    }
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)

    # Invalid data - invalid email
    invalid_data = {
        "username": "testuser",
        "password": "password123",
        "name": "Test User",
        "email": "invalid-email",
    }
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)


def test_login_schema_validation():
    """Test validation of login schema"""
    schema = LoginRequestSchema()

    # Valid data
    valid_data = {"username": "testuser", "password": "password123"}
    result = schema.load(valid_data)
    assert result["username"] == "testuser"
    assert result["password"] == "password123"

    # Invalid data - missing required fields
    invalid_data = {"username": "testuser"}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)


def test_favourite_schema_validation():
    """Test validation of favourite schema"""
    schema = FavouriteRequestSchema()

    # Valid data
    valid_data = {"userId": 123}
    result = schema.load(valid_data)
    assert result["userId"] == 123

    # Invalid data - missing required fields
    invalid_data = {}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)

    # Invalid data - wrong type
    invalid_data = {"userId": "not-an-integer"}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)


def test_profile_schema_validation():
    """Test validation of profile schema"""
    schema = ProfileSchema()

    # Valid data
    valid_data = {
        "user_id": 1,
        "description": "Test description",
        "parish": "Test parish",
        "biography": "Test biography",
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
    result = schema.load(valid_data)
    assert result["user_id_fk"] == 1
    assert result["description"] == "Test description"

    # Invalid data - missing required fields
    invalid_data = {"user_id": 1, "description": "Test description"}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)

    # Invalid data - birth year too old
    invalid_data = valid_data.copy()
    invalid_data["birth_year"] = 1800
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)

    # Invalid data - height invalid
    invalid_data = valid_data.copy()
    invalid_data["height"] = -10
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)


def test_user_schema_validation():
    """Test validation of user schema"""
    schema = UserSchema()

    # Valid data
    valid_data = {
        "username": "testuser",
        "password": "password123",
        "name": "Test User",
        "email": "test@example.com",
        "photo": "photo.jpg",
    }
    result = schema.load(valid_data)
    assert result["username"] == "testuser"
    assert result["name"] == "Test User"

    # Invalid data - missing required fields
    invalid_data = {"username": "testuser"}
    with pytest.raises(Exception) as e:
        schema.load(invalid_data)
