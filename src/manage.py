from flask.cli import FlaskGroup
from . import create_app
from .extensions import db
from .models import *

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('create_db')
def create_db():
    """Creates the database."""
    db.create_all()

@cli.command('drop_db')
def drop_db():
    """Drops the database."""
    db.drop_all()

@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    from .models.user import User
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    cli()
