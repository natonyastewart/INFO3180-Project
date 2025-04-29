"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash
import os
from app.forms import LoginForm, ProfileForm
from app.models import User, Profile
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('profile.dashboard'))
        
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/api/profiles', methods=['GET'])
@login_required
def get_user_profiles():
    profiles = Profile.query.filter_by(user_id=current_user.id).all()

    if not profiles:
        return jsonify({
            'status': 'success',
            'message' : 'No profile found',
            'data' : []
        }), 200
    
    profiles_data = []
    for profile in profiles:
        profiles_data.append({
            'id': profile.id,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_color': profile.fav_color,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented,
            'created_at': profile.created_at.isoformat()
        })
    
    return jsonify({
        'status': 'success',
        'count': len(profiles_data),
        'data': profiles_data
    }), 200
    
@app.route('/api/profiles', methods=['POST'])
@login_required
def add_profile():
    if Profile.query.filter_by(user_id=current_user.id).count() >= 3:
        flash('You can only have up to 3 profiles', 'warning')
        return redirect(url_for('profile.dashboard'))
    
    form = ProfileForm()

    if form.validate_on_submit():
        new_profile = Profile(
            user_id=current_user.id,
            description=form.description.data,
            parish=form.parish.data,
            biography=form.biography.data,
            sex=form.sex.data,
            race=form.race.data,
            birth_year=form.birth_year.data,
            height=form.height.data,
            fav_cuisine=form.fav_cuisine.data,
            fav_color=form.fav_color.data,
            fav_school_subject=form.fav_school_subject.data,
            political=form.political.data,
            religious=form.religious.data,
            family_oriented=form.family_oriented.data
        )
            
        db.session.add(new_profile)
        db.session.commit()
            
        flash('Profile created successfully!', 'success')
        return redirect(url_for('profile.dashboard'))
    
    return render_template('profiles/create.html', form=form)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404