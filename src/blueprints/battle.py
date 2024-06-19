from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..models.battle import Battle
from ..models.user import User
from ..extensions import db, ma

battle_bp = Blueprint('battle', __name__)

class BattleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Battle
        load_instance = True
        include_fk = True

battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)

@battle_bp.route('/', methods=['POST'])
@jwt_required()
def create_battle():
    try:
        battle_data = request.json
        user_id = get_jwt_identity()
        battle_data['user_id'] = user_id
        battle = battle_schema.load(battle_data)
        db.session.add(battle)
        db.session.commit()
        return battle_schema.jsonify(battle), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

@battle_bp.route('/', methods=['GET'])
@jwt_required()
def get_battles():
    user_id = get_jwt_identity()
    battles = Battle.query.filter_by(user_id=user_id).all()
    return battles_schema.jsonify(battles)

@battle_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_battle(id):
    try:
        battle_data = request.json
        battle = Battle.query.get_or_404(id)
        for key, value in battle_data.items():
            setattr(battle, key, value)
        db.session.commit()
        return battle_schema.jsonify(battle)
    except ValidationError as e:
        return jsonify(e.messages), 400

@battle_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_battle(id):
    battle = Battle.query.get_or_404(id)
    db.session.delete(battle)
    db.session.commit()
    return jsonify({'msg': 'Battle deleted'})
