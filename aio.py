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

import asyncio
from functools import wraps, partial


class SyncToAsync:
    def __init__(self, func):
        self.func = func


    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


    def __call__(self, instance, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return self.func(instance, *args, **kwargs)

            else:
                return loop.run_until_complete(self.func(instance, *args, **kwargs))

        except RuntimeError:
            newLoop = asyncio.new_event_loop()
            asyncio.set_event_loop(newLoop)
            result = newLoop.run_until_complete(self.func(instance, *args, **kwargs))
            newLoop.close()
            return result

        finally:
            asyncio.set_event_loop(loop)


def asyncFunction(func):
    @wraps(func)
    async def wrapper(instance, *args, **kwargs):
        return await func(instance, *args, **kwargs)
    return SyncToAsync(wrapper)
