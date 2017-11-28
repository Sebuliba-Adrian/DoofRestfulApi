from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.recipe import RecipeModel


class Recipe(Resource):
    """This class represents a Recipe resource  """
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="Every recipe needs a category id.")

    @jwt_required()
    def get(self, name):
        """This method handles requests for getting a recipe by name"""
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    def post(self, name):
        """This method handles requests for adding recipe to storage by name"""
        pass

    def delete(self, name):
        """This method handles requests for deleting recipe by name"""
        pass

    def put(self, name):
        """This method handles requests for updating a recipe """
        pass


class RecipeList(Resource):
    """This class represents alist of recipe resources"""

    def get(self):
        """This method handles requests for retrieving a list of recipes"""
        pass
