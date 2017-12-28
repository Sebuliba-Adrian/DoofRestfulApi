from app.models.category import CategoryModel
from app.models.user import UserModel
from app.models.recipe import RecipeModel
from app.models.user import UserModel
from tests import BaseTestCase
import json


class RecipeTest(BaseTestCase):
    """This class handles test cases for recipes """

    def setUp(self):
        super(RecipeTest, self).setUp()
       
        UserModel('testusername', 'testpassword').save_to_db()
        auth_request = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {'username': 'testusername', 'password': 'testpassword'}),
                                    headers={'Content-Type': 'application/json'})
        auth_token = json.loads(auth_request.data)['access_token']
        self.access_token = 'Bearer {0}'.format(auth_token)

    def test_get_recipe_no_auth(self):
        """Tests for getting recipes without authentication"""
        
        category = 1
        recipe = 1
        resp = self.client.get(
            '/categories/{0}/recipes/{1}'.format(category, recipe))
        self.assertEqual(resp.status_code, 401)

    def test_get_recipe_not_found(self):
        """Tests for recipe not found"""
       
        recipe = 1
        resp = self.client.get(
            '/recipes/{0}'.format(recipe), headers={'Authorization': self.access_token})
        self.assertEqual(resp.status_code, 404)

    def test_get_recipe(self):
        """Tests for getting recipe"""
      
        category = 1
        recipe = 1
        CategoryModel(name='Beverages', user_id = self.user).save_to_db()

        RecipeModel(
            'African Tea', 'Add two spoonfuls of tea leaves...', 1).save_to_db()
        resp = self.client.get('/categories/{0}/recipes/{1}'.format(category, recipe),
                            headers={'Authorization': self.access_token})
        self.assertEqual(resp.status_code, 200)

    def test_delete_recipe(self):
        """Tests for deleting recipe"""
      
        category = 1
        recipe = 1

        CategoryModel(name='Beverages', user_id= self.user).save_to_db()
        RecipeModel(
            'African Tea', 'Add two spoonfuls of tea leaves...', 1).save_to_db()

        resp = self.client.delete(
            '/categories/{0}/recipes/{1}'.format(category, recipe), headers={'Authorization': self.access_token})
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual({'message': 'Recipe deleted'},
                                json.loads(resp.data))

    def test_create_recipe(self):
        """Tests for creation of a recipe"""
       
        category = 1
        CategoryModel(name='Beverages', user_id= self.user).save_to_db()

        resp = self.client.post(
            '/categories/{0}/recipes'.format(category), data={'name': 'African tea', 'description': 'Add two spoonfuls of...'}, headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 201)
        self.assertDictEqual({'name': 'African tea', 'description': 'Add two spoonfuls of...'},
                                json.loads(resp.data))

    def test_create_duplicate_recipe(self):
        """Ensures that there are no duplicate recipes"""
        
        category = 1
        CategoryModel(name='Beverages', user_id=self.user).save_to_db()
        RecipeModel('African tea',
                    "Add two spoonfuls of...", 1).save_to_db()

        resp = self.client.post(
            '/categories/{0}/recipes'.format(category), data={'name': 'African tea', 'description': 'Add two spoonfuls of...'}, headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual({'message': 'A recipe with name \'African tea\' already exists.'},
                                json.loads(resp.data))

    def test_create_recipe_non_existing_category(self):
        """Ensures that a recipe with no category is not created"""
        
        category_id = 2
        CategoryModel(name='Beverages', user_id=self.user).save_to_db()

        RecipeModel('African tea',
                    "Add two spoonfuls of...", 1).save_to_db()
        resp = self.client.post(
            '/recipes', data={'name': 'African Tea', 'description': 'Add two spoonfuls of...'}, headers={'Authorization': self.access_token})
        pass

    def test_put_recipe(self):
        """Tests for editting a recipe"""
        
        category = 1
        recipe = 1
        CategoryModel(name='Beverages', user_id=self.user).save_to_db()
        resp = self.client.put(
            '/categories/{0}/recipes/{1}'.format(category, recipe), data={'name': 'African Tea', 'description': 'Add two spoonfuls of...'}, headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(RecipeModel.find_by_id(
            recipe).description, 'Add two spoonfuls of...')
        self.assertDictEqual({'name': 'African Tea', 'description':  'Add two spoonfuls of...'},
                            json.loads(resp.data))

    def test_put_update_recipe(self):
        """"""
        
        category = 1
        recipe = 1
        CategoryModel(name='Beverages', user_id= self.user).save_to_db()
        RecipeModel('African tea',
                    'Add two spoonfuls of...', 1).save_to_db()

        self.assertEqual(RecipeModel.find_by_id(
            recipe).description, 'Add two spoonfuls of...')

        resp = self.client.put(
            '/categories/{0}/recipes/{1}'.format(category, recipe), data={'name': 'African tea', 'description': 'Add one spoonfuls of...'}, headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(RecipeModel.find_by_name(
            'African tea').description, 'Add one spoonfuls of...')
        self.assertDictEqual({'name': 'African tea', 'description': 'Add one spoonfuls of...'},
                                json.loads(resp.data))

    def test_recipe_list(self):
        """Tests for getting a list of recipes"""

        category = 1
        CategoryModel(name='Beverages', user_id= self.user).save_to_db()
        RecipeModel('African tea',
                    'Add two spoonfuls of...', 1).save_to_db()

        resp = self.client.get(
            '/categories/{0}/recipes'.format(category), headers={'Authorization': self.access_token})

        self.assertDictEqual({'recipes': [{'name': 'African tea', 'description': 'Add two spoonfuls of...'}]},
                                json.loads(resp.data))
