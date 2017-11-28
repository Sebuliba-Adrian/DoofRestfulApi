from models.category import CategoryModel
from models.user import UserModel
from models.recipe import RecipeModel
from tests.base import BaseTestCase
import json


class RecipeTest(BaseTestCase):
    """This class handles test cases for recipes """

    def setUp(self):
        super(RecipeTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('testusername', 'testpassword').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps(
                                               {'username': 'testusername', 'password': 'testpassword'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT {0}'.format(auth_token)

    def test_get_recipe_no_auth(self):
        """Tests for getting recipes without authentication"""
        with self.app() as client:
            with self.app_context():
                resp = client.get('/recipe/African Tea')
                self.assertEqual(resp.status_code, 401)

    def test_get_recipe_not_found(self):
        """Tests for recipe not found"""
        with self.app() as client:
            with self.app_context():
                resp = client.get(
                    '/recipe/African Tea', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_recipe(self):
        """Tests for getting recipe"""
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverages').save_to_db()
                RecipeModel(
                    'African Tea', 'Add two spoonfuls of tea leaves...', 1).save_to_db()
                resp = client.get('/recipe/African Tea',
                                  headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_recipe(self):
        """Tests for deleting recipe"""
        pass

    def test_create_recipe(self):
        """Tests for creation of a recipe"""
        pass

    def test_create_duplicate_recipe(self):
        """Ensures that there are no duplicate recipes"""
        pass

    def test_put_recipe(self):
        """Tests for editting a recipe"""
        pass

    def test_put_update_recipe(self):
        """"""
        pass

    def test_recipe_list(self):
        """Tests for getting a list of recipes"""
        pass
