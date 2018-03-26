import datetime
import logging

from flasgger import swag_from
from flask import jsonify
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restful import Resource, reqparse, inputs
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError

from app.models import Blacklist, UserModel
from app.utilities import username_validator, email_validator, \
    password_validator
from parsers import user_put_parser


class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password.
    """

    @swag_from('/app/docs/register.yml')
    def post(self):
        """
        Register a new user
        """

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            type=username_validator)
        parser.add_argument('password', required=True,
                            type=password_validator)
        parser.add_argument(
            'email', required=True, type=email_validator)
        # [a-zA-Z0-9.-]+@[a-z]+\.[a-z]+

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        user = UserModel(username=username, email=email)
        user.password = password
        try:
            UserModel.query.filter_by(username=username, email=email).one()

            response = jsonify(
                {'message': 'The username or email is already registered'})
            response.status_code = 400
            return response
        except:
            try:
                user.save_to_db()
                response = jsonify(
                    {'message': 'New user successfully registered!'})
                response.status_code = 201
                return response
            except IntegrityError:

                response = jsonify(
                    {'message': 'The username or email is already registered'})
                response.status_code = 400
                return response


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=username_validator,
                        required=True
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    @swag_from('/app/docs/login.yml')
    def post(self):
        """
        This method logins in a user
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
                    expires = datetime.timedelta(days=365)
                    user_token = create_access_token(
                        identity=user.id, expires_delta=expires)

                    return {'message': 'user has successfully been logged in',
                            'access_token': user_token}, 200
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
    @swag_from('/app/docs/resetpassword.yml')
    def put(self):
        """
        This method resets the user's password
        """
        data = user_put_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user is None:

            return {'message': 'User {0} does not exist in the database.'.
                format(data['username'])}, 400
        else:
            if data['username']:
                user.username = data['username']
            if data['password']:
                user.password = data['password']
        user.save_to_db()

        return {'message': 'User password has been reset successfully.'}, 201


class UserLogout(Resource):

    @jwt_required
    @swag_from('/app/docs/logout.yml')
    def delete(self):
        """
        Logout a user
        """

        jti = get_raw_jwt()['jti']
        blist = Blacklist(jti=jti)
        blist.save_to_db()
        return {"message": "Successfully logged out"}, 200
