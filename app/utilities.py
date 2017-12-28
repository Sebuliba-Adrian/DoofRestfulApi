from flask import g
from models import UserModel
from flask_jwt_extended import get_jwt_identity
from app import app


@app.before_request
def before_request():

    current_user = get_jwt_identity()
    if current_user:
        g.user = UserModel.find_by_id(current_user)
        print(g.user.username)
