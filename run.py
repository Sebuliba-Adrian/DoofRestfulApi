import sys

from db import  db
from app import app
from app.models import UserModel
from app.resources.category import Category, CategoryList
from app.resources.recipe import Recipe, RecipeList
from app.resources.user import PasswordReset, UserLogin, UserRegister
from flasgger import Swagger
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

# instantiate flask_restful Api class
api = Api(app)
#access_token = create_access_token(identity=username)
jwt = JWTManager(app)

# # Register Recipe endpoint with flask_restful api
# api.add_resource(
#     Recipe, '/categories/<int:category_id>/recipes/<int:recipe_id>')
# # Register Category endpoint with flask_restful api
# api.add_resource(Category, '/categories/<int:category_id>')
# # Register recipe list end point with the flask_restful api
# api.add_resource(RecipeList, '/categories/<int:category_id>/recipes')
# # Register category list endpoint with flask_resful api
# api.add_resource(CategoryList, '/categories')
# Register UserRegister endpoint with flask_restful api
api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
# api.add_resource(PasswordReset, '/auth/reset')
db.init_app(app)


# @app.before_request
# def before_request():
#     """
#     Validates token.
#     Is run before all requests apart from user registration, login and index.
#     """
#     if request.endpoint not in ["userlogin", "userregister", "index"]:
#         id = get_jwt_identity()
#         print ("My id  " + str(id))
#         if id:
#             user = UserModel.find_by_id(id)
#             print (user.username)
#             if user:

#                 app.app_context().push()
#                 g.user = user

#                 print('its is'+str(g.user.id))
#             else:
#                 print("Error: The token you have entered is "
#                                     "invalid.")
#         # print ("Error: Please enter a token." )


# @app.before_first_request
# def create_tables():
#     """Creates a database on every start if there is none"""
#     db.create_all()


if __name__ == "__main__":

    if "createdb" in sys.argv:
        with app.app_context():
            db.create_all()
        print("Database created!")

    elif "seeddb" in sys.argv:
        with app.app_context():
            c1 = None
            db.session.add(c1)
            c2 = None
            db.session.add(c2)
            db.session.commit()
        print("Database seeded!")

    elif "deletedb" in sys.argv:
        with app.app_context():
            db.drop_all()
        print("Database deleted!")

    else:
        app.run(debug=True)
