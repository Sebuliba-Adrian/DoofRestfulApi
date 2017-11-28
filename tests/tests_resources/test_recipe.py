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
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverages').save_to_db()
                RecipeModel(
                    'African Tea', 'Add two spoonfuls of tea leaves...', 1).save_to_db()

                resp = client.delete('/recipe/African Tea')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Recipe deleted'},
                                     json.loads(resp.data))

    def test_create_recipe(self):
        """Tests for creation of a recipe"""
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverages').save_to_db()

                resp = client.post(
                    '/recipe/African tea', data={'description': 'Add two spoonfuls of...', 'category_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'African tea', 'description': 'Add two spoonfuls of...'},
                                     json.loads(resp.data))

    def test_create_duplicate_recipe(self):
        """Ensures that there are no duplicate recipes"""
        pass

    def test_put_recipe(self):
        """Tests for editting a recipe"""
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverages').save_to_db()
                resp = client.put(
                    '/recipe/African tea', data={'description': 'Add two spoonfuls of...', 'category_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(RecipeModel.find_by_name(
                    'African tea').description, 'Add two spoonfuls of...')
                self.assertDictEqual({'name': 'African tea', 'description':  'Add two spoonfuls of...'},
                                     json.loads(resp.data))

    def test_put_update_recipe(self):
        """"""
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverages').save_to_db()
                RecipeModel('African tea',
                            'Add two spoonfuls of...', 1).save_to_db()

                self.assertEqual(RecipeModel.find_by_name(
                    'African tea').description, 'Add two spoonfuls of...')

                resp = client.put(
                    '/recipe/African tea', data={'description': 'Add one spoonfuls of...', 'category_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(RecipeModel.find_by_name(
                    'African tea').description, 'Add one spoonfuls of...')
                self.assertDictEqual({'name': 'African tea', 'description': 'Add one spoonfuls of...'},
                                     json.loads(resp.data))

    def test_recipe_list(self):
        """Tests for getting a list of recipes"""
        pass
