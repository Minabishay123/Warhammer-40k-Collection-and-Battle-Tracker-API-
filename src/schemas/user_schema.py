from marshmallow import fields
from marshmallow.validate import Length
from init import ma

class UserSchema(ma.Schema):
    email = fields.Email(required=True)  # Validate as email and required
    password = fields.String(validate=Length(min=8), required=True)  # Minimum 8 characters
    name = fields.String()  # Optional name field
    is_admin = fields.Boolean()  # Boolean for admin status

    class Meta:
        fields = ("id", "email", "name", "password", "is_admin")  # Fields to include in the serialized output
