from flask import g, request

from app import app


@app.before_request
def before_request():
    """
    Validates token.
    Is run before all requests apart from user registration, login and index.
    """
    if request.endpoint not in ["userlogin", "userregister", "index"]:
        id= get_jwt_identity()
        
        if id :
            user = UserModel.get_by_id(id)
            if user:
                g.user = user
            else:
                return {"Error: The token you have entered is "
                                    "invalid."}, 401
        else:
            return {"Error: Please enter a token."}, 401
