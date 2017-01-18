import base64
from httplib import UNAUTHORIZED, BAD_REQUEST
from flask import request

from commitmentscheme.api.common.errors import APIError
from commitmentscheme.api.utils.password import SecurePassword
from commitmentscheme.api.models.database import DBAdapter
from commitmentscheme.api.models.user import UserModel
from commitmentscheme.api.config.loader import ConfigLoader

def get_credentials(request):
    credentials = base64.b64decode(
        request.headers['Authorization']).strip().split(":")

    if not credentials or len(credentials) != 2:
        raise APIError(
            "Please provide base64 encoded user/pass in 'Authorization' header",
            BAD_REQUEST)


    return {
        'username': credentials[0],
        'password': credentials[1]
    }


# TODO: USE THIS!
def authorize_request(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise APIError(
                "Please provide base64 encoded user/pass in 'Authorization' header",
                BAD_REQUEST)

        credentials = get_credentials(request)

        # BAD! Can be cleaned up.
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")
        db = DBAdapter(config)
        user = UserModel(db)
        user_data = user.read(credentials["username"])
        secure_password = SecurePassword()
        treated = secure_password.treat(credentials["password"])

        if credentials and treated == user_data["password"]:
            return func(*args, **kwargs)

        raise APIError(
            "Please provide valid credentials!",
            UNAUTHORIZED)
    return wrapper
