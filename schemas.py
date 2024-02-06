from marshmallow import Schema, fields
from datetime import datetime


class MoodSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique identifier for the user (read-only).")
    title=fields.Str(required=True)
    quote=fields.Str(required=True)
    author=fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True, format="%Y-%m-%dT%H:%M:%S.%fZ", missing=lambda: datetime.utcnow())


    class Meta:
        """
        Meta class for additional configuration.

        Attributes:
            ordered (bool): Whether to preserve the order of fields in the serialized output.
        """
        ordered = True

class MoodUpdateSchema(Schema):
    title=fields.Str()
    quote=fields.Str()
    author=fields.Str()

class TeamSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class UserSchema(Schema):
    """
    Schema for representing user data.

    Attributes:
    ---
        id (int): The unique identifier for the user (read-only).
        username (str): The username of the new user (required).
        password (str): The password of the new user (required, load-only).
        email (str): The email address of the new user (optional).
        team (str): The team the new user belongs to (required).
    """
    id = fields.Int(dump_only=True, description="The unique identifier for the user (read-only).")
    username = fields.Str()
    password = fields.Str(required=True, load_only=True, description="The password of the new user (load-only).")
    email = fields.Str(required=True, description="The email address of the new user (optional).")
    team = fields.Str(required=True, description="The team the new user belongs to.")

    class Meta:
        """
        Meta class for additional configuration.

        Attributes:
            ordered (bool): Whether to preserve the order of fields in the serialized output.
        """
        ordered = True


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique identifier for the user (read-only).")
    username = fields.Str()
    password = fields.Str(required=True, load_only=True, description="The password of the new user (load-only).")
    email = fields.Str(required=True, description="The email address of the new user (optional).")
    team = fields.Str(required=True, description="The team the new user belongs to.")

