import re

from app.models import CategoryModel, RecipeModel


def search_categories(query, user_id):
    """
    method that gets data based on the search query provided
    """
    categories = CategoryModel.query.filter(
        CategoryModel.created_by == user_id,
        CategoryModel.name.contains(query.lower()))

    return categories


def search_recipes(query):
    """
    method that gets data based on the search query provided
    """

    recipes = RecipeModel.query.filter(RecipeModel.name.contains(query)).all()
    return recipes


def username_validator(username):
    """ 
    This function handles username validation
    """
    if username:
        if username.strip():
            if 3 < len(username) < 16:
                if re.match("^[a-zA-Z0-9_.-]+$", username):
                    return username
                raise ValueError(
                    "Special characters in username {0} are not allowed"
                    .format(username))
            raise ValueError(
                "Username {0} should be 4 to 15 characters long".
                format(username))

        raise ValueError("Blank space is not allowed for the username field")

    raise ValueError("No input provided for the username field")


def category_name_validator(category):
    """ 
    This function handles category name validation

    """
    if category:
        if category.strip():

            if re.match("^[a-zA-Z0-9\s]+$", category):
                return category
            raise ValueError(
                "Only alphanumeric characters are allowed for the category "
                "name")

        raise ValueError(
            "Blank space is not allowed for the category name field")

    raise ValueError("No input provided for the category name field")


def recipe_name_validator(recipe):
    """ 
    This function handles recipe name validation

    """
    if recipe:
        if recipe.strip():

            if re.match("^[a-zA-Z0-9\s]+$", recipe):
                return recipe
            raise ValueError(
                "Only alphanumeric characters are allowed for the recipe name")

        raise ValueError(
            "Blank spaces are not allowed in the recipe name field")

    raise ValueError("No input provided in the recipe name field")
