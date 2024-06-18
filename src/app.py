from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config
from blueprints.users_bp import users_bp
from blueprints.miniatures_bp import miniatures_bp
from blueprints.battles_bp import battles_bp
from .middlewares.error_handler import handle_errors
from os import environ

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)
    
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(miniatures_bp, url_prefix='/miniatures')
    app.register_blueprint(battles_bp, url_prefix='/battles')
    
    app.register_error_handler(Exception, handle_errors)
    
    return app