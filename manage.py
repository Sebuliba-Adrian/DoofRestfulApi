from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from db import db


db.init_app(app)
# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
