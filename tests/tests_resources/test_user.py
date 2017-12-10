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

    def test_missing_username_at_login(self):
        """Ensure that username is not missing at login"""
        with self.app() as client:
            with self.app_context():
                auth_response = client.post('/login',
                                              data=json.dumps(
                                                  {'username': '', 'password': 'testpassword'}),
                                              headers={'Content-Type': 'application/json'})

                self.assertEqual(auth_response.status_code, 400)
                self.assertDictEqual({'message': 'Missing username parameter'},
                                     json.loads(auth_response.data))

    def test_missing_password_at_login(self):
        """Ensure that password is not missing at login"""
        with self.app() as client:
            with self.app_context():
                auth_response = client.post('/login',
                                              data=json.dumps(
                                                  {'username': 'testusername', 'password': ''}),
                                              headers={'Content-Type': 'application/json'})

                self.assertEqual(auth_response.status_code, 400)
                self.assertDictEqual({'message': 'Missing password parameter'},
                                     json.loads(auth_response.data))

    def test_wrong_credentials_at_login(self):
        """Ensure that the username and password are not wrong"""
        with self.app() as client:
            with self.app_context():
                auth_response = client.post('/login',
                                              data=json.dumps(
                                                  {'username': 'wrongusername', 'password': 'wrongpassword'}),
                                              headers={'Content-Type': 'application/json'})

                self.assertEqual(auth_response.status_code, 401)
                self.assertDictEqual({'message': 'Bad username or password'},
                                     json.loads(auth_response.data))

    def test_login_non_json_input(self):
        """Ensure that only json input is taken in"""
        with self.app() as client:
            with self.app_context():
                response = client.post('/login', data=self.non_json_data,
                                         content_type='application/json')
                self.assertEqual(response.status_code, 400)

    def test_login_invalid_json_keys(self):
        """Ensure that json keys are not invalid"""
        with self.app() as client:
            with self.app_context():
                response = client.post('/login',
                                         data=json.dumps(self.wrong_keys_data),
                                         content_type='application/json')
                self.assertEqual(response.status_code, 400)

                
