from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.recipe import RecipeModel


class Recipe(Resource):
    """This class represents a Recipe resource  """
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
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
    @jwt_required()
    def post(self, name):
        """This method handles requests for adding recipe to storage by name"""
        if RecipeModel.find_by_name(name):
            return {'message': "A recipe with name '{}' already exists.".format(name)}, 400

        data = Recipe.parser.parse_args()

        recipe = RecipeModel(name, **data)

        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe."}, 500

        return recipe.json(), 201
    @jwt_required()
    def delete(self, name):
        """This method handles requests for deleting recipe by name"""
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()

        return {'message': 'Recipe deleted'}
    @jwt_required()
    def put(self, name):
        """This method handles requests for updating a recipe """
        data = Recipe.parser.parse_args()

        recipe = RecipeModel.find_by_name(name)

        if recipe is None:
            recipe = RecipeModel(name, **data)
        else:
            recipe.description = data['description']

        recipe.save_to_db()

        return recipe.json()


class RecipeList(Resource):
    """This class represents alist of recipe resources"""
    @jwt_required()
    def get(self):
        """This method handles requests for retrieving a list of recipes"""
        return {'recipes': [recipe.json() for recipe in RecipeModel.query.all()]}
