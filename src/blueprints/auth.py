from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError, fields, post_load
from ..models.user import User
from ..extensions import db, bcrypt, ma

auth_bp = Blueprint('auth', __name__)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("password_hash",)

    password = fields.Str(load_only=True)

    @post_load
    def hash_password(self, data, **kwargs):
        password = data.pop('password', None)
        if password:
            data['password_hash'] = bcrypt.generate_password_hash(password).decode('utf-8')
        return data

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.json
        user = user_schema.load(user_data)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    user_data = request.json
    user = User.query.filter_by(username=user_data['username']).first()
    if user and user.check_password(user_data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({'msg': 'Invalid credentials'}), 401

