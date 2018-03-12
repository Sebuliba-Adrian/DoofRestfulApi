import logging

from flasgger import swag_from
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort, marshal, reqparse
from werkzeug.exceptions import BadRequest

from app.models import CategoryModel
from app.serializers import categories_serializer
from app.utilities import category_name_validator, search_categories
from db import db


class CategoryList(Resource):
    """ Defines endpoints for method calls that affect all categories
        methods: GET, POST
        url: /categories/
     """

    @jwt_required
    @swag_from('/app/docs/createcategory.yml')
    def post(self):
        """
        This method creates a recipe category
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=category_name_validator)
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()
            name = args.get("name")
            description = args["description"]
            user_id = get_jwt_identity()
            # set parsed items to an object of model class
            category = CategoryModel(
                name=name, description=description, created_by=user_id)  #

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the category'})
                response.status_code = 400
                return response
            user_id = get_jwt_identity()
            # check for similar name on category created by current user
            categories = CategoryModel.query.filter_by(
                name=name, created_by=user_id).first()  # bucks
            if categories:
                response = jsonify(
                    {'message': 'You already have a category with that name'})
                response.status_code = 400
                return response
            try:
                category.save_to_db()
                message = {'message': 'Category created Successfully'}
                response = marshal(category, categories_serializer)
                response.update(message)
                response.status_code = 201
                return response

            except Exception as e:
                logging.exception("message")
                response = jsonify(
                    {'message': 'There was an error saving the category'})
                response.status_code = 400

                return response
        except BadRequest:
            response = jsonify(
                {'message': 'You json data is deformed, correct that and '
                            'continue!'})
            response.status_code = 400

            return response

    @jwt_required
    @swag_from('/app/docs/getcategories.yml')
    def get(self):
        """
        This method gets all categories for a particular user
        """
        q = request.args.get("q", "")
        try:
            page = int(request.args.get("page", 1))
        except:
            return {"message": "Please use numbers to define the page"}, 400
        try:
            limit = int(request.args.get("limit", 4))
            if limit > 100:
                limit = 100
        except:
            return {"message": "Please use numbers to define the limit"}, 400

        user_id = get_jwt_identity()
        result = search_categories(q, user_id)
        categories = result.paginate(page, limit, error_out=False)
        if len(categories.items) == 0:
            return {
                       "message": "Your request was not found. Please try "
                                  "again"}, 404
        else:
            if categories.has_next:
                next_page = str(request.url_root) + "categories?" + \
                            "limit=" + str(limit) + "&page=" + str(page + 1)
            else:
                next_page = "None"
            if categories.has_prev:
                prev_page = request.url_root + "categories?" + \
                            "limit=" + str(limit) + "&page=" + str(page - 1)
            else:
                prev_page = "None"

            data = {"count": len(categories.items),
                    "pages": int(categories.pages),
                    "next": next_page,
                    "prev": prev_page,
                    "categories": marshal(categories.items,
                                          categories_serializer)}, 200

            if categories.items:
                return data
            else:
                response = jsonify(
                    {'message': 'There are no categories available'})
                response.status_code = 204
                return response


class Category(Resource):
    """ Defines methods that affects a single category
        methods: GET, PUT, DELETE
        url: url: api/v1/categoriess/<category_id>
    """

    @jwt_required
    @swag_from('/app/docs/getcategory.yml')
    def get(self, category_id):
        """
        This method gets specific category from the user
        """
        user_id = get_jwt_identity()
        category = CategoryModel.query.filter_by(
            id=category_id, created_by=user_id).first()
        if category:
            response = marshal(category, categories_serializer)
            return response
        else:
            response = jsonify({
                'message': 'The category your are looking '
                           'for does not exist'})
            response.status_code = 404
            return response

    @jwt_required
    @swag_from('/app/docs/editcategory.yml')
    def put(self, category_id):
        """
        This method edits the user's category
        """
        try:
            category = CategoryModel.find_by_id(category_id)
            user_id = get_jwt_identity()
            # if the category exists get new changes
            if category:
                if category.created_by == user_id:
                    parser = reqparse.RequestParser()
                    parser.add_argument(
                        'name', type=category_name_validator)
                    parser.add_argument('description', type=str, default='')
                    args = parser.parse_args()

                    name = args["name"]
                    description = args["description"]
                    data = {'name': name, 'description': description}
                    if not name or name is None:
                        data = {'description': description}

                    # update changes and commit to db
                    item_info = CategoryModel.query.filter_by(
                        id=category_id).update(
                        data)

                    try:
                        db.session.commit()
                        response = jsonify(
                            {'message': 'Category has been updated!'})
                        response.status_code = 201
                        return response

                    except Exception:
                        response = jsonify(
                            {
                                'message': 'There was an error updating the '
                                           'category'})
                        response.status_code = 500
                        return response
                else:
                    abort(401, message='You are not authorized to edit this')
            else:
                response = jsonify({
                    'message': 'The category you are '
                               'trying to edit does not '
                               'exist'})
                response.status_code = 404
                return response

        except BadRequest:

            response = jsonify(
                {
                    'message': 'Your json seems to be deformed, correct it '
                               'and try again!'})
            response.status_code = 400
            return response

    @jwt_required
    @swag_from('/app/docs/deletecategory.yml')
    def delete(self, category_id):
        """
        This method deletes a user's category by id
        """
        if category_id is None:
            response = jsonify({'message': 'Method not allowed(DELETE)'})
            response.status_code = 400
            return response
        # query whether the category exists
        category = CategoryModel.find_by_id(category_id)
        user_id = get_jwt_identity()

        # if it exists delete and commit changes to db
        if category:
            if category.created_by == user_id:  # if category belongs to
                # logged in user
                category.delete_from_db()

                response = jsonify(
                    {
                        'message': 'The category and its items have been '
                                   'successfully deleted'})
                response.status_code = 200
                return response
            else:
                abort(401, message='You are not authorized to delete this')
        else:  # else return a 204 response
            response = {
                           'message': 'The category you are trying to delete '
                                      'does not exist'}, 404

            return response
