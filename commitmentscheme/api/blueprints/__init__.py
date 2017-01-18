from __future__ import absolute_import
from flask import Blueprint, current_app

from commitmentscheme.api.utils.response import json_response
from commitmentscheme.api.blueprints.users import UserCollection
from commitmentscheme.api.blueprints.messages import (
    MessageCollection, MessageResource, MessageVerifierResource)

__all__ = ["cs_bp"]


cs_bp = Blueprint("cs_bp", __name__)

@cs_bp.route("/status")
def api_status():
    return '{"status": "Up and running!"}', 200


def add_route(route, view_class, view_name):
    view = json_response(view_class.as_view(view_name))
    cs_bp.add_url_rule(route, view_func=view)

add_route("/users", UserCollection, "users")
add_route("/messages", MessageCollection, "messages")
add_route("/messages/<mid>", MessageResource, "message")
add_route("/messages/<mid>/reveal", MessageResource, "reveal")
add_route("/messages/<mid>/verify", MessageVerifierResource, "verify")
