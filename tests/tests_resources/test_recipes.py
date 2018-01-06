from tests import BaseTestCase
class RecipeTest(BaseTestCase):
    """This class handles test cases for recipes """

    def test_recipe_creation(self):
        """ Test for response on new recipe creation """

        response = self.app.post(
            "/categories/2/recipes/", data=self.recipe_data,
            headers=self.make_token())
        self.assertEqual(response.status_code, 201)

    def test_recipe_creation_with_invalid_token(self):
        response = self.app.post(
            "/categories/2/recipes/", data=self.recipe_data,
            headers=self.make_invalid_token())
        msg = str(response.json['message'])

        self.assertEqual(msg, 'Invalid Token')
        self.assertEqual(response.status_code, 422)
    def test_recipe_creation_with_invalid_url(self):

        response = self.app.post(
            "/categories/2/recipes/1", data=self.recipe_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        print(response.status_code)
        self.assertEqual(
            msg, 'The method is not allowed for the requested URL.')
        self.assertEqual(response.status_code, 405)

    def test_recipe_creation_with_invalid_credentials(self):
        recipe_data = {"namee": "African Tea",
                       "description": "Add 2spoonfuls of..."}
        response = self.app.post(
            "/categories/2/recipes/", data=recipe_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'Please provide a name for the recipe')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_duplicate_recipe(self):
        recipe_data = {"name": "somerecipe1",
                       "description": "Add one spoonfuls of..."}
        response = self.app.post(
            "/categories/2/recipes/", data=recipe_data,
            headers=self.make_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'That name is already taken, try again')
        self.assertEqual(response.status_code, 400)

    def test_creation_of_recipe_in_none_existent_category(self):

        response = self.app.post(
            "/categories/200/recipes/", data=self.recipe_data,
            headers=self.make_token())
        self.assertEqual(response.status_code, 404)

    def test_creation_of_recipe_in_other_users_categories(self):
        response = self.app.post(
            "/categories/1/recipes/", data=self.recipe_data,
            headers=self.make_second_user_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to use the category')
        self.assertEqual(response.status_code, 401)

    def test_editing_a_recipe(self):
        """ Test for editing a recipe """
        recipe = {"name": "African Tea",
                       "description": "Add 2spoonfuls of..."}
        response = self.app.put(
            "/categories/1/recipes/1",
            headers=self.make_token(),
            data=recipe)
        msg = str(response.json['message'])
        
        self.assertEqual(msg, 'Recipe updated')
        self.assertEqual(response.status_code, 200)

    def test_editing_other_users_recipe(self):
        """ Test for editing a recipe """
        recipe = {"name": "African Tea",
                       "description": "Add 2spoonfuls of..."}
        response = self.app.put(
            "/categories/1/recipes/1",
            headers=self.make_second_user_token(),
            data=recipe)
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to edit this')
        self.assertEqual(response.status_code, 401)

    def test_editing_recipe_with_invalid_url(self):
        recipe = {"name": "African Tea",
                       "description": "Add 2spoonfuls of..."}
        response = self.app.put(
            "/categories/1/recipes/",
            headers=self.make_token(),
            data=recipe)
        msg = str(response.json['message'])
        self.assertEqual(
            msg, 'The method is not allowed for the requested URL.')
        self.assertEqual(response.status_code, 405)

    def test_editing_none_existent_category_and_recipe(self):

        response = self.app.put(
            "/categories/100/recipes/100",
            headers=self.make_token(),
            data=self.recipe_data)
        self.assertEqual(response.status_code, 404)
    def test_recipe_request_on_none_existent_category(self):
        response = self.app.get("/categories/4/recipes/1",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 404)
    def test_invalid_credentials_on_recipe_request(self):
        response = self.app.get("/categories/1/recipes/1",
                                headers=self.make_second_user_token())
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to view this')
        self.assertEqual(response.status_code, 401)
    def test_requesting_a_none_existent_recipe(self):
        """Ensure that a non existing recipe is not returned"""
        response = self.app.get("/categories/1/recipes/20",
                                headers=self.make_token())
        self.assertEqual(response.status_code, 404)
    def test_deletion_of_an_recipe(self):
        """ Test for deletion of an recipe  """
        response = self.app.delete("/categories/2/recipes/1",
                                   headers=self.make_token(),
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'The recipe has been successfully deleted')
        self.assertEqual(response.status_code, 200)
    def test_deletion_of_recipe_in_other_user_categories(self):
        """ Test for deletion of an recipe  """
        response = self.app.delete("/categories/1/recipes/1",
                                   headers=self.make_second_user_token(),
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(msg, 'You are not authorized to del this')
        self.assertEqual(response.status_code, 401)
    def test_deletion_of_a_none_existent_recipe(self):
        response = self.app.delete("/categories/2/recipes/300",
                                   headers=self.make_token(),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_deleting_an_recipe_with_invalid_url(self):
        response = self.app.delete("/categories/2/recipes/",
                                   headers=self.make_token(), 
                                   content_type='application/json')
        msg = str(response.json['message'])
        self.assertEqual(
            msg, 'The method is not allowed for the requested URL.')
        self.assertEqual(response.status_code, 405)
