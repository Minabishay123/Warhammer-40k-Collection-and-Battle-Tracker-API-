from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from blueprints.auth_blueprint import auth_bp
        from blueprints.collection_blueprint import collection_bp
        from blueprints.battle_blueprint import battle_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(collection_bp)
        app.register_blueprint(battle_bp)

    return app
