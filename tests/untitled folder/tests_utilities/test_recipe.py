from tests import BaseTestCase
from app.models.recipe import RecipeModel
from app.models.category import CategoryModel
from app.models.user import UserModel


class RecipeTest(BaseTestCase):
    def test_crud(self):
        
        UserModel("testusername","testpassword").save_to_db()
        CategoryModel(name='Beverages', user_id = self.user).save_to_db()
        recipe = RecipeModel('African tea', 'add stuf', 1)

        self.assertIsNone(RecipeModel.find_by_name(''),
                            "Found a recipe with name {}, but expected not to.".format(recipe.name))

        recipe.save_to_db()

        self.assertIsNotNone(RecipeModel.find_by_name('African tea'))

        recipe.delete_from_db()

        self.assertIsNone(RecipeModel.find_by_name('African tea'))

    def test_category_relationship(self):
        
        user=UserModel("testusername","testpassword").save_to_db()

        category = CategoryModel(name='test_category', user_id = self.user)
        recipe = RecipeModel('test_recipe', 'Add stuff', 1)

        category.save_to_db()
        recipe.save_to_db()

        self.assertEqual(recipe.category.name, 'test_category')