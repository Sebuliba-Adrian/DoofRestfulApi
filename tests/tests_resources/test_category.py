import json
from tests.base import BaseTestCase
from models.category import CategoryModel
from models.recipe import RecipeModel


class CategoryTest(BaseTestCase):
    """Ensures that the category resource functions as expectected"""

    def test_create_category(self):
        """Ensure that a recipe category is created """

        with self.app() as client:
            with self.app_context():
                resp = client.post('/category/somerecipecategory')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(
                    CategoryModel.find_by_name('somerecipecategory'))
                self.assertDictEqual({'id': 1, 'name': 'somerecipecategory', 'recipes': []},
                                     json.loads(resp.data))

    def test_create_duplicate_category(self):
        """Ensure that no duplicate categories are created"""
        with self.app() as client:
            with self.app_context():
                client.post('/category/somerecipecategory')
                resp = client.post('/category/somerecipecategory')

                self.assertEqual(resp.status_code, 400)

    def test_delete_category(self):
        """Ensure that a category gets deleted from storage """
        with self.app() as client:
            with self.app_context():
                CategoryModel('somecategory').save_to_db()
                resp = client.delete('/category/somecategory')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Category deleted'},
                                     json.loads(resp.data))

    def test_find_category(self):
        """Ensure that a category can be found """
        with self.app() as client:
            with self.app_context():
                CategoryModel('somecategory').save_to_db()
                resp = client.get('/category/somecategory')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'somecategory', 'recipes': []},
                                     json.loads(resp.data))

    def test_category_not_found(self):
        """Test whether a category cannot be found"""
        with self.app() as client:
            with self.app_context():
                resp = client.get('/category/somecategory')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Category not found'},
                                     json.loads(resp.data))

    def test_category_found_with_recipes(self):
        """Ensure that a category can be found with recipes"""
        with self.app() as client:
            with self.app_context():
                CategoryModel('Beverage').save_to_db()
                RecipeModel(
                    'African Tea', "Add two spoonfuls of tea leaves...", 1).save_to_db()

                resp = client.get('/category/Beverage')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'Beverage', 'recipes': [{'name': 'African Tea', 'description': 'Add two spoonfuls of tea leaves...'}]},
                                     json.loads(resp.data))

    def test_category_list(self):
        """Ensure that a category list is retrieved """
        with self.app() as client:
            with self.app_context():
                CategoryModel('somecategory').save_to_db()

                resp = client.get('/categories')
                self.assertDictEqual({'categories': [{'id': 1, 'name': 'somecategory', 'recipes': []}]},
                                     json.loads(resp.data))

    def test_category_list_with_recipes(self):
        """Ensure that the category list has recipes """
        pass
                                 
