#  VKMusix — VK Music API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/VKMusix>
#
#  This file is part of VKMusix.
#
#  VKMusix is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  VKMusix is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with VKMusix. If not, see <http://www.gnu.org/licenses/>.

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
