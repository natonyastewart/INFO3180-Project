import os
from flask import Blueprint, current_app, jsonify, request, g, send_from_directory
from sqlalchemy import desc, func, select
from sqlalchemy.orm import joinedload
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
    ProfileWithUserSchema,
)

profiles_bp = Blueprint("profiles", __name__)


@profiles_bp.route("/uploads/<filename>", methods=["GET"])
def get_upload(filename):
    """Serve images from the uploads folder"""
    return send_from_directory(
        os.path.join(os.getcwd(), current_app.config["UPLOAD_FOLDER"]),
        filename,
        as_attachment=True,
    )


@profiles_bp.route("/profiles", methods=["GET", "POST"])
@token_required
def handle_profiles():
    if request.method == "GET":
        return get_profiles()
    else:
        return create_profile()


def get_self_profiles():
    user_id = g.current_user.id

    # Use eager loading to fetch the user relationship in a single query
    profiles = db.session.scalars(
        select(Profile)
        .options(joinedload(Profile.user))
        .where(Profile.user_id_fk == user_id)
    ).all()

    # Use ProfileWithUserSchema to include user data in the response
    profile_schema = ProfileWithUserSchema()
    return [
        profile_schema.dump(
            {
                **profile.to_dict(),
                "user": {
                    "id": profile.user.id,
                    "name": profile.user.name,
                    "photo": profile.user.photo,
                },
            }
        )
        for profile in profiles
    ]


def get_profiles():
    """
    Get all profiles for authenticated user
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

        # Fetch the profile with user data and return it
        created_profile = (
            db.session.query(Profile).options(joinedload(Profile.user)).get(profile.id)
        )

        profile_schema = ProfileWithUserSchema()
        profile_data = profile_schema.dump(
            {
                **created_profile.to_dict(),
                "user": {
                    "id": created_profile.user.id,
                    "name": created_profile.user.name,
                    "photo": created_profile.user.photo,
                },
            }
        )

        return (
            jsonify(generate_response(data=profile_data)),
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
    # Use joinedload to fetch the profile with its related user in a single query
    profile = (
        db.session.query(Profile).options(joinedload(Profile.user)).get(profile_id)
    )

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

    # Use marshmallow schema to serialize the profile with user data
    profile_schema = ProfileWithUserSchema()
    profile_data = profile_schema.dump(
        {
            **profile.to_dict(),
            "user": {
                "id": profile.user.id,
                "name": profile.user.name,
                "photo": profile.user.photo,
            },
        }
    )

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
        fav_profile_id_fk=data["profileId"],
    )
    db.session.add(new_fav)
    db.session.commit()
    return (
        jsonify(generate_response(data=new_fav.to_dict())),
        201,
    )


@profiles_bp.route("/profiles/favourite/<int:fav_id>", methods=["DELETE"])
@token_required
@has_profile_required
def remove_favourite(fav_id):
    fav = db.session.get(Favourite, fav_id)
    if not fav:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "Favourite not found"},
                )
            ),
            404,
        )

    if fav.user_id_fk != g.current_user.id:
        return (
            jsonify(
                generate_response(
                    success=False,
                    errors={"error": "Forbidden: You do not own this favourite"},
                )
            ),
            403,
        )

    db.session.delete(fav)
    db.session.commit()
    return (
        jsonify(generate_response(data={"message": "Favourite deleted successfully"})),
        200,
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

    # Use eager loading to fetch user data in a single query
    potential_matches_query = Profile.query.options(joinedload(Profile.user))

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
    query = Profile.query.join(User).options(
        joinedload(Profile.user)
    )  # Eager load user data
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
    q = query.filter(*filters)

    if validated_params.get("limit"):
        q = q.limit(validated_params["limit"])

    results = q.all()

    # Use marshmallow schema to serialize the results with user data
    profile_schema = ProfileWithUserSchema(many=True)
    profile_data = profile_schema.dump(
        [
            {
                **profile.to_dict(),
                "user": {
                    "id": profile.user.id,
                    "name": profile.user.name,
                    "photo": profile.user.photo,
                },
            }
            for profile in results
        ]
    )

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
                    success=False,
                    errors={"error": "Threshold must be between 1 and 100"},
                )
            ),
            400,
        )

    user_id = g.current_user.id

    # Get top favoured profiles with count
    fav_profiles = db.session.scalars(
        select(Favourite)
        .options(joinedload(Favourite.favourited_profile))
        .where(Favourite.user_id_fk == user_id)
        .limit(threshold)
    ).all()

    # Use the schema to validate and serialize the data
    schema = ProfileSchema(many=True)
    result = []

    for profile in fav_profiles:
        profile_dict = profile.favourited_profile.to_dict()
        profile_user_dict = profile.favourited_profile.user.to_dict()
        profile_dict["profile"] = {
            **profile.favourited_profile.to_dict(),
            "user": {
                "name": profile_user_dict.get("name"),
                "photo": profile_user_dict.get("photo"),
                "id": profile_user_dict.get("id"),
                "username": profile_user_dict.get("username"),
            },
        }
        result.append(profile_dict)

    return jsonify(generate_response(data=result))
