from models.category import CategoryModel
from models.user import UserModel
from models.recipe import RecipeModel
from tests.base import BaseTestCase
import json


class RecipeTest(BaseTestCase):
    """This class handles test cases for recipes """

    def setUp(self):
        BaseTestCase.setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('testusername', 'testpassword').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps(
                                               {'username': 'testusername', 'password': 'testpassword'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT {auth_token}'

    def test_get_recipe_no_auth(self):
        """Tests for getting recipes without authentication"""
        pass

    def test_get_recipe_not_found(self):
        """Tests for recipe not found"""
        pass

    def test_get_recipe(self):
        """Tests for getting recipe"""
        pass

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
