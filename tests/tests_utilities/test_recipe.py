from tests.base import BaseTestCase
from models.user import UserModel


class UserTest(BaseTestCase):
    def test_crud(self):
        with self.app_context():
            user = UserModel('testusername', 'testpassword')

            self.assertIsNone(UserModel.find_by_username('testusername'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('testusername'))
            self.assertIsNotNone(UserModel.find_by_id(1))
