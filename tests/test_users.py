"""
    Class contains tests for the user model
    
"""
from unittest import TestCase
from models.user import UserModel

class UserModelTest(TestCase):
    def test_create_user(self):
        user = UserModel('testusername', 'testpassword')

        self.assertEqual(user.username, 'testusername',"error try again" )
        self.assertEqual(user.password, 'testpassword', "error try again")

