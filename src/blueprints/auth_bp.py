from flask import Blueprint, request, jsonify
from extensions import db, bcrypt, jwt
from models.user import User
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = user_schema.load(request.json)
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"message": "User already exists"}), 400
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = user_schema.load(request.json)
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = jwt.create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except ValidationError as err:
        return jsonify(err.messages), 400
