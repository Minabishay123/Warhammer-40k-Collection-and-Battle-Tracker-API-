from flask import Flask
from config import Config
from extensions import db, ma, jwt, bcrypt
from blueprints import auth_bp, collection_bp, battle_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(collection_bp, url_prefix='/collections')
    app.register_blueprint(battle_bp, url_prefix='/battles')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
