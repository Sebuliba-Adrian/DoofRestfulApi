
from tests import BaseTestCase
from app.models.user import UserModel


class UserTest(BaseTestCase):
    def test_crud(self):

        user = UserModel('testusername', 'testpassword')
        self.assertIsNone(UserModel.find_by_username('testusername'))
        self.assertIsNone(UserModel.find_by_id(1))

        user.save_to_db()

        self.assertIsNotNone(UserModel.find_by_username('testusername'))
        self.assertIsNotNone(UserModel.find_by_id(1))
