#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort, reqparse

from app.models import CategoryModel
from app.models import RecipeModel
from parsers import recipe_post_parser, recipe_put_parser
from validator import is_valid


class Recipe(Resource):
    """This class represents a Recipe resource  """

    @jwt_required
    def get(self, category_id, recipe_id):
        """
        Get a recipe by name
        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: false
            description: The id of the recipe to retrieve
            type: integer

          - in: path
            name: recipe_id
            required: false
            description: The id of the recipe to retrieve
            type: integer  

        security: 
          - TokenHeader: []
        responses:
          200:
            description: The recipe has been successfully retrieved
            schema:
              id: recipe
              properties:
                name:
                  type: string
                  default: Tea
                description:
                    type: string
                    default: Tea and specifically black

        """
        current_user = g.user.id
        print("The id is {0}".format(current_user))
        recipe = RecipeModel.find_by_category(
        category_id).find_by_id(recipe_id)
         
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    @jwt_required
    def delete(self, category_id, recipe_id):
        """
        This method handles requests for deleting recipe by name
        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of the recipe to delete
            type: integer

          - in: path
            name: recipe_id
            required: true
            description: The id of the recipe to delete
            type: integer  

        security:
          TokenHeader: []    

        responses:
          200:
            description: Successfully deleted
          204:
            description: No recipes

        """
        recipe = RecipeModel.find_by_category(
            category_id).find_by_id(recipe_id)
        if recipe:
            recipe.delete_from_db()

        return {'message': 'Recipe deleted'}

    @jwt_required
    def put(self, category_id, recipe_id):
        """
        This method handles requests for updating a recipe
        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: true
            description: The category id of the recipe to update goes here
            type: integer

          - in: path
            name: recipe_id
            required: true
            description: The id of the recipe to update goes here
            type: integer  

          - in: body
            name: body
            required: true
            description: The details of the new recipe goes here
            type: string  


        security:
          - TokenHeader: []    

        responses:
          200:
            description: Successfuly updated
          204:
            description: No content
            schema:
              id: recipe

        """

        # data = recipe_put_parser.parse_args(strict=True)
        # name = data['name']
        # description = data['description']
        # category_id = data['category_id']
        # recipe = RecipeModel.find_by_id(id)
        # if RecipeModel.find_by_name(name):
        #     return {'message': "A recipe with name '{0}' already exists.".format(name)}, 400
        # if recipe is None:
        #     recipe = RecipeModel(**data)
        # else:
        #     if name:
        #         recipe.name = name
        #     if description:
        #         recipe.description = description
        #     if category_id:
        #         category = CategoryModel.find_by_id(category_id)
        #         if category is None:
        #             return {'message': "A Category with id '{0}' does not exist".format(category_id)}, 400

        # recipe.save_to_db()

        # return recipe.json()

        data = recipe_put_parser.parse_args()
        data['category_id'] = category_id

        recipe = RecipeModel.find_by_id(recipe_id)

        if recipe is None:
            recipe = RecipeModel(**data)
        else:
            if data['name']:
                recipe.name = data['name']
            if data['description']:
                recipe.description = data['description']
            if category_id:

                category = CategoryModel.find_by_id(category_id)

                if category is None:
                    return{'message': 'Category with id {0} doesnot exist'.format(category_id)}, 400
                recipe.category = category
                # return{'message': 'Category with id {0} doesnot exist'.format(category_id)},500


        recipe.save_to_db()

        return recipe.json()


class RecipeList(Resource):
    """This class represents a list of recipe resources"""

    @jwt_required
    def post(self, category_id):
        """
        This method handles requests for adding recipe to storage by name
        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: true
            description: Recipe category id goes here
            type: integer

          - in: body
            name: body
            required: true
            description: Recipe details goes here
            type: string


        security:
          TokenHeader: []  

        responses:
          201:
            description:  The recipe has been created successfully
            schema:
              id: recipe

        """

        data = recipe_post_parser.parse_args()
        data['category_id'] = category_id
        name = data['name']

        if RecipeModel.find_by_name(name):
            return {'message': "A recipe with name '{0}' already exists.".format(name)}, 400

        recipe = RecipeModel(**data)

        try:
            category = CategoryModel.find_by_id(category_id)
            recipe.category = category
            recipe.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe."}, 500

        return recipe.json(), 201

    @jwt_required
    #@paginate('recipes')
    def get(self, category_id):
        """
        This method handles requests for retrieving a list of recipes
        ---
        tags:
         - Recipes
        parameters:

          - in: path
            name: category_id
            description: The category id goes here
            required: true
            type: string


          - in: path
            name: per_page
            description: The number of recipes to be displayed in a single page
            required: false
            type: string

          - in: path
            name: page
            description: The page to be displayed
            required: false
            type: string




        security:
          - TokenHeader: []
        responses:
          200:
            description: A list of recipes
          404:
            description: Not found
        """
        category = CategoryModel.find_by_id(category_id)
        resultx = RecipeModel.query
        # return result
        # print {'recipes': [recipe.json() for recipe in category.recipes]}
        return {'recipes': [recipe.json() for recipe in category.recipes]}
