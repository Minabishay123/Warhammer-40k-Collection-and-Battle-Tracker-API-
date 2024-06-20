from flask import Blueprint, request, jsonify
from init import db, bcrypt, jwt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_schema = UserSchema()
    try:
        user = user_schema.load(data)
        user.password = bcrypt.generate_password_hash(user.password).decode('utf8')
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid credentials'), 401
