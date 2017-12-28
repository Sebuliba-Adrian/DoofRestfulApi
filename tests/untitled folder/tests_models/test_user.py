"""
    Class contains tests for the user model
"""
from app.models.user import UserModel
from unittest import TestCase

class UserModelTest(TestCase):
    def test_create_user(self):
        user = UserModel('testusername', 'testpassword')

        self.assertEqual(user.username, 'testusername',"error try again" )
        self.assertEqual(user.password, 'testpassword', "error try again")

