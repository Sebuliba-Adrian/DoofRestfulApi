from app.models import CategoryModel, RecipeModel, UserModel
from tests import BaseTestCase


class CategoryTest(BaseTestCase):
    def test_create_category_recipes_empty(self):

        UserModel(username="testusername",
                  password="testpassword").save_to_db()

        category = CategoryModel(name='Beverages', created_by=self.user)

        self.assertListEqual(category.recipes.all(), [],
                             "The categories recipes length was not 0 even though no recipes were added.")

    def test_crud(self):

        UserModel(username="testusername",
                  password="testpassword").save_to_db()

        category = CategoryModel(name='Beverages', created_by=self.user)

        self.assertIsNone(CategoryModel.find_by_name('Beverages'))
        print(CategoryModel.find_by_name('Beverages'))

        category.save_to_db()

        self.assertIsNotNone(CategoryModel.find_by_name('Beverages'))

        category.delete_from_db()

        self.assertIsNone(CategoryModel.find_by_name('Beverages'))

    def test_category_relationship(self):

        user = UserModel(username="testusername", password="testpassword")
        user.save_to_db()

        category = CategoryModel(name='Beverages', user=user)
        category.save_to_db()
        recipe = RecipeModel(
            name='test_recipe', description="Add stuff", user=user, category=category)
        recipe.save_to_db()

        print(user.categories)
        self.assertEqual(category.recipes.count(), 1)

        self.assertEqual(category.recipes.first().name, 'test_recipe')

    def test_category_json(self):

        UserModel(username="testusername",
                  password="testpassword").save_to_db()

        category = CategoryModel(name='Beverages', created_by=self.user)
        expected = {
            'id': None,
            'name': 'Beverages',
            'recipes': []
        }

        self.assertDictEqual(category.json(), expected)

    def test_category_json_with_recipe(self):

        user = UserModel(username="testusername",
                         password="testpassword")
        user.save_to_db()

        category = CategoryModel(name='Beverages', user=user)
        recipe = RecipeModel(
            name='test_recipe', description='Add stuff', user=user, category=category)

        category.save_to_db()
        recipe.save_to_db()

        expected = {
            'id': 3,
            'name': 'Beverages',
            'recipes': [{'name': 'test_recipe', 'description': 'Add stuff'}]
        }

        # print(category.json())
        self.assertDictEqual(category.json(), expected)
