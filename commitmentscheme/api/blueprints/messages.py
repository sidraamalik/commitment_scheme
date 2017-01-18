from httplib import OK, BAD_REQUEST, INTERNAL_SERVER_ERROR, NO_CONTENT
from httplib import NOT_FOUND
from flask import current_app, request
from flask.views import MethodView
from Crypto.PublicKey import RSA

from commitmentscheme.api.common.validators import validate_json
from commitmentscheme.api.config.loader import ConfigLoader
from commitmentscheme.api.models.database import DBAdapter
from commitmentscheme.api.models.message import MessageModel, MessageType
from commitmentscheme.api.common.auth import authorize_request
from commitmentscheme.api.common.auth import get_credentials


import syslog

__all__ = ["MessageCollection"]


class MessageCollection(MethodView):
    @authorize_request
    @validate_json("messages_post")
    def post(self):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")
        json_data = request.get_json()

        db = DBAdapter(config)
        message = MessageModel(db)
        credentials = get_credentials(request)

        mid = message.commit(
            credentials["username"],
            json_data["message"],
            json_data["secret"])

        message_data = message.read(mid)

        return {
            'id': message_data['mid'],
            'owner': message_data['username'],
            'envelop': {
                'message': message_data['message'],
                'signature': message_data['signature']
            }
        }, 200

    def get(self):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")

        db = DBAdapter(config)
        message = MessageModel(db)

        return message.get_all(), 200

class MessageResource(MethodView):
    @authorize_request
    def get(self, mid):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")

        db = DBAdapter(config)
        message = MessageModel(db)

        message_data = message.read(mid)

        return {
            'id': message_data['mid'],
            'owner': message_data['username'],
            'type': message_data['type'],
            'envelop': {
                'message': message_data['message'],
                'signature': message_data['signature']
            }
        }, 200

    @authorize_request
    @validate_json("reveal_post")
    def post(self, mid):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")
        json_data = request.get_json()

        db = DBAdapter(config)
        message = MessageModel(db)
        credentials = get_credentials(request)

        message_data = message.reveal(credentials["username"], mid, json_data["secret"])

        return {
            'id': message_data['mid'],
            'owner': message_data['username'],
            'envelop': {
                'message': message_data['message'],
                'signature': message_data['signature']
            }
        }, 200

class MessageVerifierResource(MethodView):
    @validate_json("verify_post")
    def post(self, mid):
        loader = ConfigLoader(filename="database.cfg")
        config = loader.get("commitment_scheme")
        json_data = request.get_json()

        db = DBAdapter(config)
        message = MessageModel(db)
        credentials = get_credentials(request)

        is_verified = False
        try:
            is_verified = message.verify(json_data["username"], mid)
        except Exception as e:
            pass

        return {
            'is_verified': is_verified
        }, 200
