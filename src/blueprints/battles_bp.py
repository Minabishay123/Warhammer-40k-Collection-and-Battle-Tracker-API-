from flask import Blueprint, request
from init import db
from models.battle import Battle, BattleSchema
from flask_jwt_extended import jwt_required
from auth import authorize_owner
from marshmallow.exceptions import ValidationError

battles_bp = Blueprint('battles', __name__)
battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)

@battles_bp.route('/battles', methods=['POST'])
@jwt_required()
def create_battle():
    """
    Create a new battle entry for the authenticated user.

    This endpoint expects a JSON body containing the battle details.
    It returns the created battle object if successful or validation errors if the input is invalid.

    Request Body:
        {
            "opponent": "Orks",
            "description": "Epic battle against the Orks",
            "date": "2024-06-21",
            "result": "Victory",
            "user_id": 1
        }

    Returns:
        201 Created with the new battle data if successful.
        400 Bad Request with error messages if validation fails.
    """
    data = request.json
    try:
        battle = battle_schema.load(data)
        db.session.add(battle)
        db.session.commit()
        # Add the new battle to the database
        return battle_schema.dump(battle), 201
    except ValidationError as err:
        return {"error": err.messages}, 400

@battles_bp.route('/battles', methods=['GET'])
@jwt_required()
def get_battles():
    """
    Retrieve all battles for the authenticated user.

    This endpoint returns a list of all battles associated with the authenticated user.

    Returns:
        200 OK with a list of battles.
        403 Forbidden if the user is not authenticated.
    """
    battles = db.session.scalars(db.select(Battle)).all()
    # Select all battles from the database
    return battles_schema.dump(battles), 200

@battles_bp.route('/battles/<int:id>', methods=['GET'])
@jwt_required()
def get_battle(id):
    """
    Retrieve a specific battle by ID.

    This endpoint returns the battle details for the specified battle ID.

    Path Parameters:
        id (int): The ID of the battle to retrieve.

    Returns:
        200 OK with the battle data if found.
        404 Not Found if the battle does not exist.
    """
    battle = db.session.get(Battle, id)
    # Select the battle with the given ID
    if not battle:
        return {"error": "Battle not found"}, 404
    return battle_schema.dump(battle), 200

@battles_bp.route('/battles/<int:id>', methods=['PUT'])
@jwt_required()
def update_battle(id):
    """
    Update a specific battle by ID.

    This endpoint expects a JSON body containing the updated battle data.
    It returns the updated battle object if successful or validation errors if the input is invalid.

    Path Parameters:
        id (int): The ID of the battle to update.

    Request Body:
        {
            "opponent": "Updated Opponent",
            "description": "Updated description",
            "date": "2024-06-22",
            "result": "Defeat"
        }

    Returns:
        200 OK with the updated battle data if successful.
        404 Not Found if the battle does not exist.
        400 Bad Request with error messages if validation fails.
    """
    battle = db.session.get(Battle, id)
    # Select the battle with the given ID
    if not battle:
        return {"error": "Battle not found"}, 404

    data = request.json
    try:
        battle_schema.load(data, instance=battle)
        db.session.commit()
        # Update the battle with new data
        return battle_schema.dump(battle), 200
    except ValidationError as err:
        return {"error": err.messages}, 400

@battles_bp.route('/battles/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_battle(id):
    """
    Delete a specific battle by ID.

    This endpoint deletes the battle with the specified ID.

    Path Parameters:
        id (int): The ID of the battle to delete.

    Returns:
        200 OK with a message confirming deletion if successful.
        404 Not Found if the battle does not exist.
    """
    battle = db.session.get(Battle, id)
    # Select the battle with the given ID
    if not battle:
        return {"error": "Battle not found"}, 404

    authorize_owner(battle)
    db.session.delete(battle)
    db.session.commit()
    # Delete the battle from the database
    return {"message": "Battle deleted"}, 200
