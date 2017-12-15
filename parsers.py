from flask_restful import reqparse
category_put_parser = reqparse.RequestParser()
category_put_parser.add_argument(
    'name',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)
