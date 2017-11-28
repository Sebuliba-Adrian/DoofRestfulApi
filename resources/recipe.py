from flask_restful import Resource
from models.recipe import RecipeModel


class Recipe(Resource):
    """This class represents a Recipe resource  """

    def get(self, name):
        """This method handles requests for getting a recipe by name"""
        pass

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
