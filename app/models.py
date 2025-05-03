from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profiles = db.relationship("Profile", backref="user", lazy=True)
    favourites = db.relationship(
        "Favourite", foreign_keys="Favourite.user_id_fk", backref="user", lazy=True
    )

    def __init__(self, username, password, name, email, photo=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.photo = photo

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "photo": self.photo,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    parish = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(100), nullable=False)
    fav_colour = db.Column(db.String(50), nullable=False)
    fav_school_subject = db.Column(db.String(100), nullable=False)
    political = db.Column(db.Boolean, nullable=False)
    religious = db.Column(db.Boolean, nullable=False)
    family_oriented = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        user_id_fk,
        description,
        parish,
        biography,
        sex,
        race,
        birth_year,
        height,
        fav_cuisine,
        fav_colour,
        fav_school_subject,
        political,
        religious,
        family_oriented,
    ):
        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id_fk,
            "description": self.description,
            "parish": self.parish,
            "biography": self.biography,
            "sex": self.sex,
            "race": self.race,
            "birth_year": self.birth_year,
            "height": self.height,
            "fav_cuisine": self.fav_cuisine,
            "fav_colour": self.fav_colour,
            "fav_school_subject": self.fav_school_subject,
            "political": self.political,
            "religious": self.religious,
            "family_oriented": self.family_oriented,
        }

    def calculate_age(self):
        current_year = datetime.now(timezone.utc).year
        return current_year - self.birth_year


class Favourite(db.Model):
    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Define a unique constraint to prevent duplicate favorites
    __table_args__ = (
        db.UniqueConstraint("user_id_fk", "fav_user_id_fk", name="unique_favourite"),
    )

    # Relationship to get the favorited user's details
    favourited_user = db.relationship(
        "User",
        foreign_keys=[fav_user_id_fk],
        backref=db.backref("favourited_by", lazy=True),
    )

    def __init__(self, user_id_fk, fav_user_id_fk):
        self.user_id_fk = user_id_fk
        self.fav_user_id_fk = fav_user_id_fk

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id_fk,
            "fav_user_id": self.fav_user_id_fk,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
