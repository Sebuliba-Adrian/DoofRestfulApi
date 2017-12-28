from flask_restful import fields

users_serializer = {
    "id": fields.Integer,
    "username": fields.String
}

recipes_serializer = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "category_id": fields.Integer,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
}


categories_serializer = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
    "created_by": fields.Integer,
    "recipes": fields.List(fields.Nested(recipes_serializer))
}
