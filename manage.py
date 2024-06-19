from flask.cli import FlaskGroup
from app import create_app
from extensions import db
from models import *

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.create_all()
    print("Database created!")

@cli.command("drop_db")
def drop_db():
    db.drop_all()
    print("Database dropped!")

if __name__ == "__main__":
    cli()
