import os
from flask import Blueprint, request, jsonify, current_app, g
from sqlalchemy import select
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from marshmallow import ValidationError
from app.models import User, db
from app.utils import (
    generate_response,
    generate_token,
    generate_refresh_token,
    token_required,
    refresh_token_required,
)
from app.schemas import RegistrationRequestSchema, LoginRequestSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    """
    # Get form data
    data = request.json if request.is_json else request.form

    # Validate using Marshmallow schema
    schema = RegistrationRequestSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=err.messages
                )
            ),
            400,
        )

    # Additional validation for existing username/email
    if User.query.filter_by(username=validated_data["username"]).first():
        errors = {"username": ["Username already exists"]}
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=errors
                )
            ),
            400,
        )

    if User.query.filter_by(email=validated_data["email"]).first():
        errors = {"email": ["Email already exists"]}
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=errors
                )
            ),
            400,
        )

    # Handle file upload if there's a photo
    photo_filename = None
    print(len(request.files))
    if "photo" in request.files:
        photo = request.files["photo"]
        filename = secure_filename(photo.filename)
        photo_filename = (
            f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{filename}"
        )
        # Save the file
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], photo_filename)
        print(f"Saving file to {path}")
        photo.save(path)

    # Create new user
    new_user = User(
        username=validated_data["username"],
        password=validated_data["password"],
        name=validated_data["name"],
        email=validated_data["email"],
        photo=photo_filename,
    )

    # Save to database
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT tokens
    access_token = generate_token(new_user.id)
    refresh_token = generate_refresh_token(new_user.id)

    return (
        jsonify(
            generate_response(
                success=True,
                message="User registered successfully",
                data={
                    "user": new_user.to_dict(),
                    "token": access_token,
                    "refreshToken": refresh_token,
                },
            )
        ),
        201,
    )


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Authenticate a user and return JWT tokens
    """
    data = request.json if request.is_json else request.form

    # Validate using Marshmallow schema
    schema = LoginRequestSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return (
            jsonify(
                generate_response(
                    success=False, message="Validation error", errors=err.messages
                )
            ),
            400,
        )

    # Find user by username
    user = db.session.scalars(
        select(User).where(User.username == validated_data["username"])
    ).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(validated_data["password"]):
        return (
            jsonify(
                generate_response(
                    success=False,
                    message="Invalid username or password",
                    errors={"auth": ["Invalid username or password"]},
                )
            ),
            401,
        )

    # Generate JWT tokens
    access_token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    return (
        jsonify(
            generate_response(
                success=True,
                message="Login successful",
                data={
                    "user": user.to_dict(),
                    "token": access_token,
                    "refreshToken": refresh_token,
                },
            )
        ),
        200,
    )


@auth_bp.route("/auth/refresh", methods=["POST"])
@refresh_token_required
def refresh():
    """
    Refresh an access token using a refresh token
    """
    # User is already authenticated via the refresh_token_required decorator
    # and available in g.current_user

    # Generate new access token
    access_token = generate_token(g.current_user.id)

    return (
        jsonify(
            generate_response(
                success=True,
                message="Token refreshed successfully",
                data={"token": access_token},
            )
        ),
        200,
    )


@auth_bp.route("/auth/logout", methods=["POST"])
@token_required
def logout():
    """
    Note: The server doesn't really need to handle logouts for the scope of this project
    since token blacklists/revocations aren't a thing. The client should simply remove
    the token from storage in order to logout a user.
    """
    return jsonify(generate_response(success=True, message="Logout successful")), 200
