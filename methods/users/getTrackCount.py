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

class GetTrackCount:
    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def getTrackCount(self, ownerId: int) -> int:
        """
        Получает количество аудиотреков, принадлежащих этому пользователю или группе.

        Пример использования:\n
        result = client.getTrackCount(ownerId=-215973356)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы. (int)
        :return: количество аудиотреков, принадлежащих пользователю или группе, в виде целого числа.
        """

        return await self._req("getCount", {"owner_id": ownerId})