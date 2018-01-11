import json

from tests import BaseTestCase


class UserResourceTest(BaseTestCase):
    """Ensure a new user resource can be added to the database."""

    def test_successful_registration(self):
        user_data = {"username": "testusername",
                     "password": "Ss$9Ly&2Rn$1", 
                     "email":"adrian@example.com"}
        response = self.app.post("/auth/register", data=user_data)
        msg = json.loads(response.data)

        self.assertIn(msg['message'], 'New user successfully registered!')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_existing_credentials(self):
        user_data = {"username": "testusername1",
                     "password": "Ss$9Ly&2Rn$1",
                     "email": "adrian1@example.com"}
        response = self.app.post("/auth/register", data=user_data)
        msg = json.loads(response.data)
        self.assertEqual(str(msg['message']),
                         'The username or email is already registered')
        self.assertEqual(response.status_code, 400)

    def test_succesful_login(self):
        user_data = {'username': 'testusername1',
                     'password': 'Ss$9Ly&2Rn$1'}
        response = self.app.post("/auth/login", data=user_data)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_without_credentials(self):
        user_data = {'username': '', 'password': ''}
        response = self.app.post("/auth/login", data=user_data)
        msg = json.loads(response.data)
        self.assertIn(msg['message'], 'one or more fields is not complete')
        self.assertEqual(response.status_code, 400)
