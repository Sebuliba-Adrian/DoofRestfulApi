import random
import re

from app.models import CategoryModel, RecipeModel


def search_categories(query, user_id):
    """
    method that gets data based on the search query provided
    """
    categories = CategoryModel.query.filter(
        CategoryModel.created_by == user_id,
        CategoryModel.name.ilike("%{0}%".format(query)))

    return categories


def search_recipes(query):
    """
    method that gets data based on the search query provided
    """

    recipes = RecipeModel.query.filter(RecipeModel.name.
                                       ilike("%{0}%".format(query))).all()
    return recipes


def username_validator(username):
    """ 
    This function handles username validation
    """
    if username:
        if not isinstance(username, (int, float)):
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

            raise ValueError(
                "Blank space is not allowed for the username field")
        raise ValueError("Number types are not allowed for the username")

    raise ValueError("No input provided for the username field")


def category_name_validator(category):
    """ 
    This function handles category name validation

    """
    if category:
        if not isinstance(category, (int, float)):
            if category.strip():

                if re.match("^[A-Za-z0-9]*$|^[A-Za-z0-9][A-Za-z0-9 ]*"
                            "[A-Za-z0-9]$",
                            category):
                    return category
                raise ValueError(
                    "Only alphanumeric characters are allowed for the "
                    "category "
                    "name")

            raise ValueError(
                "Blank space is not allowed for the category name field")
        raise ValueError(
            "Numbers are not allowed for the category name field")

    raise ValueError("No input provided for the category name field")


def recipe_name_validator(recipe):
    """ 
    This function handles recipe name validation

    """
    if recipe:
        if not isinstance(recipe, (int, float)):
            if recipe.strip():

                if re.match("^[A-Za-z0-9]*$|^[A-Za-z-9][A-Za-z0-9 ]*"
                            "[A-Za-z0-9]$",
                            recipe):
                    return recipe
                raise ValueError(
                    "Only alphanumeric characters are allowed for the recipe "
                    "name")

            raise ValueError(
                "Blank spaces are not allowed in the recipe name field")
        raise ValueError(
            "Numbers are not allowed for the recipe name field")
    raise ValueError("No input provided in the recipe name field")


def email_validator(email):
    """ 
    This function handles password validation
    """
    if email:
        if not isinstance(email, (int, float)):
            if email.strip():

                if 4 < len(email) < 254:
                    if re.match(r'[a-zA-Z0-9.-]+@[a-z]+\.[a-z]+', email):
                        return email
                    raise ValueError(
                        "Invalid characters or format, try again!")

                raise ValueError(
                    "Email address  should be 4 to 254 characters long")

            raise ValueError("Blank space is not allowed for the email field")
        raise ValueError("Numbers are not allowed for the email field")

    raise ValueError("No input provided for the email field")


def random_password(length=3):
    """ Create a a random password to display if the
       primary validation fails. """

    valid_upcase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    valid_lowcase = 'abcdefghijklmnopqrstuvwxyz'
    valid_specs = '!$@&'
    valid_digits = '1234567890'

    return ''.join((random.choice(valid_upcase) + random.choice(
        valid_lowcase) + random.choice(valid_specs) + random.choice(
        valid_digits) for i in range(length)))


def length_error(password):
    """ Validate that the password is over 3 characters
       and no more than 25 characters. """

    return not 3 < len(password) < 25


def lower_error(password):
    return re.search(r"[a-z]", password)


def symbol_error(password):
    return re.search(r"[!@$&]", password)


def upcase_error(password):
    return re.search(r"[A-Z]", password)


def digit_error(password):
    return re.search(r"\d", password)


def password_validator(password):
    """ Where the validation occurs, if the password does
       not pass one of the following tests, it will output
       a random string that does pass the test. """

    if isinstance(password, (int, float)):
        raise ValueError(
            "Please provide a string type for the passord, try this: {0}".format(
                random_password()))

    if not password:
        raise ValueError(
            "Please provide a passord, you may try this: {0}".format(
                random_password()))

    if lower_error(password) is None or upcase_error(password) is None:
        raise ValueError(
            "Uppercase or Lowercase requirements not met, you may try this: "
            "{0}".format(
                random_password()))

    elif digit_error(password) is None or symbol_error(password) is None:
        raise ValueError(
            "Integer and special characters requirements not met, you may "
            "try this: {0}".format(
                random_password()))

    elif length_error(password) is None:
        raise ValueError(
            " 8 to 20 characters requirements not met, you may try this: {0}".
                format(random_password()))
    else:
        return password
