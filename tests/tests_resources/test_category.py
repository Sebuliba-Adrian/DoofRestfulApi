import json
from tests.base import BaseTestCase
from models.category import CategoryModel


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
