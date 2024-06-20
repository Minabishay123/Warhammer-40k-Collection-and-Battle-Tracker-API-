from flask import Blueprint, request, jsonify
from init import db
from models.collection import Collection, CollectionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

collection_bp = Blueprint('collection', __name__)
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)

@collection_bp.route('/collections', methods=['POST'])
@jwt_required()
def create_collection():
    data = request.get_json()
    user_id = get_jwt_identity()
    collection = collection_schema.load(data)
    collection.user_id = user_id
    db.session.add(collection)
    db.session.commit()
    return collection_schema.dump(collection), 201

@collection_bp.route('/collections', methods=['GET'])
@jwt_required()
def get_collections():
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(user_id=user_id).all()
    return collections_schema.dump(collections), 200

@collection_bp.route('/collections/<int:id>', methods=['GET'])
@jwt_required()
def get_collection(id):
    collection = Collection.query.get_or_404(id)
    return collection_schema.dump(collection), 200

@collection_bp.route('/collections/<int:id>', methods=['PUT'])
@jwt_required()
def update_collection(id):
    collection = Collection.query.get_or_404(id)
    data = request.get_json()
    collection_schema.load(data, instance=collection, partial=True)
    db.session.commit()
    return collection_schema.dump(collection), 200

@collection_bp.route('/collections/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    collection = Collection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    return '', 204
