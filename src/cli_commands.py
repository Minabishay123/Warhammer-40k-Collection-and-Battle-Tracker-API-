from flask import Blueprint
from datetime import date
from init import db, bcrypt
from models.user import User
from models.miniature import Collection
from models.battle import Battle

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    """
    Creates all tables in the database according to the defined models.
    """
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_tables():
    """
    Drops all tables in the database.
    """
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    """
    Seeds the database with initial data including an admin user, a regular user, collections, and battles.
    """
    # Create admin and regular user with hashed passwords
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
    db.session.commit()  # Commit the users to the database

    # Create initial collections for each user
    collection1 = Collection(name="Ultramarines", user=admin)
    collection2 = Collection(name="Orks", user=user)
    db.session.add(collection1)
    db.session.add(collection2)
    db.session.commit()  # Commit the collections to the database

    # Create initial battles for each collection
    battle1 = Battle(
        date=date(2023, 6, 19),
        opponent="Eldar",
        outcome="Victory",
        collection=collection1,
        user=admin
    )
    battle2 = Battle(
        date=date(2023, 6, 20),
        opponent="Chaos",
        outcome="Defeat",
        collection=collection2,
        user=user
    )
    db.session.add(battle1)
    db.session.add(battle2)
    db.session.commit()  # Commit the battles to the database

    print("Database seeded")
