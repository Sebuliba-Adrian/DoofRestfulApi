from tests.base import BaseTestCase
from models.recipe import RecipeModel
from models.category import CategoryModel


class RecipeTest(BaseTestCase):
    def test_crud(self):
        with self.app_context():
            CategoryModel('Beverages').save_to_db()
            recipe = RecipeModel('African tea', 'add stuf', 1)

            self.assertIsNone(RecipeModel.find_by_name(''),
                              "Found a recipe with name {}, but expected not to.".format(recipe.name))

            recipe.save_to_db()

            self.assertIsNotNone(RecipeModel.find_by_name('African tea'))

            recipe.delete_from_db()

            self.assertIsNone(RecipeModel.find_by_name('African tea'))

    def test_category_relationship(self):
        with self.app_context():
            category = CategoryModel('test_category')
            recipe = RecipeModel('test_recipe', 'Add stuff', 1)

            category.save_to_db()
            recipe.save_to_db()

            self.assertEqual(recipe.category.name, 'test_category')
