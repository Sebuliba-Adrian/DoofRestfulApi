from unittest import TestCase

from app import create_app, db




class BaseTestCase(TestCase):

    non_json_data = 'some non json data'
    string_with_only_integers = '1234'
    wrong_keys_data = {
        "wrong": "Value",
        "key": "Value"}
    user = 1

    # app.config.from_object('config.config.TestingConfig')

    def setUp(self):
        # Make sure database exists

        self.app = create_app('config.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Get a test client

        self.client = self.app.test_client()
        # self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
