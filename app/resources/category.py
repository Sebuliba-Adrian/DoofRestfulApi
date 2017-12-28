from flask import g, jsonify, request
from flask_restful import marshal, reqparse, Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from app.models import CategoryModel, RecipeModel
from app.serializers import categories_serializer
from app.utilities import search_categories


class CategoryList(Resource):
    """ Defines endpoints for method calls that affect all categories
        methods: GET, POST
        url: /categories/
     """

    @jwt_required
    def post(self, category_id=None):
        """ Method to create new categories """

        if category_id:
            abort(400, 'The requested url is not valid')

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='A name is required')
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
            message = {'message': 'Category updated Successfully'}
            response = marshal(category, categories_serializer)
            response.update(message)
            response.status_code = 201
            return response

        except Exception:
            response = jsonify(
                {'message': 'There was an error saving the category'})
            response.status_code = 400

            return response

    @jwt_required
    def get(self):
        """ Method that gets all categories """
        args = request.args.to_dict()

        q = args.get('q')
        try:
            page = int(args.get('page', 1))  # query start as an integer
            # 100 items == 20 per page for 5 pages
            limit = int(args.get('limit', 20))
            if q:
                categories = search_categories(q)
                if not categories:
                    abort(204, message='No data found matching the query')
                else:
                    response = marshal(categories, categories_serializer)
                    return response

            try:
                # query a paginate object
                user_id = get_jwt_identity()
                categories = CategoryModel.query.filter_by(created_by=user_id).paginate(
                    page, limit, False)

                all_pages = categories.pages  # get total page count
                next_pg = categories.has_next  # check for next page
                previous_pg = categories.has_prev  # check for previous page

                # if the query allows a max over the limit, generate a url
                # for the next page
                if next_pg:
                    next_page = str(request.url_root) + '/categories?' + \
                        'limit=' + str(limit) + '&page=' + str(page + 1)
                else:
                    next_page = 'None'

                # set a url for the previous page
                if previous_pg:
                    previous_page = str(request.url_root) + '/categories?' + \
                        'limit=' + str(limit) + '&page=' + str(page - 1)
                else:
                    previous_page = 'None'

                categories = categories.items

                data = {'categories': marshal(categories, categories_serializer),
                        'total pages': all_pages,
                        'next page': next_page,
                        'previous page': previous_page}
                # if categories are not None, return data as output
                if categories:
                    return data
                else:
                    response = jsonify(
                        {'message': 'There are no categories available'})
                    response.status_code = 204
                    return response
            except AttributeError:
                response = jsonify({'message': 'Authenticate to proceed'})
                response.status_code = 401
                return response

        except ValueError:
            response = jsonify({'message': ' provide an integer'})
            response.status_code = 400
            return response


class Category(Resource):
    """ Defines methods that affects a single category
        methods: GET, PUT, DELETE
        url: url: api/v1/categoriess/<category_id>
    """
    @jwt_required
    def get(self, category_id):
        """
        Method that gets a single category
        """
        user_id = get_jwt_identity()
        category = CategoryModel.query.filter_by(
            id=category_id, created_by=user_id).first()
        if category:
            response = marshal(category, categories_serializer)
            return response
        else:
            response = jsonify({'message': 'the category does not exist'})
            response.status_code = 204
            return response

    @jwt_required
    def put(self, category_id):
        """
        Method that edits an existing category
        """
        category = CategoryModel.find_by_id(category_id)
        user_id = get_jwt_identity()
        # if the category exists get new changes
        if category:
            if category.created_by == user_id:
                parser = reqparse.RequestParser()
                parser.add_argument(
                    'name', type=str, help='A name is required')
                parser.add_argument('description', type=str, default='')
                args = parser.parse_args()

                name = args["name"]
                description = args["description"]
                data = {'name': name, 'description': description}
                if not name or name == None:
                    data = {'description': description}

                # update changes and commit to db
                item_info = CategoryModel.query.filter_by(id=category_id).update(
                    data)

                try:
                    db.session.commit()
                    response = jsonify(
                        {'message': 'Category has been updated!'})
                    response.status_code = 201
                    return response

                except Exception:
                    response = jsonify(
                        {'message': 'There was an error updating the category'})
                    response.status_code = 500
                    return response
            else:
                abort(401, message='You are not authorized to edit this')
        else:
            response = jsonify({'message': 'the category does not exist'})
            response.status_code = 204
            return response

    @jwt_required
    def delete(self, category_id):
        """
        Method that deletes an existing category
        """
        if id == None:
            response = jsonify({'message': 'Method not allowed(DELETE)'})
            response.status_code = 400
            return response
        # query whether the category exists
        category = CategoryModel.find_by_id(category_id)
        user_id = get_jwt_identity()

        # if it exists delete and commit changes to db
        if category:
            if category.created_by == user_id:  # if category belongs to logged in user
                category.delete_from_db()

                response = jsonify(
                    {'message': 'The category and its items have been successfully deleted'})
                response.status_code = 200
                return response
            else:
                abort(401, message='You are not authorized to delete this')
        else:  # else return a 204 response
            response = jsonify({'message': 'the category does not exist'})
            response.status_code = 204
            return response
