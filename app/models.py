# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    photo = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    description = db.Column(db.String(500))
    parish = db.Column(db.String(50))
    biography = db.Column(db.Text)  
    sex = db.Column(db.String(10))  
    race = db.Column(db.String(50))
    birth_year = db.Column(db.Integer)
    height = db.Column(db.Float)  
    fav_cuisine = db.Column(db.String(50))
    fav_color = db.Column(db.String(30))
    fav_school_subject = db.Column(db.String(50))
    political = db.Column(db.Boolean, default=False)
    religious = db.Column(db.Boolean, default=False)
    family_oriented = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='profile', uselist=False)


class Favourite(db.Model):
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id_fk], backref='favourites_given')
    fav_user = db.relationship('User', foreign_keys=[fav_user_id_fk], backref='favourites_received')
