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

from types import FunctionType, MethodType
import json

class Encoder(json.JSONEncoder):
    def default(self, o) -> any:
        from datetime import datetime

        if any((class_.__name__ == 'Base' for class_ in o.__class__.__bases__)):
            return o._toDict()

        elif isinstance(o, datetime):
            return o.strftime('%d/%m/%Y %H:%M:%S')

        elif isinstance(o, type):
            return o.__name__

        try:
            return super().default(o)

        except TypeError:
            return repr(o)

class Base:
    def __init__(self, client: 'vkmusix.Client') -> None:
        self._client = client

    def __eq__(self, other: 'Base') -> bool:
        if not any((class_.__name__ == 'Base' for class_ in other.__class__.__bases__)):
            return False

        for key in self.__slots__:
            if key == 'raw':
                continue

            value = getattr(self, key, None)
            value2 = getattr(other, key, None)

            if value != value2:
                return False

        return True

    def _toDict(self) -> dict:
        result = dict()
        for key in self.__slots__:
            value = getattr(self, key, None)

            if (
                value is None or
                (
                    key == 'fullTitle' and
                    not getattr(self, 'subtitle', None)
                ) or
                isinstance(value, (FunctionType, MethodType)) or
                key in ('_client', 'raw')
            ):
                continue

            result[key if not key.startswith('_') else key[1:]] = value

        return result

    def __repr__(self) -> str:
        return json.dumps(self._toDict(), indent=4, ensure_ascii=False, cls=Encoder)