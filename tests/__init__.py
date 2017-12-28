from flask_testing import TestCase

import os
from run import db, app

from app.models import UserModel, CategoryModel, RecipeModel

import json

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.config.TestingConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.database = db
        db.create_all()

        # Add dummy data for test purposes
        user = UserModel(username="testusername1")
        user.password = 'testpassword'

        user2 = UserModel(username="testusername2")
        user2.password = 'testpassword'

        c_list1 = CategoryModel(
            name="somerecipecategory", created_by=1)
        c_list2 = CategoryModel(
            name="somerecipecategory2", created_by=1)

        r_item1 = RecipeModel(
            name="somerecipe1", description="Add one spoonfuls of...", created_by=1, category_id=1)
        r_item2 = RecipeModel(
            name="somerecipe2", description="Add two spoonfuls of...", created_by=1, category_id=2)

        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

    def make_token(self):
        self.user_data = {'username': 'testusername1', 'password': 'testpassword'}
        response = self.app.post("/auth/login", data=self.user_data)
        output = json.loads(response.data)
        token = output.get("access_token").encode("ascii")
        self.authorization = {'Authorization': 'Token %s' % token}
        return self.authorization

    def make_second_user_token(self):
        self.user_data = {'username': 'testuserusername2', 'password': 'testpassword'}
        response = self.app.post("/auth/login", data=self.user_data)
        output = json.loads(response.data)
        token = output.get("access_token").encode("ascii")
        self.authorization = {'Authorization': 'Token %s' % token}
        return self.authorization

    def tearDown(self):
        db.session.remove()
        db.drop_all()
