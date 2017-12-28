from tests import BaseTestCase
from app.models.category import CategoryModel
from app.models.recipe import RecipeModel
from app.models.user import UserModel
import json


class CategoryTest(BaseTestCase):
    """Ensures that the category resource functions as expectected"""

    def setUp(self):
        super(CategoryTest, self).setUp()
     
        UserModel('testusername', 'testpassword').save_to_db()
        auth_request = self.client.post('/auth/login',
                                data=json.dumps(
                                    {'username': 'testusername', 'password': 'testpassword'}),
                                headers={'Content-Type': 'application/json'})
        auth_token = json.loads(auth_request.data)['access_token']
        self.access_token = 'Bearer {0}'.format(auth_token)

    def test_create_category(self):
        """Ensure that a recipe category is created """

      
        resp = self.client.post('/categories', data={'name': 'somerecipecategory'},
                            headers={'Authorization': self.access_token})
        print(resp.data)
        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(
            CategoryModel.find_by_name('somerecipecategory'))
        self.assertDictEqual({'id': 1, 'name': 'somerecipecategory', 'recipes': []},
                                json.loads(resp.data))

    def test_create_duplicate_category(self):
        """Ensure that no duplicate categories are created"""
       
        self.client.post('/categories', data={'name': 'somerecipecategory'},
                    headers={'Authorization': self.access_token})

        resp = self.client.post('/categories', data={'name': 'somerecipecategory'},
                            headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 400)

    def test_put_category(self):
        """Tests for editting a recipe"""
       
        category = 1
        CategoryModel(name='somerecipecategory',user_id=1).save_to_db()

        resp = self.client.put(
            '/categories/{0}'.format(category), data={'name': 'Tea'}, headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CategoryModel.find_by_id(
            category).name, 'Tea')
        self.assertDictEqual({'id': category, 'name': 'Tea', 'recipes': []},
                                json.loads(resp.data))

    def test_put_update_category(self):
        """Ensure that a category gets created for a put request"""

        category = 1

        CategoryModel(name='somerecipecategory',user_id=1).save_to_db()
        
        resp = self.client.put('/categories/{0}'.format(category),
                            data={'name': 'somenewrecipecategory'}, headers={'Authorization': self.access_token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CategoryModel.find_by_id(
            category).name, 'somenewrecipecategory')
        self.assertDictEqual({'id': 1, 'name': 'somenewrecipecategory', 'recipes': []},
                                json.loads(resp.data))

    def test_put_duplicate_category(self):
        """Ensure that no duplicate categories are created for a put request"""
     
        category = 1
        self.client.post('/categories', data={'name': 'somerecipecategory'},
                    headers={'Authorization': self.access_token})

        resp = self.client.put('/categories/{0}'.format(category), data={'name': 'somerecipecategory'},
                            headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual({'message': 'A category with name \'somerecipecategory\' already exists.'},
                                json.loads(resp.data))

    def test_delete_category(self):
        """Ensure that a category gets deleted from storage """
       
        category = 1
        user = 1
        CategoryModel(name ='somecategory',user_id=self.user).save_to_db()
        resp = self.client.delete(
            '/categories/{0}'.format(category), headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual({'message': "Category deleted"},
                                json.loads(resp.data))

    def test_find_category(self):
        """Ensure that a category can be found """
       
        category = 1
        CategoryModel(name='somecategory', user_id=self.user).save_to_db()
        resp = self.client.get('/categories/{0}'.format(category),
                            headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual({'id': 1, 'name': 'somecategory', 'recipes': []},
                                json.loads(resp.data))

    def test_category_not_found(self):
        """Test whether a category cannot be found"""
     
        category = 1
        resp = self.client.get('/categories/{0}'.format(category),
                            headers={'Authorization': self.access_token})

        self.assertEqual(resp.status_code, 404)
        self.assertDictEqual({'message': 'Category not found'},
                                json.loads(resp.data))

    def test_category_found_with_recipes(self):
        """Ensure that a category can be found with recipes"""
       
        CategoryModel(name='Beverage', user_id=self.user).save_to_db()
        RecipeModel(
            'African Tea', "Add two spoonfuls of tea leaves...", 1).save_to_db()
        category = 1
        resp = self.client.get('/categories/{0}'.format(category),
                            headers={'Authorization': self.access_token})
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual({'id': 1, 'name': 'Beverage', 'recipes': [{'name': 'African Tea', 'description': 'Add two spoonfuls of tea leaves...'}]},
                                json.loads(resp.data))

    def test_category_list(self):
        """Ensure that a category list is retrieved """

        CategoryModel(name='somecategory', user_id=self.user).save_to_db()

        resp = self.client.get(
            '/categories', headers={'Authorization': self.access_token})
        self.assertDictEqual({'categories': [{'id': 1, 'name': 'somecategory', 'recipes': []}]},
                                json.loads(resp.data))

    def test_category_list_with_recipes(self):
        """Ensure that the category list has recipes """
    
        CategoryModel(name='Beverages', user_id= self.user).save_to_db()
        RecipeModel(
            'African Tea', 'Add two spoonfuls of tea leaves...', 1).save_to_db()

        resp = self.client.get(
            '/categories', headers={'Authorization': self.access_token})
        self.assertDictEqual({'categories': [{'id': 1, 'name': 'Beverages', 'recipes': [{'name': 'African Tea', 'description': 'Add two spoonfuls of tea leaves...'}]}]},
                            json.loads(resp.data))
    # def test_pagination(self):
    #     """Ensure that the category list has recipes """
    #     with self.app() as client:
    #         with self.app_context():
    #             categories = []
    #             for i in range(0, 55):
    #                 categories.append(CategoryModel(name='category_{0:02d}'.format(i)))
    #                 CategoryModel.save_all_db(categories)

    #             rv = client.get('/categories', headers={'Authorization': self.access_token})
    #             self.assertTrue(rv.status_code == 200)
    #             self.assertTrue(rv['categories'][0] == categories[0].get_url())

    #             print(rv)
        # define 55 categories (3 pages at 25 per page)
        # categories = []
        # for i in range(0, 55):
        #     categories.append(CategoryModel(name='category_{0:02d}'.format(i)))
        #     db.session.add_all(categories)
        #     db.session.commit()

        # get first page of category list
