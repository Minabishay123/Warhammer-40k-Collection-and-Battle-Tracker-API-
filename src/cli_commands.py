from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.collection import Collection
from models.battle import Battle

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    admin = User(
        email="admin@warhammer.com",
        password=bcrypt.generate_password_hash("adminpass").decode('utf8'),
        is_admin=True
    )
    user = User(
        email="user@warhammer.com",
        password=bcrypt.generate_password_hash("userpass").decode('utf8')
    )
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

    collection1 = Collection(name="Ultramarines", user=admin)
    collection2 = Collection(name="Orks", user=user)
    db.session.add(collection1)
    db.session.add(collection2)
    db.session.commit()

    battle1 = Battle(
        date='2023-06-19',
        opponent="Eldar",
        outcome="Victory",
        collection=collection1,
        user=admin
    )
    battle2 = Battle(
        date='2023-06-20',
        opponent="Chaos",
        outcome="Defeat",
        collection=collection2,
        user=user
    )
    db.session.add(battle1)
    db.session.add(battle2)
    db.session.commit()

    print("Database seeded")
