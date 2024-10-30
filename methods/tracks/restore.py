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

class Restore:
    from vkmusix.aio import async_

    @async_
    async def restore(self, ownerId: int, trackId: int) -> bool:
        """
        Восстанавливает удалённый трек.

        `Пример использования`:

        result = client.restore(
            ownerId=-2001471901,
            trackId=123471901,
        )

        print(result)

        :param ownerId: идентификатор владельца трека. (``int``)
        :param trackId: идентификатор трека. (``int``)
        :return: `При успехе`: ``True``. `Если трек не удалось восстановить`: ``False``.
        """

        response = await self._req(
            "restore",
            {
                "owner_id": ownerId,
                "audio_id": trackId,
            },
        )

        return bool(response)