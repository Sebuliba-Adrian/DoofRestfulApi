import json
import os
from flask_testing import TestCase

from run import db, app

from app.models import UserModel, CategoryModel, RecipeModel


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(TestCase):
    recipe_data = {"name": "African Tea",
                   "description": "Add  2spoonfuls..."}
    user = 1

    def create_app(self):
        app.config.from_object('config.config.TestingConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.database = db
        db.create_all()

        # Add dummy data for test purposes
        user = UserModel(username="testusername1")
        user.email='adrian1@example.com'
        user.password = 'Ss$9Ly&2Rn$1'
        user.save_to_db()

        user2 = UserModel(username="testusername2")
        user2.email='adrian2@email.com'
        user2.password = 'Ss$9Ly&2Rn$1'
        user2.save_to_db()

        user3 = UserModel(username="testusername3")
        user3.email='adrian3@gmail.com'
        user3.password = 'Ss$9Ly&2Rn$1'
        user3.save_to_db()

        category1 = CategoryModel(
            name="somerecipecategory", created_by=1)
        category1.save_to_db()
        category2 = CategoryModel(
            name="somerecipecategory2", created_by=1)
        category2.save_to_db()

        recipe1 = RecipeModel(
            name="somerecipe1",
            description="Add one spoonfuls of...",
            created_by=1, category_id=1)
        recipe1.save_to_db()
        recipe2 = RecipeModel(
            name="somerecipe2", description="Add two spoonfuls of...",
            created_by=1, category_id=2)
        recipe2.save_to_db()

    def make_token(self):
        user_data = {'username': 'testusername1',
                     'password': 'Ss$9Ly&2Rn$1'}
        response = self.app.post("/auth/login", data=user_data)
        token = json.loads(response.data)['access_token']

        authorization = {'Authorization': 'Bearer {0}'.format(token)}
        return authorization

    def make_second_user_token(self):
        user_data = {'username': 'testusername2',
                     'password': 'Ss$9Ly&2Rn$1'}
        response = self.app.post("/auth/login", data=user_data)
        token = json.loads(response.data)['access_token']
        authorization = {'Authorization': 'Bearer {0}'.format(token)}
        return authorization

    def make_invalid_token(self):
        user_data = {'username': 'testusername3',
                     'password': 'Ss$9Ly&2Rn$1'}
        response = self.app.post("/auth/login", data=user_data)
        token = json.loads(response.data)['access_token'] + "98hjjhbhgbdj"
        authorization = {'Authorization': 'Bearer {0}'.format(token)}
        return authorization

    def tearDown(self):
        db.session.remove()
        db.drop_all()
