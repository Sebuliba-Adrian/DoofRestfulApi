from models.category import CategoryModel

from unittest import TestCase

class CategoryTest(TestCase):
    def test_create_category(self):
        category = CategoryModel('categoryname')

        self.assertEqual(category.name, 'categoryname',
                         "The name of the category after creation in wrong!!.")

    