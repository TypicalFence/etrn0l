"""This module hold custom extensions to flask."""

from abc import ABC, abstractmethod
from functools import wraps
from flask import request, jsonify
from flask.json import JSONEncoder
from flask_controller import FlaskController  # type: ignore
from .service import AuthService

# ----------------------------------------------------------------------------
# Json
# ----------------------------------------------------------------------------
class JsonSerializable(ABC):
    """Classes Implementing this interface will be serializable by flask."""

    @abstractmethod
    def json_serialize(self):
        pass


class CustomJSONEncoder(JSONEncoder):
    """Overwrites the default JSONEncoder of flask."""

    def default(self, obj):
        if isinstance(obj, JsonSerializable):
            return obj.json_serialize()

        return super().default(obj)


# ----------------------------------------------------------------------------
# Response Wrappers
# ----------------------------------------------------------------------------
class ApiResponse(JsonSerializable):
    def __init__(self, code=None, msg=""):
        self.code = code
        self.msg = msg
    
    def json_serialize(self):
        print(self.__dict__)
        return self.__dict__

    @staticmethod
    def ok(data=None, msg="ok", count=None):
        if count is not None:
            return ListApiResponse(code=200, msg=msg, data=data, count=count)
        if data is not None:
            return DataApiResponse(code=200, msg=msg, data=data)

        return ApiResponse(code=200, msg=msg)

    @staticmethod
    def not_found(msg="not_found"):
        return ApiResponse(code=404, msg=msg)

    @staticmethod
    def bad_request(msg="bad_request"):
        return ApiResponse(code=400, msg=msg)

    @staticmethod
    def internal_error(msg="internal_error"):
        return ApiResponse(code=500, msg=msg)

    @staticmethod
    def unauthorized(msg="unauthorized"):
        return ApiResponse(code=401, msg=msg)


class DataApiResponse(ApiResponse):
    def __init__(self, code=None, msg="", data=None):
        super().__init__(code, msg)
        self.data = data

class ListApiResponse(DataApiResponse):
    def __init__(self, code=None, msg="", data=None, count=None):
        super().__init__(code, msg, data)
        self.count = count


# ----------------------------------------------------------------------------
# Auth stuff
# ----------------------------------------------------------------------------
class SecuredController(FlaskController):
    """Ensures that a controller has an AuthService."""
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @property
    def auth_service(self) -> AuthService:
        return self._auth_service


def auth_required(f):
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        if not issubclass(type(self), SecuredController):
            # TODO: logging
            return jsonify(ApiResponse.internal_error()), 500

        auth = request.headers.get("Authorization")
        if auth is not None:
            auth = auth.split(" ")
            if auth[0] == "Bearer":
                valid = self.auth_service.check_token(auth[1])

                if valid:
                    return f(self, *args, **kwargs)
        return jsonify(ApiResponse.unauthorized()), 401
    return decorated_function

