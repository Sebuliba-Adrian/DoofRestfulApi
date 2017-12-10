"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
from flask_script import Manager
from flask_migrate import MigrateCommand
import unittest

from app import app
from db import db

app.config.from_object('config.DevelopmentConfig')
db.init_app(app)

manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
