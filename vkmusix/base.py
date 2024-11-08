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

from json import JSONEncoder

class Encoder(JSONEncoder):
    def default(self, o) -> any:
        from datetime import datetime

        if any((class_.__name__ == "Base" for class_ in o.__class__.__bases__)):
            return o._toDict()

        elif isinstance(o, datetime):
            return o.strftime("%d/%m/%Y %H:%M:%S")

        elif isinstance(o, type):
            return o.__name__

        return super().default(o)


class Base:
    def __repr__(self) -> str:
        if len(self.__dict__) == 1:
            return list(self.__dict__.values())[0]

        from json import dumps

        return dumps(self.__dict__, indent=4, ensure_ascii=False, cls=Encoder)

    __str__ = __repr__