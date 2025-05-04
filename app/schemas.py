from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timezone


class UserSchema(Schema):
    """Schema for User model"""

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(
        required=True, validate=validate.Length(min=8), load_only=True
    )
    name = fields.Str(required=True, validate=validate.Length(max=120))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    photo = fields.Str(allow_none=True)
    date_joined = fields.DateTime(dump_only=True)


class CreateProfileDto(Schema):
    """Schema for creating a profile"""

    description = fields.Str(required=True, validate=validate.Length(max=255))
    parish = fields.Str(required=True, validate=validate.Length(max=100))
    biography = fields.Str(required=False)
    sex = fields.Str(required=True, validate=validate.Length(max=20))
    race = fields.Str(required=True, validate=validate.Length(max=100))
    birth_year = fields.Int(required=True)
    height = fields.Float(required=True)
    fav_cuisine = fields.Str(required=True, validate=validate.Length(max=100))
    fav_colour = fields.Str(required=True, validate=validate.Length(max=50))
    fav_school_subject = fields.Str(required=True, validate=validate.Length(max=100))
    political = fields.Bool(required=True)
    religious = fields.Bool(required=True)
    family_oriented = fields.Bool(required=True)

    @validates("birth_year")
    def _validate_birth_year(self, value, **kwargs):
        current_year = datetime.now(timezone.utc).year
        if value < 1900 or value > current_year - 18:
            raise ValidationError(
                f"Birth year must be between 1900 and {current_year - 18}"
            )

    @validates("height")
    def _validate_height(self, value, **kwargs):
        if value <= 0 or value > 300:  # Reasonable height range in cm
            raise ValidationError("Height must be a positive number less than 300")


class ProfileSchema(Schema):
    """Schema for Profile model"""

    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, attribute="user_id_fk")
    description = fields.Str(required=True, validate=validate.Length(max=255))
    parish = fields.Str(required=True, validate=validate.Length(max=100))
    biography = fields.Str(required=True)
    sex = fields.Str(required=True, validate=validate.Length(max=20))
    race = fields.Str(required=True, validate=validate.Length(max=100))
    birth_year = fields.Int(required=True)
    height = fields.Float(required=True)
    fav_cuisine = fields.Str(required=True, validate=validate.Length(max=100))
    fav_colour = fields.Str(required=True, validate=validate.Length(max=50))
    fav_school_subject = fields.Str(required=True, validate=validate.Length(max=100))
    political = fields.Bool(required=True)
    religious = fields.Bool(required=True)
    family_oriented = fields.Bool(required=True)

    @validates("birth_year")
    def _validate_birth_year(self, value, **kwargs):
        current_year = datetime.now(timezone.utc).year
        if value < 1900 or value > current_year - 18:
            raise ValidationError(
                f"Birth year must be between 1900 and {current_year - 18}"
            )

    @validates("height")
    def _validate_height(self, value, **kwargs):
        if value <= 0 or value > 300:  # Reasonable height range in cm
            raise ValidationError("Height must be a positive number less than 300")


class FavouriteSchema(Schema):
    """Schema for Favourite model"""

    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, attribute="user_id_fk")
    fav_user_id = fields.Int(required=True, attribute="fav_user_id_fk")
    created_at = fields.DateTime(dump_only=True)


class TopFavouriteSchema(Schema):
    """Schema for top favourites results"""

    user_id = fields.Int()
    name = fields.Str()
    favourite_count = fields.Int()


class UserInfoSchema(Schema):
    """Schema for minimal user information"""

    name = fields.Str()
    photo = fields.Str(allow_none=True)
    id = fields.Int()


class ProfileWithUserSchema(Schema):
    """Schema for profile with user information"""

    id = fields.Int()
    user_id = fields.Int(attribute="user_id_fk")
    description = fields.Str()
    parish = fields.Str()
    biography = fields.Str()
    sex = fields.Str()
    race = fields.Str()
    birth_year = fields.Int()
    height = fields.Float()
    fav_cuisine = fields.Str()
    fav_colour = fields.Str()
    fav_school_subject = fields.Str()
    political = fields.Bool()
    religious = fields.Bool()
    family_oriented = fields.Bool()
    user = fields.Nested(UserInfoSchema)


# Request schemas
class RegistrationRequestSchema(Schema):
    """Schema for registration request"""

    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    name = fields.Str(required=True, validate=validate.Length(max=120))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    # Photo is handled separately since it's a file upload


class LoginRequestSchema(Schema):
    """Schema for login request"""

    username = fields.Str(required=True)
    password = fields.Str(required=True)


class FavouriteRequestSchema(Schema):
    """Schema for adding a favourite"""

    userId = fields.Int(required=True)


class SearchRequestSchema(Schema):
    """Schema for search query parameters"""

    name = fields.Str(allow_none=True)
    birth_year = fields.Int(allow_none=True)
    sex = fields.Str(allow_none=True)
    race = fields.Str(allow_none=True)
