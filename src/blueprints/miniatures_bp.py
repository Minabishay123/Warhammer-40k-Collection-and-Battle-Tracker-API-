from flask import Blueprint, request, jsonify
from app import db
from models.miniature import Miniature
from models.miniature import MiniatureSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

miniatures_bp = Blueprint('miniatures_bp', __name__)
miniature_schema = MiniatureSchema()
miniatures_schema = MiniatureSchema(many=True)

@miniatures_bp.route('/', methods=['POST'])
@jwt_required()
def create_miniature():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_miniature = Miniature(
        user_id=current_user['id'],
        name=data['name'],
        faction=data['faction'],
        unit_type=data['unit_type'],
        points_cost=data['points_cost']
    )
    db.session.add(new_miniature)
    db.session.commit()
    return miniature_schema.jsonify(new_miniature), 201

@miniatures_bp.route('/', methods=['GET'])
@jwt_required()
def get_miniatures():
    current_user = get_jwt_identity()
    miniatures = Miniature.query.filter_by(user_id=current_user['id']).all()
    return miniatures_schema.jsonify(miniatures)

@miniatures_bp.route('/<int:miniature_id>', methods=['GET'])
@jwt_required()
def get_miniature(miniature_id):
    current_user = get_jwt_identity()
    miniature = Miniature.query.filter_by(id=miniature_id, user_id=current_user['id']).first()
    if not miniature:
        return jsonify({"msg": "Miniature not found"}), 404
    return miniature_schema.jsonify(miniature)

@miniatures_bp.route('/<int:miniature_id>', methods=['PUT'])
@jwt_required()
def update_miniature(miniature_id):
    current_user = get_jwt_identity()
    miniature = Miniature.query.filter_by(id=miniature_id, user_id=current_user['id']).first()
    if not miniature:
        return jsonify({"msg": "Miniature not found"}), 404
    data = request.get_json()
    miniature.name = data['name']
    miniature.faction = data['faction']
    miniature.unit_type = data['unit_type']
    miniature.points_cost = data['points_cost']
    db.session.commit()
    return miniature_schema.jsonify(miniature)

@miniatures_bp.route('/<int:miniature_id>', methods=['DELETE'])
@jwt_required()
def delete_miniature(miniature_id):
    current_user = get_jwt_identity()
    miniature = Miniature.query.filter_by(id=miniature_id, user_id=current_user['id']).first()
    if not miniature:
        return jsonify({"msg": "Miniature not found"}), 404
    db.session.delete(miniature)
    db.session.commit()
    return jsonify({"msg": "Miniature deleted successfully"})
