from models.user import UserModel
from  unittest import TestCase
from tests.base import BaseTestCase
import json

class UserResourceTest(BaseTestCase):
    """Ensure a new user resource can be added to the database."""
    def test_register_user(self):
        """Ensure that user resource  is registered"""
         with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('testusername'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))
            
    
