from app import app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

migrate = Migrate(app, db)
cli = FlaskGroup(app)

@cli.command('db')
def db_command():
    """Run database migrations."""
    from flask.cli import with_appcontext
    from flask_migrate import upgrade, migrate, init, downgrade

    @with_appcontext
    def run_migrate():
        migrate()
        upgrade()

    run_migrate()

if __name__ == '__main__':
    cli()
