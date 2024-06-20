from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import blueprints
from blueprints.user_blueprint import user_bp
from blueprints.miniature_blueprint import miniature_bp
from blueprints.battle_blueprint import battle_bp

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(miniature_bp, url_prefix='/miniatures')
app.register_blueprint(battle_bp, url_prefix='/battles')
