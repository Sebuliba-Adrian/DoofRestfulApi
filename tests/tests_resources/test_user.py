from models.user import UserModel
from unittest import TestCase
from tests.base import BaseTestCase
import json


class UserResourceTest(BaseTestCase):
    """Ensure a new user resource can be added to the database."""

    def test_register_user(self):
        """Ensure that user resource  is registered"""
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(
                    UserModel.find_by_username('testusername'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))

    def test_register_duplicate_user(self):
        """Ensure that user resource registered is not a duplicate"""
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register', data={'username': 'testusername', 'password': 'testpassword'})
                response = client.post(
                    '/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))

    def test_register_and_login(self):
        """Ensure that user can register and then login """
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register', data={'username': 'testusername', 'password': 'testpassword'})
                auth_response = client.post('/login',
                                            data=json.dumps(
                                                {'username': 'testusername', 'password': 'testpassword'}),
                                            headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(
                    auth_response.data).keys())
