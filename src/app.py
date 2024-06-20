from init import app, db
import cli  # Import CLI commands to register them with the Flask app

# Import CLI commands
app.cli.add_command(cli.db_commands)

if __name__ == '__main__':
    app.run(debug=True)
