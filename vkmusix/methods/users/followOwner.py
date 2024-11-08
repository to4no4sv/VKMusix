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

class FollowOwner:
    from vkmusix.aio import async_

    @async_
    async def followOwner(self, ownerId: int) -> bool:
        """
        Подписывается на обновления музыки пользователя или группы.

        `Пример использования`:

        result = client.followOwner(
            ownerId=-28905875,
        )

        print(result)

        :param ownerId: идентификатор owner'а (пользователь или группа). (``int``)
        :return: `При успехе`: ``True``. `Если owner (пользователь или группа) не найден`: ``False``.
        """

        from vkmusix.errors import NotFound

        try:
            response = await self._req(
                "followOwner",
                {
                    "owner_id": ownerId,
                },
            )

        except NotFound:
            return False

        return bool(response)

    follow_owner = followOwner