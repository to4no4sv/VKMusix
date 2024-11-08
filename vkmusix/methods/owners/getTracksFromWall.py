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

class GetTracksFromWall:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getTracksFromWall(self, ownerId: int = None) -> Union[List[Track], None]:
        """
        Получает треки со стены owner'а (пользователь или группа).

        `Пример использования`:

        tracks = client.getTracksFromWall(
            ownerId=-28905875,
        )

        print(tracks)

        :param ownerId: идентификатор owner'а (пользователь или группа). По умолчанию залогиненный пользователь. (``int``, `optional`)
        :return: `При успехе`: треки (``list[types.Track]``). `Если owner (пользователь или группа) не найден или треки отсутствуют`: ``None``.
        """

        if not ownerId:
            ownerId = await self._getMyId()

        tracks = (await self._req(
            "getAudioIdsBySource",
            {
                "source": "wall",
                "entity_id": ownerId,

            },
        )).get("audios")

        tracks = await self._parseAPITracks(tracks)

        return tracks

    get_tracks_from_wall = getTracksFromWall