import pymysql
import flask
from flask import json
from functools import wraps

from commitmentscheme.api.common.errors import APIError

def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            data, code = f(*args, **kwargs)
        except APIError as e:
            response = json.jsonify({"error": e.message})
            response.status_code = e.status_code
        except pymysql.err.IntegrityError as e:
            #PATCH! Bad..
            response = json.jsonify({"error": "Conflicting resource!"})
            response.status_code = 409
        except Exception as e:
            response = json.jsonify({"error": e.message})
            response.status_code = 500
        else:
            if isinstance(data, list):
                response = flask.jsonify(data)
            else:
                response = json.jsonify(data)

            response.status_code = code

        return response
    return wrapper
