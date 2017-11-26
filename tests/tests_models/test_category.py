from models.category import CategoryModel

from unittest import TestCase

class CategoryTest(TestCase):
    def test_create_category(self):
        category = CategoryModel('test')

        self.assertEqual(category.name, 'test',
                         "The name of the category after creation does not equal the constructor argument.")

    