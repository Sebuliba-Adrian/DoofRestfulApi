from app.models import CategoryModel, RecipeModel


def search_categories(q, user_id):
    '''
    method that gets data based on the search query provided
    '''
    categories = CategoryModel.query.filter(CategoryModel.created_by == user_id,
                                            CategoryModel.name.contains(q))

    return categories


def search_recipes(q):
    '''
    method that gets data based on the search query provided
    '''

    recipes = RecipeModel.query.filter(RecipeModel.name.contains(q)).all()
    return recipes


def user_name_validator(value):
    pass


def recipe_validator(value):
    pass


def category_validator(value):
    pass
