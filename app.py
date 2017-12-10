from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from resources.category import Category, CategoryList
from resources.recipe import Recipe, RecipeList
from resources.user import UserLogin, UserRegister

# Instantiate the app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# instantiate flask_restful Api class
api = Api(app)
#access_token = create_access_token(identity=username)
jwt = JWTManager(app)

# Add logger for sanity check
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logging.warning(app.config['SQLALCHEMY_DATABASE_URI'])

# Register Recipe endpoint with flask_restful api
api.add_resource(Recipe, '/recipe/<string:name>')
# Register Category endpoint with flask_restful api
api.add_resource(Category, '/category/<string:name>')
# Register recipe list end point with the flask_restful api
api.add_resource(RecipeList, '/recipes')
# Register category list endpoint with flask_resful api
api.add_resource(CategoryList, '/categories')
# Register UserRegister endpoint with flask_restful api
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin,'/login')


db.init_app(app)


@app.before_first_request
def create_tables():
    """Creates a database on every start if there is none"""
    db.create_all()


if __name__ == "__main__":

    app.run()
