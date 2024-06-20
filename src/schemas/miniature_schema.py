from init import ma
from marshmallow import fields

class MiniatureSchema(ma.Schema):
    name = fields.String(required=True)  # Required miniature name
    faction = fields.String(required=True)  # Required faction
    user_id = fields.Integer(required=True)  # Foreign key to user

    class Meta:
        fields = ("id", "name", "faction", "user_id")  # Fields to include in the serialized output
