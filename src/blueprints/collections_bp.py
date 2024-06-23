from flask import Blueprint, request
from init import db
from models.collection import Collection, CollectionSchema
from flask_jwt_extended import jwt_required
from auth import authorize_owner
from marshmallow.exceptions import ValidationError

collections_bp = Blueprint('collections', __name__)
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)

@collections_bp.route('/collections', methods=['POST'])
@jwt_required()
def create_collection():
    """
    Create a new collection for the authenticated user.

    This endpoint expects a JSON body containing the collection details.
    It returns the created collection object if successful or a validation error if the input is invalid.

    Request Body:
        {
            "name": "Collection Name",
            "count": 100,
            "user_id": 1
        }

    Returns:
        201 Created with the new collection data if successful.
        400 Bad Request with error messages if validation fails.
    """
    data = request.json
    try:
        collection = collection_schema.load(data)
        db.session.add(collection)
        db.session.commit()
        # Add the new collection to the database
        return collection_schema.dump(collection), 201
    except ValidationError as err:
        return {"error": err.messages}, 400

@collections_bp.route('/collections', methods=['GET'])
@jwt_required()
def get_collections():
    """
    Retrieve all collections for the authenticated user.

    This endpoint returns a list of all collections associated with the authenticated user.

    Returns:
        200 OK with a list of collections.
        403 Forbidden if the user is not authenticated.
    """ 
    collections = db.session.scalars(db.select(Collection)).all()
    # Select all collections from the database
    return collections_schema.dump(collections), 200

@collections_bp.route('/collections/<int:id>', methods=['GET'])
@jwt_required()
def get_collection(id):
    """
    Retrieve a specific collection by ID.

    This endpoint returns the collection details for the specified collection ID.

    Path Parameters:
        id (int): The ID of the collection to retrieve.

    Returns:
        200 OK with the collection data if found.
        404 Not Found if the collection does not exist.
    """
    collection = db.session.get(Collection, id)
    # Select the collection with the given ID
    if not collection:
        return {"error": "Collection not found"}, 404
    return collection_schema.dump(collection), 200

@collections_bp.route('/collections/<int:id>', methods=['PUT'])
@jwt_required()
def update_collection(id):
    """
    Update a specific collection by ID.

    This endpoint expects a JSON body containing the updated collection data.
    It returns the updated collection object if successful or validation errors if the input is invalid.

    Path Parameters:
        id (int): The ID of the collection to update.

    Request Body:
        {
            "name": "Updated Name",
            "count": 75
        }

    Returns:
        200 OK with the updated collection data if successful.
        404 Not Found if the collection does not exist.
        400 Bad Request with error messages if validation fails.
    """
    collection = db.session.get(Collection, id)
    # Select the collection with the given ID
    if not collection:
        return {"error": "Collection not found"}, 404

    data = request.json
    try:
        collection_schema.load(data, instance=collection)
        db.session.commit()
        # Update the collection with new data
        return collection_schema.dump(collection), 200
    except ValidationError as err:
        return {"error": err.messages}, 400

@collections_bp.route('/collections/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    """
    Delete a specific collection by ID.

    This endpoint deletes the collection with the specified ID.

    Path Parameters:
        id (int): The ID of the collection to delete.

    Returns:
        200 OK with a message confirming deletion if successful.
        404 Not Found if the collection does not exist.
    """
    collection = db.session.get(Collection, id)
    # Select the collection with the given ID
    if not collection:
        return {"error": "Collection not found"}, 404

    authorize_owner(collection)
    db.session.delete(collection)
    db.session.commit()
    # Delete the collection from the database
    return {"message": "Collection deleted"}, 200
