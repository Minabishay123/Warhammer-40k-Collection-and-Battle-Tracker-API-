from flask import Blueprint, request, jsonify
from app import db
from models.battle import Battle
from models.battle import BattleSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

battles_bp = Blueprint('battles_bp', __name__)
battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)

@battles_bp.route('/', methods=['POST'])
@jwt_required()
def create_battle():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_battle = Battle(
        user_id=current_user['id'],
        opponent_name=data['opponent_name'],
        date=data['date'],
        outcome=data['outcome'],
        location=data.get('location'),
        notes=data.get('notes')
    )
    db.session.add(new_battle)
    db.session.commit()
    return battle_schema.jsonify(new_battle), 201

@battles_bp.route('/', methods=['GET'])
@jwt_required()
def get_battles():
    current_user = get_jwt_identity()
    battles = Battle.query.filter_by(user_id=current_user['id']).all()
    return battles_schema.jsonify(battles)

@battles_bp.route('/<int:battle_id>', methods=['GET'])
@jwt_required()
def get_battle(battle_id):
    current_user = get_jwt_identity()
    battle = Battle.query.filter_by(id=battle_id, user_id=current_user['id']).first()
    if not battle:
        return jsonify({"msg": "Battle not found"}), 404
    return battle_schema.jsonify(battle)

@battles_bp.route('/<int:battle_id>', methods=['PUT'])
@jwt_required()
def update_battle(battle_id):
    current_user = get_jwt_identity()
    battle = Battle.query.filter_by(id=battle_id, user_id=current_user['id']).first()
    if not battle:
        return jsonify({"msg": "Battle not found"}), 404
    data = request.get_json()
    battle.opponent_name = data['opponent_name']
    battle.date = data['date']
    battle.outcome = data['outcome']
    battle.location = data.get('location')
    battle.notes = data.get('notes')
    db.session.commit()
    return battle_schema.jsonify(battle)

@battles_bp.route('/<int:battle_id>', methods=['DELETE'])
@jwt_required()
def delete_battle(battle_id):
    current_user = get_jwt_identity()
    battle = Battle.query.filter_by(id=battle_id, user_id=current_user['id']).first()
    if not battle:
        return jsonify({"msg": "Battle not found"}), 404
    db.session.delete(battle)
    db.session.commit()
    return jsonify({"msg": "Battle deleted successfully"})
