import re


def is_valid(name):
    """This method is used to validate the username
    check if its fully string or string with numbers """
    name = str(name)
    validated_letter = []
    for n, letter in enumerate(name):
        letter = str(letter)
        if re.match(r'^[a-zA-Z]+$', letter):
            validated_letter.append(letter)
    if len(name) == len(validated_letter):
        return True
    else:
        return False


def validate_password(password):
    """This method is used to validate the password
    check if its strong enough with letters and numbers """
    if len(password) >= 6:
        password = str(password)
        validated_letter = []
        for n, letter in enumerate(password):
            if re.match(r'[a-zA-Z0-9]', letter):
                validated_letter.append(letter)
        if len(password) == len(validated_letter):
            return "Valid password"
    return "not strong enough"
