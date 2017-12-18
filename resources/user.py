from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from models.user import UserModel
from parsers import user_put_parser


class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        """
        Register a new user
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            type: string
        responses:
          200:
            description: A user is successfully logged in
            schema:
              id: user
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        """
        Log in a user
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            type: string
            description: Username and password of the user


        responses:
          200:
            description: User is successfully logged in and token generated
            schema:
              id: user
              properties:
                username:
                  type: string
                  default: testusername
                password:
                  type: string
                  default: testpassword
            """
        data = UserLogin.parser.parse_args()

        try:

            user = UserModel.find_by_username(data['username'])
            if not request.is_json:
                return {"message": "Missing JSON in request"}, 400

            username = data['username']
            password = data['password']
            if not username:
                return {"message": "Missing username parameter"}, 400
            if not password:
                return {"message": "Missing password parameter"}, 400
            if (user and user.username and user.password):
                # Identity can be any data that is json serializable
                access_token = create_access_token(identity=username)
                return {'access_token': str(access_token)}, 201
            else:
                return {"message": "Bad username or password"}, 401

        except Exception as e:
            response = {'message': str(e)}
            return response, 500


class PasswordReset(Resource):

    @jwt_required
    def put(self):
        """
        Reset a user's password
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            required: true
            type: string
        responses:
          200:
            description: A user is successfully updated
            schema:
              id: user
        """
        # data = user_put_parser.parse_args(strict=True)
        # username = data['username']
        # user = UserModel.find_by_username(username)
        # if UserModel.find_by_username(username):
        #     return {'message': "A user with name '{0}' already exists.".format(username)}, 400

        # else:
        #     if data['username']:
        #         user.username = data['username']
        #     if data['password']:
        #         user.password = data['password']

        # user.save_to_db()

        # return {'message': 'User password has been reset successfully.'}, 201

        data = user_put_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user is None:
            return {'message': 'User {0} does not exist in the database.'.format(data['username'])}, 400
        else:
            if data['username']:
                user.username = data['username']
            if data['password']:
                user.password = data['password']
        user.save_to_db()

        return {'message': 'User password has been reset successfully.'}, 201


class LogoutUser(Resource):

    pass
