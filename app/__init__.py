from flask import Flask
from flasgger import Swagger

from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_restful import Api

from .resources.user import PasswordReset, UserLogin, UserRegister, UserLogout


app = Flask(__name__)
app.config.from_object('config.config.DevelopmentConfig')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']


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
