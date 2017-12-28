from flask import Flask
from flasgger import Swagger

from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_restful import Api
from .resources.category import Category, CategoryList
from .resources.recipe import Recipe, RecipeList
from .resources.user import PasswordReset, UserLogin, UserRegister


app = Flask(__name__)
app.config.from_object('config.config.DevelopmentConfig')


swag = Swagger(app=app,
               template={
                   "info": {
                       "title": "Doof! Recipes Api",
                       "description": "An API for the yummies recipe called Doof!",
                       "contact": {
                           "responsibleOrganization": "Andela",
                           "responsibleDeveloper": "Adrian Sebuliba",
                           "email": "adrian.sebuliba@andela.com",
                           "url": "www.andela.com",
                       },
                       "termsOfService": "http://andela.com/terms",
                       "version": "1.0"
                   },
                   "securityDefinitions": {
                       "TokenHeader": {
                           "type": "apiKey",
                           "name": "Authorization",
                           "in": "header"
                       }
                   },
                   "Consumes": "Application/json"
               })
