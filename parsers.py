from flask_restful import reqparse

# Parser for category put request
category_put_parser = reqparse.RequestParser()
category_put_parser.add_argument(
    'name',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)

# Parser for recipes put request
recipe_put_parser = reqparse.RequestParser()
recipe_put_parser.add_argument('name',
                               type=str,
                               required=True,
                               help="This field cannot be left blank!")

recipe_put_parser.add_argument('description',
                               type=str,
                               required=True,
                               help="This field cannot be left blank!")
recipe_put_parser.add_argument('category_id',
                               type=int,
                               required=True,
                               help="Every recipe needs a category id.")

# Parser for recipes post request
recipe_post_parser = reqparse.RequestParser()
recipe_post_parser.add_argument('name',
                                type=str,
                                required=True,
                                help="This field cannot be left blank!")

recipe_post_parser.add_argument('description',
                                type=str,
                                required=True,
                                help="This field cannot be left blank!")
recipe_post_parser.add_argument('category_id',
                                type=int,
                                required=True,
                                help="Every recipe needs a category id.")


# Parser for categories post request
category_post_parser = reqparse.RequestParser()
category_post_parser.add_argument('name',
                                  type=str,
                                  required=True,
                                  help="This field cannot be left blank!")
