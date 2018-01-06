from app.models import CategoryModel, RecipeModel, UserModel
from app.utilities import recipe_name_validator
from tests import BaseTestCase


class RecipeTest(BaseTestCase):
    def test_crud(self):
        user = UserModel(username="testusername", password="testpassword")
        user.save_to_db()
        category = CategoryModel(name='Beverages', user=user)
        recipe = RecipeModel(
            name='African tea', description='add stuf',
            user=user, category=category)

        self.assertIsNone(RecipeModel.find_by_name(''),
                          "Found a recipe with name {}, but expected not to."
                          .format(recipe.name))

        recipe.save_to_db()

        self.assertIsNotNone(RecipeModel.find_by_name('African tea'))

        recipe.delete_from_db()

        self.assertIsNone(RecipeModel.find_by_name('African tea'))

    def test_category_relationship(self):
        user = UserModel(username="testusername",
                         password="testpassword")
        user.save_to_db()

        category = CategoryModel(name='test_category', user=user)
        recipe = RecipeModel(name='test_recipe',
                             description='Add stuff', user=user,
                             category=category)

        category.save_to_db()
        recipe.save_to_db()

        self.assertEqual(recipe.category.name, 'test_category')


class RecipeValidationTest(BaseTestCase):

    def test_input_for_valid_recipename(self):
        """Ensure that a valid recipe name actually gets 
        returned """
        self.assertEqual(recipe_name_validator("somerecipe"), 'somerecipe')

    def test_blank_recipename(self):
        """Ensure that no blank recipenames are provided as input to 
        the api"""
        self.assertRaises(ValueError, recipe_name_validator, "  ")

    def test_none_input_for_recipename(self):
        """Ensure that none recipename are not provide as inputs to 
        the api"""
        self.assertRaises(ValueError, recipe_name_validator, None)

    def test_recipename_contains_special_characters(self):
        """Ensure that the recipename doesnot contain any special characters
        """
        self.assertRaises(ValueError, recipe_name_validator, '*()#$%')
