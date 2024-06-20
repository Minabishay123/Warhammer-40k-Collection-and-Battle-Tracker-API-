from init import create_app
from cli_commands import db_commands

app = create_app()

app.cli.add_command(db_commands)
