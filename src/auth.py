from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.user import User
from flask import abort, jsonify, make_response

def admin_only(fn):
    @jwt_required()
    def inner():
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if user:
            return fn()
        else:
            return {"error": "By decree of the Imperium, only those bearing the sigil of Admin have the honor of accessing this sacred resource. Unauthorized mortals shall face the wrath of the God-Emperors sanction!"}, 403
    return inner

def authorize_owner(record):
    user_id = get_jwt_identity()
    if user_id != record.user_id:
        abort(make_response(jsonify(error="Only the rightful custodian of this resource, bearing the mark of ownership, may unlock its secrets. All others shall be cast into the void by the will of the God-Emperor!"), 403))
