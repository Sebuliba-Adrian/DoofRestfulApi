
from flask import g, request

from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from app import app
from app.models.user import UserModel


@app.before_request
def before_request():
    """
    Validates token.
    Is run before all requests apart from user registration and login
    """

    token = request.headers.get("access_token")
    print ('my token'+token)
      
       
           
