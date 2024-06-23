from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    This endpoint expects a JSON body containing the user's email, name, and password.
    It returns the created user object if successful or validation errors if the input is invalid.

    Request Body:
        {
            "email": "user@example.com",
            "name": "User Name",
            "password": "securepassword"
        }

    Returns:
        201 Created with the new user data if successful.
        400 Bad Request with error messages if validation fails.
    """
    data = request.json
    try:
        # Hash the user's password before saving
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf8')
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
        # Add the new user to the database
        return user_schema.dump(user), 201
    except ValidationError as err:
        return {"error": err.messages}, 400

@users_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT token.

    This endpoint expects a JSON body containing the user's email and password.
    It returns a JWT token if authentication is successful or an error message if authentication fails.

    Request Body:
        {
            "email": "user@example.com",
            "password": "securepassword"
        }

    Returns:
        200 OK with a JWT token if authentication is successful.
        401 Unauthorized with an error message if authentication fails.
    """
    data = request.json
    user = db.session.scalar(db.select(User).where(User.email == data['email']))
    # Select the user with the given email
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    else:
        return {"error": "Invalid email or password"}, 401

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    
    """
    Retrieve all users.

    This endpoint returns a list of all users.

    Returns:
        200 OK with a list of users.
        403 Forbidden if the user is not authenticated.
    """
    users = db.session.scalars(db.select(User)).all()
    # Select all users from the database
    return users_schema.dump(users), 200

@users_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    
    """
    Retrieve a specific user by ID.

    This endpoint returns the user details for the specified user ID.

    Path Parameters:
        id (int): The ID of the user to retrieve.

    Returns:
        200 OK with the user data if found.
        404 Not Found if the user does not exist.
    """
    user = db.session.get(User, id)
    # Select the user with the given ID
    if not user:
        return {"error": "User not found"}, 404
    return user_schema.dump(user), 200

@users_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Update a specific user by ID.

    This endpoint expects a JSON body containing the updated user data.
    It returns the updated user object if successful or validation errors if the input is invalid.

    Path Parameters:
        id (int): The ID of the user to update.

    Request Body:
        {
            "email": "user@example.com",
            "name": "Updated Name",
            "password": "newpassword"
        }

    Returns:
        200 OK with the updated user data if successful.
        404 Not Found if the user does not exist.
        400 Bad Request with error messages if validation fails.
    """
    user = db.session.get(User, id)
    # Select the user with the given ID
    if not user:
        return {"error": "User not found"}, 404

    data = request.json
    if 'password' in data:
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf8')
    try:
        user_schema.load(data, instance=user)
        db.session.commit()
        # Update the user with new data
        return user_schema.dump(user), 200
    except ValidationError as err:
        return {"error": err.messages}, 400

@users_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    
    """
    Delete a specific user by ID.

    This endpoint deletes the user with the specified ID.

    Path Parameters:
        id (int): The ID of the user to delete.

    Returns:
        200 OK with a message confirming deletion if successful.
        404 Not Found if the user does not exist.
    """
    user = db.session.get(User, id)
    # Select the user with the given ID
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()
    # Delete the user from the database
    return {"message": "User deleted"}, 200
