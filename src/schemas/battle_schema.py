from init import ma
from marshmallow import fields

class BattleSchema(ma.Schema):
    date = fields.Date(required=True)  # Required battle date
    location = fields.String(required=True)  # Required location
    outcome = fields.String(required=True)  # Required outcome
    user_id = fields.Integer(required=True)  # Foreign key to user

    class Meta:
        fields = ("id", "date", "location", "outcome", "user_id")  # Fields to include in the serialized output
