from flask import abort
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with, reqparse

from db import db
from models.category import CategoryModel
from parsers import category_put_parser
from utilities import paginate


class Category(Resource):
    """This is a Category resource class """

    @jwt_required
    def get(self, id):
        """
        This request method gets category resource by name from the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: id
            required: true
            description: A name of the recipe to retrieve
            type: integer


        security: 
          - TokenHeader: []
        responses:
          200:
            description: The recipe category has been successfully retrieved


        """

        category = CategoryModel.find_by_id(id)
        print category
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    @jwt_required
    def put(self, id=None):
        """"This method updates a particular category from the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: id
            required: true
            description: An id of the recipe to update
            type: integer

          - in: body
            name: Details of the new recipe
            required: true
            description: An id of the recipe to update
            type: string  

        security:
          - TokenHeader: []

        responses:
          200:
            description: The recipe category has been sucessfully changed
            schema:
              id: categories
              properties:
                name:
                  Type: string
                  default: Tea
        """

        args = category_put_parser.parse_args()
        print id

        category = CategoryModel.find_by_id(id)

        if category and args['name']:
            category.name = args['name']
        category.save_to_db()
        return category.json()

    @jwt_required
    def delete(self, id):
        """
        This method deletes a particular category resource from the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: path
            name: id
            required: true
            description: A name of the recipe to delete
            type: integer


        security: 
          - TokenHeader: []
        responses:
          200:
            description: The recipe category has been successfully deleted
        """

        # if not id:
        #       abort(400)
        # category= CategoryModel.query.filter_by(id=id).first()

        # db.session.delete(category)
        # db.session.commit()

        # return {'message': "Category deleted"}

        category = CategoryModel.find_by_id(id)
        if category:
            category.delete_from_db()
        return {'message': "Category deleted"}

        # category = CategoryModel.query.filter_by(id=id).first()

        # if category:
        #       db.session.delete(category)
        #       db.session.commit()
        # return {"message": "Sucessfully deleted"}


class CategoryList(Resource):
    """
        This is a category list class, it handles requests that involve retrieving lists of  resources
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    @jwt_required
    def post(self):
        """
        This post request method adds a category resource of a particular name to the storage
        ---
        tags:
          - Recipe Categories
        parameters:
          - in: body
            name: category name
            required: true
            type: string
            description: Category name

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

        args = CategoryList.parser.parse_args(strict=True)
        name = args['name']

        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{0}' already exists.".format(name)}, 400

        category = CategoryModel(name)

        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 201

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
