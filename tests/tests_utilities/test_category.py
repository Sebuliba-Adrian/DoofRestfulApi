from models.recipe import RecipeModel
from models.category import CategoryModel

from tests.base import BaseTestCase


class CategoryTest(BaseTestCase):
    def test_create_category_recipes_empty(self):
        category = CategoryModel('Beverages')

        self.assertListEqual(category.recipes.all(), [],
                             "The categories recipes length was not 0 even though no recipes were added.")

    def test_crud(self):
        with self.app_context():
            category = CategoryModel('Beverages')

            self.assertIsNone(CategoryModel.find_by_name('Beverages'))

            category.save_to_db()

            self.assertIsNotNone(CategoryModel.find_by_name('Beverages'))

            category.delete_from_db()

            self.assertIsNone(CategoryModel.find_by_name('Beverages'))

    def test_category_relationship(self):
        with self.app_context():
            category = CategoryModel('Beverages')
            recipe = RecipeModel('test_recipe', "Add stuff", 1)

            category.save_to_db()
            recipe.save_to_db()

            self.assertEqual(category.recipes.count(), 1)
            self.assertEqual(category.recipes.first().name, 'test_recipe')

    def test_category_json(self):
        category = CategoryModel('Beverages')
        expected = {
            'id': None,
            'name': 'Beverages',
            'recipes': []
        }

        self.assertDictEqual(category.json(), expected)

    def test_category_json_with_recipe(self):
        with self.app_context():
            category = CategoryModel('Beverages')
            recipe = RecipeModel('test_recipe', 'Add stuff', 1)

            category.save_to_db()
            recipe.save_to_db()

            expected = {
                'id': 1,
                'name': 'Beverages',
                'recipes': [{'name': 'test_recipe', 'description': 'Add stuff'}]
            }

            self.assertDictEqual(category.json(), expected)