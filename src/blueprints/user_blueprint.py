from flask import Blueprint, request, jsonify
from init import db, bcrypt
from models.user import User
from schemas.user_schema import UserSchema
from marshmallow.exceptions import ValidationError

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()

@user_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user.
    """
    try:
        data = user_schema.load(request.json)  # Validate and deserialize input
        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf8')
        # Create a new User instance
        user = User(email=data['email'], name=data['name'], password=hashed_password)
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the session to the database
        return user_schema.jsonify(user), 201  # Return the created user
    except ValidationError as err:
        return jsonify(err.messages), 400  # Return validation errors
