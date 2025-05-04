from flask import Blueprint, jsonify, request, g
from sqlalchemy import desc, func, select
from marshmallow import ValidationError
from app.models import Favourite, Profile, User, db
from app.utils import generate_response, token_required, has_profile_required
from app.schemas import (
    CreateProfileDto,
    FavouriteRequestSchema,
    ProfileSchema,
    SearchRequestSchema,
    UserSchema,
    FavouriteSchema,
    TopFavouriteSchema,
    ProfileWithUserSchema,
    UserInfoSchema,
)

profiles_bp = Blueprint("profiles", __name__)


@profiles_bp.route("/profiles", methods=["GET", "POST"])
@token_required
def handle_profiles():
    if request.method == "GET":
        return get_profiles()
    else:
        return create_profile()


def get_self_profiles():
    user_id = g.current_user.id

    profiles = db.session.scalars(
        select(Profile).where(Profile.user_id_fk == user_id)
    ).all()

    profile_schema = ProfileSchema()
    return [profile_schema.dump(profile.to_dict()) for profile in profiles]


def get_profiles():
    """
    Get all profiles fdr authenticated user
    """
    return jsonify(generate_response(data=get_self_profiles()))


def create_profile():
    user_id = g.current_user.id

    if len(get_self_profiles()) == 3:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={
                        "error": "You already have 3 profiles, you cannot create any more."
                    },
                )
            ),
            400,
        )

    body = request.get_json()
    schema = CreateProfileDto()

    try:
        data = schema.load(body)

        profile = Profile(user_id_fk=user_id, **data)
        db.session.add(profile)
        db.session.commit()

        return (
            jsonify(generate_response(data=profile.to_dict())),
            201,
        )
    except ValidationError as err:
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=err.messages
                )
            ),
            400,
        )


@profiles_bp.route("/profiles/<profile_id>", methods=["GET"])
@token_required
def get_profiles_detail(profile_id):
    profile = db.session.get(Profile, profile_id)

    if not profile:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "Profile not found"},
                )
            ),
            404,
        )

    # Use marshmallow schema to serialize the profile
    profile_schema = ProfileSchema()
    profile_data = profile_schema.dump(profile)

    return jsonify(generate_response(data=profile_data))


@profiles_bp.route("/profiles/favourite", methods=["POST"])
@token_required
@has_profile_required
def add_favourite():
    # Validate request data using marshmallow schema
    schema = FavouriteRequestSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=err.messages
                )
            ),
            400,
        )

    new_fav = Favourite(
        user_id_fk=g.current_user.id,
        fav_user_id_fk=data["userId"],
    )
    db.session.add(new_fav)
    db.session.commit()
    return (
        jsonify(generate_response(data=new_fav.to_dict())),
        201,
    )


@profiles_bp.route("/profiles/matches/<profile_id>", methods=["GET"])
@token_required
@has_profile_required
def get_profile_matches(profile_id):
    """
    Finds and returns profiles matching the given profile_id based on specific criteria.
    Criteria:
    1. Age within +/- 5 years.
    2. Not the same user.
    3. Height difference between 3 and 10 inches (inclusive).
    4. Match on at least 3 of: fav_cuisine, fav_colour, fav_school_subject,
       political, religious, family_oriented.
    """
    source_profile = db.session.get(Profile, profile_id)

    if not source_profile:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "Profile not found"},
                )
            ),
            404,
        )

    if source_profile.user_id_fk != g.current_user.id:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "Forbidden: You do not own this profile"},
                )
            ),
            403,
        )

    # Requirement 1: Age Range (+/- 5 years) -> Calculate birth year range
    min_birth_year = source_profile.birth_year - 5
    max_birth_year = source_profile.birth_year + 5

    # Requirement 3: Height Range (absolute difference 3-10 inches)
    source_height = source_profile.height

    # Requirement 4: Fields to compare for commonality
    match_fields = [
        "fav_cuisine",
        "fav_colour",
        "fav_school_subject",
        "political",
        "religious",
        "family_oriented",
    ]

    potential_matches_query = Profile.query

    potential_matches_query = potential_matches_query.filter(
        Profile.birth_year.between(min_birth_year, max_birth_year)
    )

    potential_matches_query = potential_matches_query.filter(
        Profile.user_id_fk != source_profile.user_id_fk
    )

    potential_matches_query = potential_matches_query.filter(
        func.abs(Profile.height - source_height).between(3, 10)
    )

    candidate_profiles = potential_matches_query.all()

    final_matches = []
    for candidate in candidate_profiles:
        match_count = 0
        for field in match_fields:
            if getattr(source_profile, field) == getattr(candidate, field):
                match_count += 1

        if match_count >= 3:
            final_matches.append(candidate)

    # Transform the results into the expected format
    detailed_results = []
    for profile in final_matches:
        profile_dict = profile.to_dict()
        user_info = profile.user.to_dict()
        profile_dict["user"] = {
            "name": user_info.get("name"),
            "photo": user_info.get("photo"),
            "id": user_info.get("id"),
        }
        detailed_results.append(profile_dict)

    # Use the schema to validate and serialize the data
    schema = ProfileWithUserSchema(many=True)
    result = schema.dump(detailed_results)

    return jsonify(data=result), 200


@profiles_bp.route("/search", methods=["GET"])
@token_required
def search_profiles():
    """Search profiles by name, birth year, sex, race or combination"""
    # Get query parameters
    query_params = {
        "name": request.args.get("name"),
        "birth_year": request.args.get("birth_year"),
        "sex": request.args.get("sex"),
        "race": request.args.get("race"),
    }

    # Convert birth_year to int if it exists
    if query_params["birth_year"]:
        try:
            query_params["birth_year"] = int(query_params["birth_year"])
        except ValueError:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Validation error",
                        errors={"birth_year": ["Must be a valid integer"]},
                    )
                ),
                400,
            )

    # Validate query parameters using marshmallow schema
    schema = SearchRequestSchema()
    try:
        validated_params = schema.load(query_params)
    except ValidationError as err:
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=err.messages
                )
            ),
            400,
        )

    # Build query filters
    query = Profile.query.join(User)  # Assuming Profile has user relationship
    filters = []

    if validated_params.get("name"):
        filters.append(User.name.ilike(f"%{validated_params['name']}%"))
    if validated_params.get("birth_year"):
        filters.append(Profile.birth_year == validated_params["birth_year"])
    if validated_params.get("sex"):
        filters.append(Profile.sex == validated_params["sex"])
    if validated_params.get("race"):
        filters.append(Profile.race == validated_params["race"])

    filters.append(Profile.user_id_fk != g.current_user.id)

    # Apply filters and execute query
    results = query.filter(*filters).all()

    # Use marshmallow schema to serialize the results
    profile_schema = ProfileSchema(many=True)
    profile_data = profile_schema.dump(results)

    return jsonify(
        generate_response(
            data=profile_data,
            message=f"Found {len(results)} matching profiles",
        )
    )


@profiles_bp.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """Get details of a specific user"""
    user = db.session.scalars(select(User).where(User.id == user_id)).first()

    if not user:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "User not found"},
                )
            ),
            404,
        )

    # Use marshmallow schema to serialize the user
    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return jsonify(
        generate_response(
            data={
                "name": user_data["name"],
                "username": user_data["username"],
                "photo": user_data["photo"],
                "id": user_data["id"],
                "date_joined": user_data["date_joined"],
            }
        )
    )


@profiles_bp.route("/users/favourites", methods=["GET"])
@token_required
@has_profile_required
def get_user_favourites():
    """Get list of users favored by specified user"""
    user_id = g.current_user.id
    favourites = Favourite.query.filter_by(user_id_fk=user_id).all()

    # Use marshmallow schema to serialize the favourites
    favourite_schema = FavouriteSchema(many=True)
    favourite_data = favourite_schema.dump(favourites)

    return jsonify(generate_response(data=favourite_data))


@profiles_bp.route("/users/favourites/<int:threshold>", methods=["GET"])
@token_required
def get_top_favourites(threshold):
    """Get top N most favoured users"""
    if threshold < 1 or threshold > 100:
        return (
            jsonify(
                generate_response(
                    success=False, errors={"error": "N must be between 1 and 100"}
                )
            ),
            400,
        )

    # Get top favoured users with count
    top_users = (
        db.session.query(
            Favourite.fav_user_id_fk,
            func.count(Favourite.fav_user_id_fk).label("favourite_count"),
            User.name,
        )
        .join(User, Favourite.fav_user_id_fk == User.id)  # <-- specify join condition
        .group_by(Favourite.fav_user_id_fk, User.name)
        .order_by(desc("favourite_count"))
        .limit(threshold)
        .all()
    )

    # Transform the results into the expected format
    data = [
        {
            "user_id": user.fav_user_id_fk,
            "name": user.name,
            "favourite_count": user.favourite_count,
        }
        for user in top_users
    ]

    # Use the schema to validate and serialize the data
    schema = TopFavouriteSchema(many=True)
    result = schema.dump(data)

    return jsonify(generate_response(data=result))
