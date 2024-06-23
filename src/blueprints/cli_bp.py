from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.collection import Collection
from models.battle import Battle
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")

    users = [
        User(
            email="admin@warhammer.com",
            password=bcrypt.generate_password_hash("adminpassword").decode("utf8"),
            is_admin=True,
        ),
        User(
            email="player@warhammer.com",
            name="Player One",
            password=bcrypt.generate_password_hash("playerpassword").decode("utf8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    collections = [
        Collection(
            name="Space Marines",
            count=50,
            user=users[0]
        ),
        Collection(
            name="Orks",
            count=30,
            user=users[1]
        ),
    ]

    battles = [
        Battle(
            opponent="Orks",
            description="Epic battle against the Orks",
            date=date.today(),
            result="Victory",
            user=users[0]
        ),
        Battle(
            opponent="Space Marines",
            description="Lost against the Space Marines",
            date=date.today(),
            result="Defeat",
            user=users[1]
        ),
    ]

    db.session.add_all(collections)
    db.session.add_all(battles)
    db.session.commit()

    print("Users, Collections, and Battles added")
