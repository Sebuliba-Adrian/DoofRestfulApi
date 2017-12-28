import json

from tests import BaseTestCase


class CategoryTest(BaseTestCase):
    """Ensures that the category resource functions as expectected"""

    def test_invalid_url_on_creation_of_a_category(self):
        self.category = {"name": "Lunch", "description": "lunch at 1:00pm"}
        response = self.client.get(
            "/categories//", data=self.category, headers=self.make_token(),
            content_type='application/json')
        # print(response.data)
        # msg = str(response.json['Error'])
        # self.assertEqual(msg, 'The requested url was not found')
        # self.assertEqual(response.status_code, 404)
        # pass
        pass

    def test_requesting_a_category_without_auth(self):
        response = self.client.get(
            "/categories", content_type='application/json')
        msg = str(response.json['msg'])

        self.assertEqual(msg, 'Missing Authorization Header')
        self.assertEqual(response.status_code, 401)

    def test_requesting_other_users_categories(self):
        response = self.client.get(
            "/categories/1", headers=self.make_second_user_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_requesting_categories(self):
        response = self.client.get(
            "/categories", headers=self.make_second_user_token(),
            content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_editing_a_category_without_auth(self):
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/cstegories/1", data=self.category, headers=self.make_second_user_token(),
            content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_creation_of_a_category(self):
        """ Test for creation of a category """
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.post(
            "/categories", data=self.category, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Category updated Successfully')
        self.assertEqual(response.status_code, 200)

    def test_creation_of_a_category_without_name(self):
        """ Test for creation of a category """
        self.category = {"description": "lunch at 1:00pm"}
        response = self.client.post(
            "/categories", data=self.category, headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please provide a name for the category')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_a_category_with_existing_name(self):
        """ Test for creation of a category with existing name """
        self.category = {"name": "somerecipecategory", "description": "dance time"}
        response = self.client.post(
            "/categories", data=self.category, headers=self.make_token())
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
        self.assertEqual(response.status_code, 204)

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
        self.assertEqual(response.status_code, 204)

    def test_editing_a_category_without_auth(self):
        self.category = {"name": "lunch", "description": "lunch at 1:00pm"}
        response = self.client.put(
            "/categories/1", data=self.category, headers=self.make_second_user_token(),
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
        self.assertEqual(response.status_code, 204)

    def test_input_on_get_categories_request(self):
        response = self.app.get("/categories?limit=abc",
                                headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, ' provide an integer')
        self.assertEqual(response.status_code, 400)
