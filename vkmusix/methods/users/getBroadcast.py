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

class GetBroadcast:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getBroadcast(self, ownerId: int = None) -> Union[Track, None, bool]:
        """
        Получает трек транслируемый в статус owner'а (пользователь или группа).

        `Пример использования для получения трека, транслируемого в статус залогиненного пользователя`:

        track = client.getBroadcast()

        print(track)

        `Пример использования для получения трека, транслируемого в статус любого пользователя`:

        track = client.getBroadcast(
            ownerId=1,
        )

        print(track)

        `Пример использования для получения трека, транслируемого в статус любой группы`:

        track = client.getBroadcast(
            ownerId=-1,
        )

        print(track)

        :param ownerId: идентификатор owner'а (пользователь или группа). По умолчанию залогиненный пользователь. (``int``, `optional`)
        :return: `Если трек транслируется в статус`: транслируемый трек (``types.Track``). `Если трек не транслируется в статус`: `только для залогиненного пользователя`: флаг, указывающий, транслируются ли треки в статус при проигрывании. (``bool``). `для любого owner'а (пользователь или группа)`: ``None``.
        """

        broadcast = await self._req(
            "status.get",
            (
                {
                    "user_id": ownerId,
                }
                if ownerId > 0 else
                {
                    "group_id": -ownerId,
                }
            ) if ownerId else None
        )

        audio = broadcast.get("audio")
        if audio:
            from vkmusix.types import Track

            return self._finalizeResponse(audio, Track)

        if not ownerId or ownerId == await self._getMyId():
            isBroadcastEnabled = (await self._req("getBroadcast")).get("enabled")
            return bool(isBroadcastEnabled)

    get_broadcast = getBroadcast