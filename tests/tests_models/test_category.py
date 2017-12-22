from models.category import CategoryModel
from models.user import UserModel

from unittest import TestCase

class CategoryTest(TestCase):
    def test_create_category(self):
        user= UserModel('testusername','testpassword')
        
        category = CategoryModel(name='categoryname', user=user)

        self.assertEqual(category.name, 'categoryname',
                         "The name of the category after creation in wrong!!.")

    