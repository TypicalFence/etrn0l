"""This module hold custom extensions to flask."""

from abc import ABC, abstractmethod
from flask.json import JSONEncoder


class JsonSerializable(ABC):
    @abstractmethod
    def json_serialize(self):
        pass


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonSerializable):
            return obj.json_serialize()

        return super().default(obj)
