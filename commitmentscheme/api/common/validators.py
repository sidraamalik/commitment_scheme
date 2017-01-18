import ujson as json
import jsonschema
from httplib import BAD_REQUEST
from functools import wraps
from flask import request
from pkg_resources import resource_string


from commitmentscheme.api.common.errors import APIError

def validate_json(schema_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.is_json is False:
                raise APIError(
                    "Please provide application/json content-type.",
                    BAD_REQUEST)

            json_data = request.get_json(silent=True)
            schema_data = json.loads(
                resource_string(
                    "commitmentscheme.api.schemas", "{0}.json".format(schema_name)))
            try:
                jsonschema.validate(
                    json_data,
                    schema_data,
                    format_checker=jsonschema.FormatChecker())
            except Exception as e:
                raise APIError(str(e), BAD_REQUEST)

            return func(*args, **kwargs)
        return wrapper
    return decorator
