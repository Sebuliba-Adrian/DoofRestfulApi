
from models.category import CategoryModel
from models.recipe import RecipeModel
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pre_load, validate

ma = Marshmallow()


class CategoryModelSchema(ma.ModelSchema):
    class Meta:
        model = CategoryModel
    url = ma.URLFor('categorylist', id='<id>', _external=True)




class RecipeModelSchema(ma.ModelSchema):
    class Meta:
        model = RecipeModel
