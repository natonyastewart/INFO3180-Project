# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, FloatField, SubmitField, BooleanField
from wtforms.validators import InputRequired, NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    description = StringField('Profile Description', validators=[InputRequired()], render_kw={"placeholder": "Brief description of yourself"})
    parish = StringField('Parish', validators=[InputRequired()], render_kw={'placeholder': 'Please enter your parish'})
    biography = TextAreaField('Biography', validators=[InputRequired()], render_kw={"rows": 5, "placeholder": "Tell us about yourself..."})
    sex = SelectField('Sex', choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        validators=[InputRequired()])
    
    race = StringField('Race/Ethnicity', validators=[InputRequired()])
    birth_year = IntegerField('Birth Year', validators=[InputRequired()], render_kw={"placeholder": "e.g. 1990"})
    height = FloatField('Height (cm)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 175.5"})
    
    fav_cuisine = StringField('Favorite Cuisine', validators=[InputRequired()], render_kw={"placeholder": "e.g. Jamaican, Italian"})
    fav_color = StringField('Favorite Color', validators=[InputRequired()])
    fav_school_subject = StringField('Favorite School Subject', validators=[InputRequired()])
    
    political = BooleanField('Political?')
    religious = BooleanField('Religious?')
    family_oriented = BooleanField('Family Oriented?')

    submit = SubmitField('Create Profile')