from app.models import User, Profile, Favourite, db


def test_database_modification(client, app):
    """Test that verifies database modifications are cleaned up between tests."""
    # Add a new user to the database
    with app.app_context():
        new_user = User(
            username="temporary_user",
            password="temp_password",
            name="Temporary User",
            email="temp@example.com",
            photo="temp.jpg",
        )
        db.session.add(new_user)
        db.session.commit()

        # Verify the user was added
        user = User.query.filter_by(username="temporary_user").first()
        assert user is not None
        assert user.name == "Temporary User"


def test_database_is_clean(client, app):
    """Test that verifies the database is clean after the previous test."""
    # Check that the temporary user from the previous test doesn't exist
    with app.app_context():
        user = User.query.filter_by(username="temporary_user").first()
        assert user is None

        # Verify that only the original test users exist
        users = User.query.all()
        usernames = [user.username for user in users]
        assert "testuser1" in usernames
        assert "testuser2" in usernames
        assert "testuser3" in usernames
        assert len(users) == 7


def test_add_and_verify_favourite(client, app):
    """Test adding a new favourite and verifying it exists."""
    # Add a new favourite relationship
    with app.app_context():
        new_favourite = Favourite(user_id_fk=1, fav_profile_id_fk=3)
        db.session.add(new_favourite)
        db.session.commit()

        # Verify the favourite was added
        favourite = Favourite.query.filter_by(user_id_fk=1, fav_profile_id_fk=3).first()
        assert favourite is not None


def test_favourites_are_reset(client, app):
    """Test that favourites are reset to initial state after previous test."""
    # Check that the database has been reset to its initial state
    with app.app_context():
        # Verify only the original favourites exist
        favourites = Favourite.query.all()
        assert len(favourites) == 3

        # Check specific favourite relationships from the initial setup
        fav1 = Favourite.query.filter_by(user_id_fk=1, fav_profile_id_fk=1).first()
        assert fav1 is not None

        fav2 = Favourite.query.filter_by(user_id_fk=2, fav_profile_id_fk=1).first()
        assert fav2 is not None

        fav3 = Favourite.query.filter_by(user_id_fk=3, fav_profile_id_fk=1).first()
        assert fav3 is not None


def test_profile_modification_and_cleanup(client, app):
    """Test that modifies a profile and verifies cleanup works."""
    # Modify an existing profile
    with app.app_context():
        profile = Profile.query.filter_by(user_id_fk=1).first()
        original_description = profile.description
        profile.description = "Modified description for testing"
        profile.parish = "Modified parish"
        db.session.commit()

        # Verify the profile was modified
        modified_profile = Profile.query.filter_by(user_id_fk=1).first()
        assert modified_profile.description == "Modified description for testing"
        assert modified_profile.parish == "Modified parish"


def test_profile_is_reset(client, app):
    """Test that verifies the profile was reset after the previous test."""
    # Check that the profile has been reset to its initial state
    with app.app_context():
        profile = Profile.query.filter_by(user_id_fk=1).first()
        assert profile.description == "Test profile 1"
        assert profile.parish == "Kingston"
