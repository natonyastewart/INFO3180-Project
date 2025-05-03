import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from marshmallow import ValidationError
from app.models import User, db
from app.utils import generate_response, generate_token, token_required
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
    if "photo" in request.files:
        photo = request.files["photo"]
        if photo.filename:
            # Secure the filename
            filename = secure_filename(photo.filename)
            # Generate a unique filename
            photo_filename = (
                f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{filename}"
            )
            # Save the file
            photo.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], photo_filename)
            )

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

    # Generate JWT token
    token = generate_token(new_user.id)

    return (
        jsonify(
            generate_response(
                success=True,
                message="User registered successfully",
                data={"user": new_user.to_dict(), "token": token},
            )
        ),
        201,
    )


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Authenticate a user and return a JWT token
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
    user = User.query.filter_by(username=validated_data["username"]).first()

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

    # Generate JWT token
    token = generate_token(user.id)

    return (
        jsonify(
            generate_response(
                success=True,
                message="Login successful",
                data={"user": user.to_dict(), "token": token},
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
