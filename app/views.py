"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")





@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_Profiles_Detail():
    profile = Profile.query.get_or_404(profile_id)
    return jsonify({
        'id': profile.id,
        'user_id_fk': profile.user_id_fk,
        'description': profile.description,
        'parish': profile.parish,
        'biography': profile.biography,
        'sex': profile.sex,
        'race': profile.race,
        'birth_year': profile.birth_year,
        'height': profile.height,
        'fav_cuisine': profile.fav_cuisine,
        'fav_colour': profile.fav_colour,
        'fav_school_subject': profile.fav_school_subject,
        'political': profile.political,
        'religious': profile.religious,
        'family_oriented': profile.family_oriented
    })


@app.route('/api/profiles/<user_id>/favourite', methods=['POST'])
def add_Favourite():
    data = request.get_json()
    new_fav = Favorite(
        id=data['user_id'],
        user_id_fk=data['user_id_fk'],
        fav_user_id_fk=data['fav_user_id_fk'],
    )
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({
        'message': f'Profile {data["profile_id"]} added to favorites of user {user_id}'
    }), 201


@app.route('/api/profiles/matches/<profile_id> ', methods=['GET'])
def get_Specific_Profile_List():
    """Get matches for specific profile"""
    # Implement matching logic
    return jsonify({
        'matches': [],
        'profile_id': profile_id
    })

@app.route('/api/search', methods=['GET'])
def search_profiles():
    """Search profiles by name, birth year, sex, race or combination"""
    # Get query parameters
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')

    # Build query filters
    query = Profile.query.join(User)  # Assuming Profile has user relationship
    filters = []

    if name:
        filters(User.name.ilike(f'%{name}%'))
    if birth_year:
        filters.append(Profile.birth_year == birth_year)
    if sex:
        filters.append(Profile.sex == sex)
    if race:
        filters.append(Profile.race == race)

    # Apply filters and execute query
    results = query.filter(*filters).all()

    return jsonify([{
        'user_id': profile.user_id_fk,
        'name': profile.user.name,  # Assuming User model has name field
        'birth_year': profile.birth_year,
        'sex': profile.sex,
        'race': profile.race,
        'parish': profile.parish
    } for profile in results])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get details of a specific user"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'registration_date': user.registration_date.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    })

@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    """Get list of users favored by specified user"""
    favourites = Favorite.query.filter_by(user_id_fk=user_id).all()
    return jsonify([{
        'favoured_user_id': fav.fav_user_id_fk,
        'favoured_user_name': User.query.get(fav.fav_user_id_fk).name,
        'date_added': fav.timestamp.isoformat()
    } for fav in favourites])

@app.route('/api/users/favourites/<int:N>', methods=['GET'])
def get_top_favourites(N):
    """Get top N most favoured users"""
    if N < 1 or N > 100:
        return jsonify({'error': 'N must be between 1 and 100'}), 400

    # Get top favoured users with count
    top_users = db.session.query(
        Favorite.fav_user_id_fk,
        func.count(Favorite.fav_user_id_fk).label('favourite_count'),
        User.name
    ).join(User).group_by(Favorite.fav_user_id_fk).order_by(desc('favourite_count')).limit(N).all()

    return jsonify([{
        'user_id': user_id,
        'name': name,
        'favourite_count': count
    } for user_id, count, name in top_users])


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