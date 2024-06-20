from flask import Blueprint, request, jsonify
from init import db
from models.battle import Battle
from schemas.battle_schema import BattleSchema
from marshmallow.exceptions import ValidationError

battle_bp = Blueprint('battle_bp', __name__)
battle_schema = BattleSchema()

@battle_bp.route('/', methods=['POST'])
def create_battle():
    """
    Create a new battle record.
    """
    try:
        data = battle_schema.load(request.json)  # Validate and deserialize input
        # Create a new Battle instance
        battle = Battle(**data)
        db.session.add(battle)  # Add the battle to the session
        db.session.commit()  # Commit the session to the database
        return battle_schema.jsonify(battle), 201  # Return the created battle
    except ValidationError as err:
        return jsonify(err.messages), 400  # Return validation errors
