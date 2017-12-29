from db import db
from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, abort, marshal, reqparse
from app.models import CategoryModel, RecipeModel
from app.serializers import recipes_serializer


class Recipe(Resource):
    """ Defines endpoints for recipes manipulation
        methods: GET, POST, PUT, DELETE
        url: /api/v1/categories/<category_id>/recipes/
     """
    @jwt_required
    def post(self, category_id, recipe_id=None):
        """
        request that handles recipes creation
        """
        if recipe_id:
            response = jsonify({'message': 'Method not allowed(POST)'})
            response.status_code = 400
            return response

        category = CategoryModel.find_by_id(category_id)
        user_id = get_jwt_identity()
        if category:
            if category.created_by != user_id:
                response = jsonify(
                    {'message': 'You are not authorized to use the category'})
                response.status_code = 401
                return response
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='A name is required')
            parser.add_argument('description', type=str, default='')
            args = parser.parse_args()

            name = args["name"]
            description = args["description"]

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the recipe'})
                response.status_code = 400
                return response

            recipe = RecipeModel(
                name=name, description=description,
                category_id=category_id, created_by=user_id)

            if not name:
                response = jsonify(
                    {'message': 'Please provide a name for the recipe'})
                response.status_code = 400
                return response

            try:
                RecipeModel.query.filter_by(name=name).one()
                response = jsonify(
                    {'message': 'That name is already taken, try again'})
                response.status_code = 400
                return response

            except:
                try:
                    recipe.save_to_db()
                    message = {
                        'message': 'Recipe added Successfully!'}
                    response = marshal(recipe, recipes_serializer)
                    response.update(message)
                    return response, 201

                except:
                    response = jsonify(
                        {'message': 'There was an error saving the recipe'})
                    response.status_code = 400
                    return response
        else:
            response = jsonify(
                {'message': 'A category with the ID provided does not exist!'})
            response.status_code = 204
            return response

    @jwt_required
    def put(self, category_id, recipe_id=None):
        """
        request that updates an item
        """
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        try:
            category = CategoryModel.find_by_id(category_id)
            recipe = RecipeModel.query.filter_by(id=recipe_id).one()
        except:
            response = jsonify(
                {'message': 'The category or recipe does not exist'})
            response.status_code = 204
            return response
        user_id = get_jwt_identity()
        if recipe.created_by == user_id:
            if category and recipe:
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

                recipe_info = RecipeModel.query.filter_by(
                    id=recipe_id).update(data)

                try:
                    db.session.commit()
                    response = jsonify({'message': 'Recipe updated'})
                    response.status_code = 200
                    return response

                except Exception:
                    response = jsonify(
                        {'message': 'There was an error updating the recipe'})
                    response.status_code = 500
                    return response
            else:
                response = jsonify(
                    {'message': 'The category or recipe does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify(
                {'message': 'You are not authorized to edit this'})
            response.status_code = 401
            return response

    @jwt_required
    def get(self, category_id, recipe_id=None):
        """
        request that lists a single recipe
        """
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed, check url'})
            response.status_code = 400
            return response
        category = CategoryModel.find_by_id(category_id)
        recipe = RecipeModel.query.filter_by(
            id=recipe_id, category_id=category_id).first()
        user_id = get_jwt_identity()
        if category:
            if recipe:
                if recipe.created_by == user_id:
                    return marshal(recipe, recipes_serializer)
                else:
                    response = jsonify(
                        {'message': 'You are not authorized to view this'})
                    response.status_code = 401
                    return response
            else:
                response = jsonify({'message': 'The recipe does not exist'})
                response.status_code = 204
                return response
        else:
            response = jsonify({'message': 'the category does not exist'})
            response.status_code = 204
            return response

    @jwt_required
    def delete(self, category_id, recipe_id=None):
        """
        request that deletes a recipe
        """
        if recipe_id == None:
            response = jsonify({'message': 'Method not allowed (DELETE)'})
            response.status_code = 400
            return response

        recipe = RecipeModel.find_by_id(recipe_id)
        user_id = get_jwt_identity()

        if recipe:
            if recipe.created_by == user_id:
                recipe.delete_from_db()
                response = jsonify(
                    {'message': 'The recipe has been successfully deleted'})
                response.status_code = 200
                return response
            else:
                response = jsonify(
                    {'message': 'You are not authorized to del this'})
                response.status_code = 401
                return response
        else:
            response = jsonify({'message': 'The item does not exist'})
            response.status_code = 204
            return response
