"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
import os
import unittest

import coverage
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from app import app
from db import db

app.config.from_object('config.config.DevelopmentConfig')
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='test*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()



