from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..models.collection import Collection
from ..models.user import User
from ..extensions import db, ma

collection_bp = Blueprint('collection', __name__)

class CollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collection
        load_instance = True
        include_fk = True

collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)

@collection_bp.route('/', methods=['POST'])
@jwt_required()
def create_collection():
    try:
        collection_data = request.json
        user_id = get_jwt_identity()
        collection_data['user_id'] = user_id
        collection = collection_schema.load(collection_data)
        db.session.add(collection)
        db.session.commit()
        return collection_schema.jsonify(collection), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

@collection_bp.route('/', methods=['GET'])
@jwt_required()
def get_collections():
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(user_id=user_id).all()
    return collections_schema.jsonify(collections)

@collection_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_collection(id):
    try:
        collection_data = request.json
        collection = Collection.query.get_or_404(id)
        for key, value in collection_data.items():
            setattr(collection, key, value)
        db.session.commit()
        return collection_schema.jsonify(collection)
    except ValidationError as e:
        return jsonify(e.messages), 400

@collection_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    collection = Collection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    return jsonify({'msg': 'Collection deleted'})
