from app.models import UserModel
from app.utilities import username_validator
from tests import BaseTestCase


class UserTest(BaseTestCase):
    def test_crud(self):
        user = UserModel(username='testusername', password='testpassword')
        self.assertIsNone(UserModel.find_by_username('testusername'))
        self.assertIsNotNone(UserModel.find_by_id(1))

        user.save_to_db()

        self.assertIsNotNone(UserModel.find_by_username('testusername'))
        self.assertIsNotNone(UserModel.find_by_id(1))


class UserValidationTest(BaseTestCase):

    def test_valid_username(self):
        """Ensure that a valid username is provided as input to 
        the api"""
        self.assertEqual(username_validator("Sebuliba_A."), "Sebuliba_A.")

    def test_blank_username(self):
        """Ensure that no blank username are provided as input to 
        the api"""
        self.assertRaises(ValueError, username_validator, "  ")

    def test_none_input_for_username(self):
        """Ensure that none username are not provide as inputs to 
        the api"""
        self.assertRaises(ValueError, username_validator, None)

    def test_usename_below_4_characters(self):
        """Ensure that username below 4 characters are not allowed"""
        self.assertRaises(ValueError, username_validator, 'adr')

    def test_username_above_15_characters(self):
        """Ensure that username of characters above 15 are not allowed"""
        self.assertRaises(ValueError, username_validator,
                          'adrian.sebulibam')

    def test_username_contains_special_characters(self):
        """Ensure that the username doesnot contain special characters 
        except dots and underscores"""
        self.assertRaises(ValueError, username_validator, '*()#$%')
