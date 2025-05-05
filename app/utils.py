import jwt
import datetime
from functools import wraps
from flask import request, jsonify, g, current_app

from app.models import User, db


def generate_response(success=True, message=None, data=None, errors=None):
    """
    Generate a standardized API response format

    Args:
        success (bool): Whether the request was successful
        message (str, optional): Message to include in the response
        data (any, optional): Data to include in the response
        errors (dict, optional): Dictionary of field-level errors

    Returns:
        dict: Standardized API response
    """
    response = {"success": success}

    if message is not None:
        response["message"] = message

    if data is not None:
        response["data"] = data

    if errors is not None:
        response["errors"] = errors

    return response


def generate_token(user_id, token_type="access"):
    """
    Generate a JWT token for authentication

    Args:
        user_id (int): ID of the user to generate token for
        token_type (str): Type of token to generate ("access" or "refresh")

    Returns:
        str: JWT token
    """
    expiration = current_app.config["JWT_EXPIRATION"]
    if token_type == "refresh":
        expiration = current_app.config["JWT_REFRESH_EXPIRATION"]

    payload = {
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=expiration),
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "sub": user_id,
        "type": token_type,
    }

    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def generate_refresh_token(user_id):
    """
    Generate a JWT refresh token

    Args:
        user_id (int): ID of the user to generate token for

    Returns:
        str: JWT refresh token
    """
    return generate_token(user_id, token_type="refresh")


def decode_token(token):
    """
    Decode a JWT token

    Args:
        token (str): JWT token to decode

    Returns:
        dict: Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token, current_app.config["JWT_SECRET"], algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator for routes that require authentication

    Args:
        f (function): Function to wrap

    Returns:
        function: Wrapped function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Authentication token is missing",
                        errors={"auth": ["Authentication token is required"]},
                    )
                ),
                401,
            )

        # Decode token
        payload = decode_token(token)
        if not payload:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Invalid or expired token",
                        errors={"auth": ["Invalid or expired token"]},
                    )
                ),
                401,
            )

        # Check if token is an access token
        if payload.get("type") != "access":
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Invalid token type",
                        errors={"auth": ["Invalid token type"]},
                    )
                ),
                401,
            )

        # Get user from database
        user = db.session.get(User, payload["sub"])
        if not user:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="User not found",
                        errors={"auth": ["User not found"]},
                    )
                ),
                401,
            )

        # Store user in flask g object for use in route function
        g.current_user = user

        return f(*args, **kwargs)

    return decorated


def refresh_token_required(f):
    """
    Decorator for routes that require a refresh token

    Args:
        f (function): Function to wrap

    Returns:
        function: Wrapped function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Refresh token is missing",
                        errors={"auth": ["Refresh token is required"]},
                    )
                ),
                401,
            )

        # Decode token
        payload = decode_token(token)
        if not payload:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Invalid or expired refresh token",
                        errors={"auth": ["Invalid or expired refresh token"]},
                    )
                ),
                401,
            )

        # Check if token is a refresh token
        if payload.get("type") != "refresh":
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Invalid token type",
                        errors={"auth": ["Invalid token type, refresh token required"]},
                    )
                ),
                401,
            )

        # Get user from database
        user = db.session.get(User, payload["sub"])
        if not user:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="User not found",
                        errors={"auth": ["User not found"]},
                    )
                ),
                401,
            )

        # Store user in flask g object for use in route function
        g.current_user = user

        return f(*args, **kwargs)

    return decorated


def has_profile_required(f):
    """
    Decorator for routes that require a user to have at least one profile

    Args:
        f (function): Function to wrap

    Returns:
        function: Wrapped function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.current_user

        if not user.profiles:
            return (
                jsonify(
                    generate_response(
                        success=False,
                        message="Profile required",
                        errors={
                            "profile": [
                                "You must create a profile before accessing this feature"
                            ]
                        },
                    )
                ),
                403,
            )

        return f(*args, **kwargs)

    return decorated


def profile_is_complete(profile):
    """
    Check if a profile has all required fields filled out

    Args:
        profile (Profile): Profile to check

    Returns:
        bool: True if profile is complete, False otherwise
    """
    required_fields = [
        "description",
        "parish",
        "biography",
        "sex",
        "race",
        "birth_year",
        "height",
        "fav_cuisine",
        "fav_colour",
        "fav_school_subject",
        "political",
        "religious",
        "family_oriented",
    ]

    for field in required_fields:
        if getattr(profile, field) is None:
            return False

    return True
