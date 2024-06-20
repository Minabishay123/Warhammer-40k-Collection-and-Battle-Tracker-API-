from flask import Blueprint, request, jsonify
from init import db
from models.miniature import Miniature
from schemas.miniature_schema import MiniatureSchema
from marshmallow.exceptions import ValidationError

miniature_bp = Blueprint('miniature_bp', __name__)
miniature_schema = MiniatureSchema()

@miniature_bp.route('/', methods=['POST'])
def create_miniature():
    """
    Create a new miniature.
    """
    try:
        data = miniature_schema.load(request.json)  # Validate and deserialize input
        # Create a new Miniature instance
        miniature = Miniature(**data)
        db.session.add(miniature)  # Add the miniature to the session
        db.session.commit()  # Commit the session to the database
        return miniature_schema.jsonify(miniature), 201  # Return the created miniature
    except ValidationError as err:
        return jsonify(err.messages), 400  # Return validation errors

