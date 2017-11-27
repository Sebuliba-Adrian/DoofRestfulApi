from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError
from security import authenticate, identity
from db import db

from resources.user import UserRegister

import logging


# Instantiate the app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# instantiate flask_restful Api class
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth

# Add logger for sanity check
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logging.warning(app.config['SQLALCHEMY_DATABASE_URI'])

# Register UserRegister resource with flask_restful api
api.add_resource(UserRegister, '/register')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":

    app.run()
