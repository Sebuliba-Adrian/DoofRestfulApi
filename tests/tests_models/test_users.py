"""
    Class contains tests for the user model
"""
from app.models import UserModel
from unittest import TestCase


class UserModelTest(TestCase):
    def test_create_user(self):
        user = UserModel(username='testusername')
        user.password = 'testpassword'

        self.assertEqual(user.username, 'testusername', "error try again")
        self.assertTrue(user.verify_password('testpassword')
                        , "error try again")
