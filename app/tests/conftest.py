import pytest
from app import create_app
from app.models import User, db, Profile, Favourite
import os
import tempfile


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    db_fd, db_path = tempfile.mkstemp()

    test_app = create_app(
        config_overrides={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": False,
            "JWT_SECRET": "test-secret",
            "JWT_EXPIRATION": 3600,
        }
    )

    # Create the database and the database tables
    with test_app.app_context():
        db.create_all()
        _populate_db()
        yield test_app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing protected routes."""
    from app.utils import generate_token

    # User ID 1 is created in _populate_db
    token = generate_token(1)
    return {"Authorization": f"Bearer {token}"}


def _populate_db():
    """Add sample data to the database."""
    # Create test users
    user1 = User(
        username="testuser1",
        password="password123",
        name="Test User 1",
        email="test1@example.com",
        photo="profile1.jpg",
    )

    user2 = User(
        username="testuser2",
        password="password123",
        name="Test User 2",
        email="test2@example.com",
        photo="profile2.jpg",
    )

    user3 = User(
        username="testuser3",
        password="password123",
        name="Test User 3",
        email="test3@example.com",
        photo="profile3.jpg",
    )

    # Additional users for match testing
    user4 = User(
        username="testuser4",
        password="password123",
        name="Test User 4",
        email="test4@example.com",
        photo="profile4.jpg",
    )

    user5 = User(
        username="testuser5",
        password="password123",
        name="Test User 5",
        email="test5@example.com",
        photo="profile5.jpg",
    )

    user6 = User(
        username="testuser6",
        password="password123",
        name="Test User 6",
        email="test6@example.com",
        photo="profile6.jpg",
    )

    user7 = User(
        username="testuser7",
        password="password123",
        name="Test User 7",
        email="test7@example.com",
        photo="profile7.jpg",
    )

    db.session.add_all([user1, user2, user3, user4, user5, user6, user7])
    db.session.commit()

    # Create test profiles
    profile1 = Profile(
        user_id_fk=user1.id,
        description="Test profile 1",
        parish="Kingston",
        biography="This is a test biography for user 1",
        sex="Male",
        race="Black",
        birth_year=1990,
        height=180.5,
        fav_cuisine="Italian",
        fav_colour="Blue",
        fav_school_subject="Mathematics",
        political=True,
        religious=False,
        family_oriented=True,
    )

    profile2 = Profile(
        user_id_fk=user2.id,
        description="Test profile 2",
        parish="St. Andrew",
        biography="This is a test biography for user 2",
        sex="Female",
        race="Asian",
        birth_year=1995,
        height=165.0,
        fav_cuisine="Japanese",
        fav_colour="Red",
        fav_school_subject="Science",
        political=False,
        religious=True,
        family_oriented=True,
    )

    # Profile that should match profile1 (meets all criteria)
    # - Age within +/- 5 years (1992 is within 5 years of 1990)
    # - Height difference between 3-10 inches (175.0 is 5.5 inches less than 180.5)
    # - Matches on 3+ preferences (fav_cuisine, fav_colour, family_oriented)
    profile3 = Profile(
        user_id_fk=user3.id,
        description="Test profile 3",
        parish="St. Catherine",
        biography="This is a test biography for user 3",
        sex="Female",
        race="Black",
        birth_year=1992,
        height=175.0,
        fav_cuisine="Italian",  # Match
        fav_colour="Blue",  # Match
        fav_school_subject="English",
        political=False,
        religious=True,
        family_oriented=True,  # Match
    )

    # Profile that shouldn't match profile1 due to age (outside +/- 5 years)
    profile4 = Profile(
        user_id_fk=user4.id,
        description="Test profile 4",
        parish="Portland",
        biography="This is a test biography for user 4",
        sex="Female",
        race="White",
        birth_year=1980,  # 10 years older than profile1
        height=175.0,  # Valid height difference
        fav_cuisine="Italian",  # Match
        fav_colour="Blue",  # Match
        fav_school_subject="Mathematics",  # Match
        political=True,  # Match
        religious=False,  # Match
        family_oriented=True,  # Match
    )

    # Profile that shouldn't match profile1 due to height (outside 3-10 inch difference)
    profile5 = Profile(
        user_id_fk=user5.id,
        description="Test profile 5",
        parish="Clarendon",
        biography="This is a test biography for user 5",
        sex="Female",
        race="Mixed",
        birth_year=1991,  # Valid age
        height=179.0,  # Only 1.5 inches difference, less than required 3 inches
        fav_cuisine="Italian",  # Match
        fav_colour="Blue",  # Match
        fav_school_subject="Mathematics",  # Match
        political=True,  # Match
        religious=False,  # Match
        family_oriented=True,  # Match
    )

    # Profile that shouldn't match profile1 due to insufficient preference matches (only 2 matches)
    profile6 = Profile(
        user_id_fk=user6.id,
        description="Test profile 6",
        parish="St. Thomas",
        biography="This is a test biography for user 6",
        sex="Female",
        race="Black",
        birth_year=1993,  # Valid age
        height=172.0,  # Valid height difference
        fav_cuisine="Italian",  # Match
        fav_colour="Blue",  # Match
        fav_school_subject="History",
        political=False,
        religious=True,
        family_oriented=False,
    )

    # Another profile that should match profile1
    profile7 = Profile(
        user_id_fk=user7.id,
        description="Test profile 7",
        parish="Manchester",
        biography="This is a test biography for user 7",
        sex="Female",
        race="Indian",
        birth_year=1988,  # Valid age (within 5 years)
        height=173.0,  # Valid height difference
        fav_cuisine="Italian",  # Match
        fav_colour="Green",
        fav_school_subject="Mathematics",  # Match
        political=True,  # Match
        religious=False,  # Match
        family_oriented=True,  # Match
    )

    db.session.add_all(
        [profile1, profile2, profile3, profile4, profile5, profile6, profile7]
    )
    db.session.commit()

    # Create test favourites
    fav1 = Favourite(user_id_fk=1, fav_profile_id_fk=profile1.id)
    fav2 = Favourite(user_id_fk=2, fav_profile_id_fk=profile1.id)
    fav3 = Favourite(user_id_fk=3, fav_profile_id_fk=profile1.id)

    db.session.add_all([fav1, fav2, fav3])
    db.session.commit()
