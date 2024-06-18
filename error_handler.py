from flask import jsonify

def handle_errors(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500
