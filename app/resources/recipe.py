from flask import g, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort, marshal, reqparse

from app.models import CategoryModel, RecipeModel
from app.serializers import recipes_serializer
from app.utilities import search_recipes
from db import db


class Recipe(Resource):
    """ Defines endpoints for recipes manipulation
        methods: GET, POST, PUT, DELETE
        url: /api/v1/categories/<category_id>/recipes/
     """

    @jwt_required
    def put(self, category_id, recipe_id=None):
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
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        try:
            category = CategoryModel.find_by_id(category_id)
            recipe = RecipeModel.query.filter_by(id=recipe_id).one()
        except:
            response = jsonify(
                {'message': 'The category or recipe does not exist'})
            response.status_code = 204
            return response
        user_id = get_jwt_identity()
        if recipe.created_by == user_id:
            if category and recipe:
                parser = reqparse.RequestParser()
                parser.add_argument(
                    'name', type=str, help='A name is required')
                parser.add_argument('description', type=str, default='')

                args = parser.parse_args()

                name = args["name"]
                description = args["description"]

                data = {'name': name, 'description': description}
                if not name or name == None:
                    data = {'description': description}

                recipe_info = RecipeModel.query.filter_by(
                    id=recipe_id).update(data)

                try:
                    db.session.commit()
                    response = jsonify({'message': 'Recipe updated'})
                    response.status_code = 200
                    return response

                except Exception:
                    response = jsonify(
                        {'message': 'There was an error updating the recipe'})
                    response.status_code = 500
                    return response
            else:
                response = jsonify(
                    {'message': 'The category or recipe does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify(
                {'message': 'You are not authorized to edit this'})
            response.status_code = 401
            return response

    @jwt_required
    def get(self, category_id, recipe_id=None):
        """
        Get a recipe by id
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
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        category = CategoryModel.find_by_id(category_id)
        recipe = RecipeModel.query.filter_by(
            id=recipe_id, category_id=category_id).first()
        user_id = get_jwt_identity()
        if category:
            if recipe:
                if recipe.created_by == user_id:
                    return marshal(recipe, recipes_serializer)
                else:
                    response = jsonify(
                        {'message': 'You are not authorized to view this'})
                    response.status_code = 401
                    return response
            else:
                response = jsonify({'message': 'The recipe does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify({'message': 'the category does not exist'})
            response.status_code = 204
            return response

    @jwt_required
    def delete(self, category_id, recipe_id=None):
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
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed (DELETE)'})
            response.status_code = 400
            return response

        recipe = RecipeModel.find_by_id(recipe_id)
        user_id = get_jwt_identity()

        if recipe:
            if recipe.created_by == user_id:
                recipe.delete_from_db()
                response = jsonify(
                    {'message': 'The recipe has been successfully deleted'})
                response.status_code = 200
                return response
            else:
                response = jsonify(
                    {'message': 'You are not authorized to del this'})
                response.status_code = 401
                return response
        else:
            response = jsonify({'message': 'The item does not exist'})
            response.status_code = 204
            return response


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

        # if recipe_id:
        #     response = jsonify({'message': 'Method not allowed(POST)'})
        #     response.status_code = 400
        #     return response

        category = CategoryModel.find_by_id(category_id)
        user_id = get_jwt_identity()
        if category:
            if category.created_by != user_id:
                response = jsonify(
                    {'message': 'You are not authorized to use the category'})
                response.status_code = 401
                return response
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the recipe'})
                response.status_code = 400
                return response

            recipe = RecipeModel(
                name=name, description=description,
                category_id=category_id, created_by=user_id)

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the recipe'})
                response.status_code = 400
                return response

            try:
                RecipeModel.query.filter_by(name=name).one()
                response = jsonify(
                    {'message': 'That name is already taken, try again'})
                response.status_code = 400
                return response

            except:
                try:
                    recipe.save_to_db()
                    message = {
                        'message': 'Recipe added Successfully!'}
                    response = marshal(recipe, recipes_serializer)
                    response.update(message)
                    return response, 201

                except:
                    response = jsonify(
                        {'message': 'There was an error saving the recipe'})
                    response.status_code = 400
                    return response
        else:
            response = jsonify(
                {'message': 'A category with the ID provided does not exist!'})
            response.status_code = 204
            return response

    @jwt_required
    #@paginate('recipes')
    def get(self, category_id=None):
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


          - in: query
            name: q
            description: The search term(s)
            required: false
            type: string

          - in: query
            name: page
            description: The page to be displayed
            required: false
            type: string   


          - in: query
            name: limit
            description: The number of recipes to be displayed in a single page
            required: false
            type: string









        security:
          - TokenHeader: []
        responses:
          200:
            description: A list of recipes in a category
          404:
            description: Not found
        """
        args = request.args.to_dict()

        q = args.get('q')
        try:
            page = int(args.get('page', 1))  # query start as an integer
            # 100 items == 20 per page for 5 pages
            limit = int(args.get('limit', 4))
            if q:
                recipes = search_recipes(q)
                if not recipes:
                    abort(204, message='No data found matching the query')
                else:
                    response = marshal(recipes, recipes_serializer)
                    return response

            try:
                # query a paginate object
                user_id = get_jwt_identity()
                recipes = RecipeModel.query.filter_by(category_id=category_id, created_by=user_id).paginate(
                    page, limit, False)

                all_pages = recipes.pages  # get total page count
                next_pg = recipes.has_next  # check for next page
                previous_pg = recipes.has_prev  # check for previous page

                # if the query allows a max over the limit, generate a url
                # for the next page
                if next_pg:
                    next_page = str(request.url_root) + '/recipes?' + \
                        'limit=' + str(limit) + '&page=' + str(page + 1)
                else:
                    next_page = 'None'

                # set a url for the previous page
                if previous_pg:
                    previous_page = str(request.url_root) + '/recipes?' + \
                        'limit=' + str(limit) + '&page=' + str(page - 1)
                else:
                    previous_page = 'None'

                recipes = recipes.items

                data = {'recipes': marshal(recipes, recipes_serializer),
                        'total pages': all_pages,
                        'next page': next_page,
                        'previous page': previous_page}
                # if recipes are not None, return data as output
                if recipes:
                    return data
                else:
                    response = jsonify(
                        {'message': 'There are no recipes available'})
                    response.status_code = 204
                    return response
            except AttributeError:
                response = jsonify({'message': 'Authenticate to proceed'})
                response.status_code = 401
                return response

        except ValueError:
            response = jsonify({'message': ' provide an integer'})
            response.status_code = 400
            return response

        # category = CategoryModel.find_by_id(category_id)
        # resultx = RecipeModel.query
        # return result
        # print {'recipes': [recipe.json() for recipe in category.recipes]}
        # return {'recipes': [recipe.json() for recipe in category.recipes]}
