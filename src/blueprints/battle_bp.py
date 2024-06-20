from flask import Blueprint, request, jsonify
from init import db
from models.battle import Battle, BattleSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

battle_bp = Blueprint('battle', __name__)
battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)

@battle_bp.route('/battles', methods=['POST'])
@jwt_required()
def create_battle():
    data = request.get_json()
    user_id = get_jwt_identity()
    battle = battle_schema.load(data)
    battle.user_id = user_id
    db.session.add(battle)
    db.session.commit()
    return battle_schema.dump(battle), 201

@battle_bp.route('/battles', methods=['GET'])
@jwt_required()
def get_battles():
    user_id = get_jwt_identity()
    battles = Battle.query.filter_by(user_id=user_id).all()
    return battles_schema.dump(battles), 200

@battle_bp.route('/battles/<int:id>', methods=['GET'])
@jwt_required()
def get_battle(id):
    battle = Battle.query.get_or_404(id)
    return battle_schema.dump(battle), 200

@battle_bp.route('/battles/<int:id>', methods=['PUT'])
@jwt_required()
def update_battle(id):
    battle = Battle.query.get_or_404(id)
    data = request.get_json()
    battle_schema.load(data, instance=battle, partial=True)
    db.session.commit()
    return battle_schema.dump(battle), 200

@battle_bp.route('/battles/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_battle(id):
    battle = Battle.query.get_or_404(id)
    db.session.delete(battle)
    db.session.commit()
    return '', 204
