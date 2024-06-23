from init import app
from blueprints.cli_bp import db_commands
from blueprints.collections_bp import collections_bp
from blueprints.battles_bp import battles_bp
from blueprints.users_bp import users_bp
from marshmallow.exceptions import ValidationError

app.register_blueprint(db_commands)
app.register_blueprint(collections_bp)
app.register_blueprint(battles_bp)
app.register_blueprint(users_bp)

@app.route("/")
def index():
    return "Welcome to the world of Warhammer 40K!!!"

@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {"error": "Not Found"}, 404

@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"error": vars(err)["messages"]}, 400

@app.errorhandler(KeyError)
def missing_key(err):
    return {"error": f"Missing field: {str(err)}"}, 400

if __name__ == "__main__":
    app.run()
