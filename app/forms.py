from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange
from datetime import datetime, timezone

class RegistrationForm(FlaskForm):
    """
    Form for user registration
    """
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=80, message="Username must be between 3 and 80 characters")
    ])
    password = StringField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(max=120, message="Name must be less than 120 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format"),
        Length(max=120, message="Email must be less than 120 characters")
    ])
    
    # Photo is handled separately since it's a file upload

class LoginForm(FlaskForm):
    """
    Form for user login
    """
    username = StringField('Username', validators=[
        DataRequired(message="Username is required")
    ])
    password = StringField('Password', validators=[
        DataRequired(message="Password is required")
    ])

class ProfileForm(FlaskForm):
    """
    Form for profile creation/updating
    """
    description = StringField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(max=255, message="Description must be less than 255 characters")
    ])
    parish = StringField('Parish', validators=[
        DataRequired(message="Parish is required"),
        Length(max=100, message="Parish must be less than 100 characters")
    ])
    biography = TextAreaField('Biography', validators=[
        DataRequired(message="Biography is required")
    ])
    sex = StringField('Sex', validators=[
        DataRequired(message="Sex is required"),
        Length(max=20, message="Sex must be less than 20 characters")
    ])
    race = StringField('Race', validators=[
        DataRequired(message="Race is required"),
        Length(max=100, message="Race must be less than 100 characters")
    ])
    
    # Validate birth year to ensure user is at least 18 years old
    def validate_birth_year(form, field):
        try:
            year = int(field.data)
            current_year = datetime.now(timezone.utc).year
            if year < 1900 or year > current_year - 18:
                raise ValidationError("Birth year must be between 1900 and " + str(current_year - 18))
        except (ValueError, TypeError):
            raise ValidationError("Birth year must be a valid number")
    
    birth_year = IntegerField('Birth Year', validators=[
        DataRequired(message="Birth year is required"),
        validate_birth_year
    ])
    
    # Validate height to ensure it's a reasonable value
    def validate_height(form, field):
        try:
            height = float(field.data)
            if height <= 0 or height > 300:  # Reasonable height range in cm
                raise ValidationError("Height must be a positive number less than 300")
        except (ValueError, TypeError):
            raise ValidationError("Height must be a valid number")
    
    height = FloatField('Height', validators=[
        DataRequired(message="Height is required"),
        validate_height
    ])
    
    fav_cuisine = StringField('Favorite Cuisine', validators=[
        DataRequired(message="Favorite cuisine is required"),
        Length(max=100, message="Favorite cuisine must be less than 100 characters")
    ])
    fav_colour = StringField('Favorite Colour', validators=[
        DataRequired(message="Favorite colour is required"),
        Length(max=50, message="Favorite colour must be less than 50 characters")
    ])
    fav_school_subject = StringField('Favorite School Subject', validators=[
        DataRequired(message="Favorite school subject is required"),
        Length(max=100, message="Favorite school subject must be less than 100 characters")
    ])
    political = BooleanField('Political')
    religious = BooleanField('Religious')
    family_oriented = BooleanField('Family Oriented')

class SearchForm(FlaskForm):
    """
    Form for profile searching
    """
    name = StringField('Name')
    birth_year = IntegerField('Birth Year', validators=[], default=None)
    sex = StringField('Sex')
    race = StringField('Race')