from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.collection import Collection
from marshmallow import Schema, fields, ValidationError

collection_bp = Blueprint('collection', __name__)

class CollectionSchema(Schema):
    name = fields.String(required=True)
    description = fields.String()

collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)

@collection_bp.route('/', methods=['POST'])
@jwt_required()
def create_collection():
    try:
        data = collection_schema.load(request.json)
        user_id = get_jwt_identity()
        collection = Collection(name=data['name'], description=data.get('description'), user_id=user_id)
        db.session.add(collection)
        db.session.commit()
        return collection_schema.jsonify(collection), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@collection_bp.route('/', methods=['GET'])
@jwt_required()
def get_collections():
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(user_id=user_id).all()
    return collections_schema.jsonify(collections), 200

@collection_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_collection(id):
    try:
        data = collection_schema.load(request.json)
        collection = Collection.query.get_or_404(id)
        collection.name = data['name']
        collection.description = data.get('description')
        db.session.commit()
        return collection_schema.jsonify(collection), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

@collection_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    collection = Collection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    return '', 204
