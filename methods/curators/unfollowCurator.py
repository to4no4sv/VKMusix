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

class UnfollowCurator:
    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def unfollowCurator(self, curatorId: int = None) -> bool:
        """
        Отписывается от обновлений музыки куратора.

        Пример использования:\n
        result = client.unfollowCurator(curatorId=28905875)\n
        print(result)

        :param curatorId: идентификатор куратора, от обновлений которого необходимо отписаться. (int)
        :return: `True`, если Вы успешно отписались от обновлений музыки куратора, `False` в противном случае.
        """

        response = await self._req("unfollowCurator", {"curator_id": curatorId})
        return bool(response)