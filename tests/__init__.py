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
        user.save_to_db()

        user2 = UserModel(username="testusername2")
        user2.password = 'testpassword'
        user2.save_to_db()

        category1 = CategoryModel(
            name="somerecipecategory", created_by=1)
        category1.save_to_db()
        category2 = CategoryModel(
            name="somerecipecategory2", created_by=1)
        category2.save_to_db()    

        recipe1 = RecipeModel(
            name="somerecipe1", description="Add one spoonfuls of...", created_by=1, category_id=1)
        recipe1.save_to_db()    
        recipe2 = RecipeModel(
            name="somerecipe2", description="Add two spoonfuls of...", created_by=1, category_id=2)
        recipe2.save_to_db()    


    def make_token(self):
        self.user_data = {'username': 'testusername1',
                          'password': 'testpassword'}
        response = self.app.post("/auth/login", data=self.user_data)
        output = json.loads(response.data)
        token = json.loads(response.data)['access_token']
        
        self.authorization = {'Authorization': 'Bearer {0}'.format(token)}
        return self.authorization

    def make_second_user_token(self):
        self.user_data = {'username': 'testusername2',
                          'password': 'testpassword'}
        response = self.app.post("/auth/login", data=self.user_data)
        output = json.loads(response.data)
        # token = output.get("access_token").encode("ascii")
        print(output)
        token = json.loads(response.data)['access_token']
        self.authorization = {'Authorization': 'Bearer {0}'.format(token)}
        return self.authorization

    def tearDown(self):
        db.session.remove()
        db.drop_all()
