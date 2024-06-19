from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.battle import Battle
from marshmallow import Schema, fields, ValidationError

battle_bp = Blueprint('battle', __name__)

class BattleSchema(Schema):
    opponent = fields.String(required=True)
    result = fields.String(required=True)
    date = fields.DateTime(required=True)

battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)

@battle_bp.route('/', methods=['POST'])
@jwt_required()
def create_battle():
    try:
        data = battle_schema.load(request.json)
        user_id = get_jwt_identity()
        battle = Battle(opponent=data['opponent'], result=data['result'], date=data['date'], user_id=user_id)
        db.session.add(battle)
        db.session.commit()
        return battle_schema.jsonify(battle), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@battle_bp.route('/', methods=['GET'])
@jwt_required()
def get_battles():
    user_id = get_jwt_identity()
    battles = Battle.query.filter_by(user_id=user_id).all()
    return battles_schema.jsonify(battles), 200

@battle_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_battle(id):
    try:
        data = battle_schema.load(request.json)
        battle = Battle.query.get_or_404(id)
        battle.opponent = data['opponent']
        battle.result = data['result']
        battle.date = data['date']
        db.session.commit()
        return battle_schema.jsonify(battle), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

@battle_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_battle(id):
    battle = Battle.query.get_or_404(id)
    db.session.delete(battle)
    db.session.commit()
    return '', 204
