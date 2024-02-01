from marshmallow import Schema, fields



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
    username = fields.Str(required=True, description="The username of the new user.")
    password = fields.Str(required=True, load_only=True, description="The password of the new user (load-only).")
    email = fields.Str(required=False, description="The email address of the new user (optional).")
    team = fields.Str(required=True, description="The team the new user belongs to.")

    class Meta:
        """
        Meta class for additional configuration.

        Attributes:
            ordered (bool): Whether to preserve the order of fields in the serialized output.
        """
        ordered = True


