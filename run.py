import sys

from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app import app
from app.models import Blacklist
from app.resources.category import Category, CategoryList
from app.resources.recipe import Recipe, RecipeList
from app.resources.user import (PasswordReset, UserLogin, UserLogout,
                                UserRegister)
from db import db

# instantiate flask_restful Api class
api = Api(app)
# access_token = create_access_token(identity=username)
jwt = JWTManager(app)


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# Token attempts to access an endpoint
@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({'status': 401,

                    'message': 'You must be logged in to access this!'
                    }), 401


@jwt.revoked_token_loader
def my_revoked_token_callback():
    return jsonify({'message': 'You must be logged in to access this!'})


@jwt.invalid_token_loader
def my_invalid_token_callback(error='Invalid Token'):
    return jsonify({'message': 'Invalid Token'}), 422


@jwt.unauthorized_loader
def my_unauthorized_loader(error='error'):
    return jsonify({'message': 'No authorization token provided'}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

    isthere = Blacklist.get_or_create(jti)
    return isthere


@app.errorhandler(404)
def url_not_found(error):
    return jsonify(
        {'message': 'Your url seems to be deformed, please try again!'}), 404



# # Register Recipe endpoint with flask_restful api
api.add_resource(
    Recipe, '/categories/<int:category_id>/recipes/<int:recipe_id>')
# # Register Category endpoint with flask_restful api
api.add_resource(Category, '/categories/<int:category_id>')
# # Register recipe list end point with the flask_restful api
api.add_resource(RecipeList, '/categories/<int:category_id>/recipes')
# # Register category list endpoint with flask_resful api
api.add_resource(CategoryList, '/categories')
# Register UserRegister endpoint with flask_restful api
api.add_resource(PasswordReset, '/auth/reset')
api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogout, '/auth/logout')
db.init_app(app)


@app.before_first_request
def create_tables():
    """Creates a database on every start if there is none"""
    db.create_all()


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
