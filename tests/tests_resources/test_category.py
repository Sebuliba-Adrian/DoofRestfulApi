import json
from tests import BaseTestCase


class CategoryTest(BaseTestCase):
    """Ensures that the category resource functions as expectected"""

    def test_user_logout(self):
        response = self.app.delete(
            "/auth/logout", headers=self.make_token(),
            content_type='application/json')

        msg = json.loads(response.data)
        print(msg)
        self.assertIn(msg['message'], 'Successfully logged out')
        self.assertEqual(response.status_code, 200)

    def test_requesting_category_without_auth(self):
        response = self.client.get(
            "/categories", content_type='application/json')
        msg = str(response.json['message'])

        self.assertEqual(msg, 'No authorization token provided')
        self.assertEqual(response.status_code, 401)

    def test_requesting_otherusers_categories(self):
        response = self.client.get(
            "/categories/1", headers=self.make_second_user_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_requesting_categories(self):
        response = self.client.get(
            "/categories", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Your request was not found. Please try again')
        self.assertEqual(response.status_code, 404)

    def test_editing_a_category_withno_auth(self):
        category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/categories/1", data=category,
            headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_creation_of_a_category(self):
        """ Test for creation of a category """
        category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.post(
            "/categories", data=category, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Category created Successfully')
        self.assertEqual(response.status_code, 200)

    def test_category_creation_with_invalid_token(self):
        """ Test for creation of a category with invalid token """
        category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.post(
            "/categories", data=category, headers=self.make_invalid_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Invalid Token')
        self.assertEqual(response.status_code, 422)

    def test_creation_of_a_category_without_name(self):
        """ Test for creation of a category """
        category = {"description": "lunch at 1:00pm"}
        response = self.client.post(
            "/categories", data=category, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please provide a name for the category')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_a_category_with_existing_name(self):
        """ Test for creation of a category with existing name """
        category = {"name": "somerecipecategory",
                    "description": "dance time"}
        response = self.client.post(
            "/categories", data=category, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You already have a category with that name')
        self.assertEqual(response.status_code, 400)

    def test_deletion_of_a_category(self):
        """ Test deletion of a category """
        response = self.app.delete(
            "/categories/1", headers=self.make_token(),
            content_type='application/json')

        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_deletion_of_other_user_categories(self):
        """ Test deletion of a category """
        response = self.app.delete(
            "/categories/1", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to delete this')
        self.assertEqual(response.status_code, 401)

    def test_deletion_of_a_none_existent_category(self):
        """ Test deletion of a category """
        response = self.app.delete(
            "/categories/10", headers=self.make_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_categories(self):
        """ Test listing all categories via a get request """
        response = self.app.get(
            "/categories", headers=self.make_token(),
            content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_editing_a_category_that_doesnt_exist(self):
        """ Test editing a categories that doesn't exist """
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.app.put(
            "/categories/2000", data=self.category,
            headers=self.make_token(), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_editing_a_category_without_auth(self):
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/categories/1", data=self.category,
            headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_other_users_categories(self):
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/categories/1", headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_a_category(self):
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/categories/1", data=self.category, headers=self.make_token())
        print(response.data)
        self.assertEqual(response.status_code, 201)

    def test_get_single_category(self):
        """ Test listing a single category"""
        response = self.app.get("/categories/1",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 200)

    def test_get_none_existent_category(self):
        """ Test get request on a none existent category """
        response = self.app.get("/categories/50",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 404)

    def test_input_on_get_categories_request(self):
        response = self.app.get("/categories?limit=abc",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please use numbers to define the limit')
        self.assertEqual(response.status_code, 400)

    def test_pagination(self):
        """Tests specified number of pages returned from GET request."""
        response = self.client.get("/categories?page=1",
                                   content_type="application/json",
                                   headers=self.make_token())
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertTrue(response_msg["next"], "None")

    def test_invalid_pagination(self):
        """Tests error raised for non-integer pagination request."""
        response = self.client.get("/categories?page=invalid",
                                   content_type="application/json",
                                   headers=self.make_token())
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("use numbers", response_msg["message"])

    def test_search_by_category_name(self):
        """Tests category can be retrieved from search."""
        response = self.client.get("/categories?q=somerecipecategory",
                                   content_type="application/json",
                                   headers=self.make_token())
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertEqual(
            "somerecipecategory", response_msg["categories"][0]["name"])

    def test_invalid_search(self):
        """Tests error raised for invalid search."""
        response = self.client.get("/categories?q=invalid",
                                   content_type="application/json",
                                   headers=self.make_token())
        self.assertEqual(response.status_code, 404)
