from httplib import OK, BAD_REQUEST, INTERNAL_SERVER_ERROR, NO_CONTENT
from httplib import NOT_FOUND
from flask import current_app, request
from flask.views import MethodView
from Crypto.PublicKey import RSA

from commitmentscheme.api.common.validators import validate_json
from commitmentscheme.api.config.loader import ConfigLoader
from commitmentscheme.api.models.database import DBAdapter
from commitmentscheme.api.models.user import UserModel


import syslog

__all__ = ["UserCollection"]


class UserCollection(MethodView):
    @validate_json("users_post")
    def post(self):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")

        db = DBAdapter(config)
        user = UserModel(db)
        json_data = request.get_json()
        uid = user.create(json_data["user"], json_data["password"])
        data = user.read(json_data["user"])

        return {
            'id': data['uid'],
            'username': data['username'],
            'keys': {
                'id': data['kpid'],
                'public': data['public_key'],
                'private': data['private_key']
            }
        }, 200
