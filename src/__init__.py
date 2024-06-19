from flask import Flask
from .config import Config
from .extensions import db, ma, bcrypt, jwt
from .blueprints.auth import auth_bp
from .blueprints.collection import collection_bp
from .blueprints.battle import battle_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(collection_bp, url_prefix='/collection')
    app.register_blueprint(battle_bp, url_prefix='/battle')

    return app
