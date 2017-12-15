from unittest import TestCase

from app import app
from db import db


class BaseTestCase(TestCase):

    non_json_data = 'some non json data'
    wrong_keys_data = {
        "wrong": "Value",
        "key": "Value"}
    app.config.from_object('config.TestingConfig')

    def setUp(self):
        # Make sure database exists

        with app.app_context():
            db.create_all()
        # Get a test client

        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
