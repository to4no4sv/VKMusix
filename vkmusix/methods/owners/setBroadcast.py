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

class SetBroadcast:
    from typing import Union, List

    from vkmusix.aio import async_

    @async_
    async def setBroadcast(self, ownerId: int = None, trackId: int = None, groupIds: Union[List[int], int] = None) -> bool:
        """
        Транслирует трек в статус owner'а (пользователь или группа). Также останавливает трансляцию в статус.

        `Пример использования для трансляции трека в статус залогиненного пользователя`:

        result = client.setBroadcast(
            ownerId=-2001471901,
            trackId=123471901,
        )

        print(result)

        `Пример использования для остановки трансляции трека в статус залогиненного пользователя`:

        result = client.setBroadcast()

        print(result)

        `Пример использования для трансляции трека в статус группы`:

        result = client.setBroadcast(
            ownerId=-2001471901,
            trackId=123471901,
            groupIds=1,
        )

        print(result)

        `Пример использования для остановки трансляции трека в статус группы`:

        result = client.setBroadcast(
            groupIds=1,
        )

        print(result)

        :param ownerId: идентификатор владельца трека, который необходимо транслировать в статус (пользователь или группа). Если параметр не заполнен, останавливает трансляцию в статус. (``int``, `optional`)
        :param trackId: идентификатор трека, который необходимо транслировать в статус. Если параметр не заполнен, останавливает трансляцию в статус. (``int``, `optional`)
        :param groupIds: идентификаторы групп, трансляцию в статус которых необходимо начать или остановить. По умолчанию залогиненный пользователь. (``Union[list[int], int]``, `optional`)
        :return: `При успехе`: ``True``. `В противном случае`: ``False``.
        """

        response = await self._req(
            "setBroadcast",
            {
                **(
                    {
                        "audio": f"{ownerId}_{trackId}",
                    }
                    if ownerId and trackId else dict()
                ),
                **(
                    {
                        "target_ids": groupIds,
                    }
                    if groupIds else dict()
                )
            },
        )

        return bool(response)

    set_broadcast = setBroadcast