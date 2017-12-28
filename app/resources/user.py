from app.models import UserModel
from flask import jsonify, make_response, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource, reqparse
from parsers import user_put_parser


class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password.
    """
    
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
      
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            type=str, help='Username is required')
        parser.add_argument('password', required=True, default='')
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel(username=username)
        user.password =password
        try:
            UserModel.query.filter_by(username=username).one()

            response = jsonify(
                {'message': 'The username is already registered'})
            response.status_code = 400
            return response
        except:
            try:
                user.save_to_db()
                response = jsonify(
                    {'message': 'New user successfully registered!'})
                response.status_code = 201
                return response
            except Exception:
                response = jsonify(
                    {'message': 'There was a problem while saving the data'})
                response.status_code = 500
                return response                    



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
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            type=str, help='Username is required')
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        
        if username and password:
            user = UserModel.find_by_username(username)
            if user:
                if user.verify_password(password):
                    user_token = create_access_token(identity=user.id)
                    return {'access_token': user_token}, 200
                else:
                    message = {'message': 'Invalid password'}
                    return message
            else:
                message = {'message': 'The user does not exist'}
                return message
        else:
            message = {'message': 'one or more fields is not complete'}
            return message, 400


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
