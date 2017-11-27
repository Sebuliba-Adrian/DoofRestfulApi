from flask_restful import Resource
from models.category import CategoryModel


class Category(Resource):
    """This is a Category resource class """

    def get(self, name):
        """This request method gets category resource by name from the storage  """
        pass

    def post(self, name):
        """This post request method adds a category resource of a particular name to a the storage"""

        pass

    def delete(self, name):
        """This method deletes a particular category resource from the storage"""
        pass


class CategoryList(Resource):
    """This is a category list class, it handles requests that involve retrieving lists of  resources"""
    def get(self):
        """This method gets a list of resources from the storage"""
        pass
