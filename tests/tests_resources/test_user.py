from app.models import UserModel
from unittest import TestCase
from tests import BaseTestCase
import json


class UserResourceTest(BaseTestCase):
    """Ensure a new user resource can be added to the database."""

    def test_successful_registration(self):
        self.user_data = {"username": "testusername",
                          "password": "testpasssword"}
        response = self.app.post("/auth/register", data=self.user_data)
        msg = json.loads(response.data)
        

        print(response.data)
        self.assertIn(msg['message'], 'New user successfully registered!')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_existing_credentials(self):
        self.user_data = {"username": "testusername1",
                          "password": "testpasssword"}
        response = self.app.post("/auth/register", data=self.user_data)
        msg = json.loads(response.data)
        self.assertEqual(str(msg['message']),
                         'The username is already registered')
        self.assertEqual(response.status_code, 400)

    def test_succesful_login(self):
        self.user_data = {'username': 'testusername', 'password': 'testpasssword'}
        response = self.app.post("/auth/login", data=self.user_data)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_without_credentials(self):
        self.user_data = {'username': '', 'password': ''}
        response = self.app.post("/auth/login", data=self.user_data)
        msg = json.loads(response.data)
        self.assertIn(msg['message'], 'one or more fields is not complete')
        self.assertEqual(response.status_code, 400)
