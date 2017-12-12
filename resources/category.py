from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.category import CategoryModel
from utilities import paginate


class Category(Resource):
    """This is a Category resource class """
    @jwt_required
    def get(self, name):
        """
        This request method gets category resource by name from the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: category name
            required: true
            description: A name of the recipe to retrieve
            type: string


        security: 
          - TokenHeader: []
        responses:
          200:
            description: The recipe category has been successfully retrieved


        """
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    @jwt_required
    def post(self, name):
        """
        This post request method adds a category resource of a particular name to the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: category name
            required: true
            type: string
            description: Category name

          - in: body
            name: category details
            required: true
            type: string
            description: Category details

        security: 
          - TokenHeader: []  


        responses:
          200:
            description: Recipe category is successfully created
            schema:
              id: category
              properties:
                name:
                  type: string
                  default: Tea

        """
        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists.".format(name)}, 400

        category = CategoryModel(name)
        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 201

    @jwt_required
    def delete(self, name):
        """
        This method deletes a particular category resource from the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: category name
            required: true
            description: A name of the recipe to delete
            type: string


        security: 
          - TokenHeader: []
        responses:
          200:
            description: The recipe category has been successfully deleted



        """
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()

        return {'message': 'Category deleted'}


class CategoryList(Resource):
    """
        This is a category list class, it handles requests that involve retrieving lists of  resources


    """
    @jwt_required
    #@paginate('categories')
    def get(self):
        """
        This method gets a list of resources from the storage
        ---
        tags:
         - Recipe Categories
        parameters:
          - in: path
            name: per_page
            description: The number of recipes to be displayed in a single page
            required: true
            type: string
          - in: path
            name: page
            description: The page to be displayed
            required: true
        security:
          - TokenHeader: []
        responses:
          200:
            description: A list of recipes
          404:
            description: Not found
        """
        result = CategoryModel.query
        # return result
        return {'categories': [category.json() for category in CategoryModel.query.all()]}
