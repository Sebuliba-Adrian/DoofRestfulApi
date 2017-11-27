from models.user import UserModel
from  unittest import TestCase
from tests.base import BaseTestCase
import json

class UserResourceTest(BaseTestCase):
    def test_register_user(self):
                client=BaseTestCase.create_app().test_client()
                response = client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('testusername'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))
            
    
