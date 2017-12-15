from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.recipe import RecipeModel
from utilities import paginate


class Recipe(Resource):
    """This class represents a Recipe resource  """
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="Every recipe needs a category id.")

    @jwt_required
    def get(self, id):
        """
        Get a recipe by name
        ---
        tags:
          - recipes
        parameters:
          - in: path
            name: id
            required: true
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
        recipe = RecipeModel.find_by_id(id)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    @jwt_required
    def delete(self, id):
        """
        This method handles requests for deleting recipe by name
        ---
        tags:
          - recipes
        parameters:
          - in: path
            name: id
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
        recipe = RecipeModel.find_by_id(id)
        if recipe:
            recipe.delete_from_db()

        return {'message': 'Recipe deleted'}

    @jwt_required
    def put(self, id):
        """
        This method handles requests for updating a recipe
        ---
        tags:
          - recipes
        parameters:
          - in: path
            name: id
            required: true
            description: The id of the recipe to update
            type: string

          - in: body
            name: body
            required: true
            description: The details of the new recipe
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
        data = Recipe.parser.parse_args()

        recipe = RecipeModel.find_by_id(id)

        if recipe is None:
            recipe = RecipeModel(**data)
        else:
            recipe.description = data['description']

        recipe.save_to_db()

        return recipe.json()


class RecipeList(Resource):
    """This class represents a list of recipe resources"""
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="Every recipe needs a category id.")

    @jwt_required
    def post(self):
        """
        This method handles requests for adding recipe to storage by name
        ---
        tags:
          - recipes
        parameters:
          - in: body
            name: name
            required: true
            description: Recipe details go here
            type: string

      
        security:
          TokenHeader: []  

        responses:
          201:
            description:  The recipe has been created successfully
            schema:
              id: recipe


        """
        data = RecipeList.parser.parse_args()
        name = data['name']

        if RecipeModel.find_by_name(name):
            return {'message': "A recipe with name '{0}' already exists.".format(name)}, 400

        recipe = RecipeModel(**data)

        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe."}, 500

        return recipe.json(), 201

    @jwt_required
    #@paginate('recipes')
    def get(self):
        """
        This method handles requests for retrieving a list of recipes
        ---
        tags:
         - recipes
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
        result = RecipeModel.query
        # return result
        return {'recipes': [recipe.json() for recipe in RecipeModel.query.all()]}
