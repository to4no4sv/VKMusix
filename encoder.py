import json
from datetime import datetime
from types import FunctionType, MethodType


class _CustomEncoder(json.JSONEncoder):
    def default(self, o) -> any:
        if isinstance(o, _BaseModel):
            return o.toDict()

        elif isinstance(o, datetime):
            return o.strftime("%d/%m/%Y %H:%M:%S")

        elif isinstance(o, type):
            return o.__name__

        return super().default(o)


class _BaseModel:
    def __init__(self, client: "Client" = None) -> None:
        self._client = client

    def toDict(self) -> any:
        result = {}
        for key, value in self.__dict__.items():
            if any((value is None, isinstance(value, (FunctionType, MethodType)), key == "_client")):
                continue

            result[key if not key.startswith("_") else key[1:]] = value

        return result

    def __repr__(self) -> any:
        return json.dumps(self.toDict(), indent=4, ensure_ascii=False, cls=_CustomEncoder)