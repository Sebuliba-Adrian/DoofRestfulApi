from app.models import RecipeModel
from unittest import TestCase


class RecipeTest(TestCase):
    def test_create_recipe(self):
        recipe = RecipeModel(
            name='African Tea', description="Add two spoonful of tea leaves... ", category_id=1)

        self.assertEqual(recipe.name, 'African Tea',
                         "The name of the recipe after creation does not equal the constructor argument.")
        self.assertEqual(recipe.description,  "Add two spoonful of tea leaves... ",
                         "The description of the recipe after creation is wrong!.")
        self.assertEqual(recipe.category_id, 1,
                         "The category_id of the recipe after creation does not equal the constructor argument.")
        self.assertIsNone(
            recipe.category, "The recipe's category was not None even though it was not created.")
