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

class GetCuratorTracks:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getCuratorTracks(self, curatorId: int, limit: int = None, offset: int = None) -> Union[List[Track], None]:
        """
        Получает треки куратора.

        `Пример использования`:

        tracks = client.getCuratorTracks(
            curatorId=28905875,
            limit=10,
        )

        print(tracks)

        :param curatorId: идентификатор куратора (пользователь или группа). (``int``)
        :param limit: лимит треков. (``int``, `optional`)
        :param offset: сколько треков пропустить. (``int``, `optional`)
        :return: `При успехе`: треки куратора (``list[types.Track]``). `Если куратор не найден или треки отсутствуют`: ``None``.
        """

        from vkmusix.types import Track

        tracks = await self._req(
            "getAudiosByCurator",
            {
                "curator_id": curatorId,
                "count": limit,
                "offset": offset,
            },
        )

        return self._finalizeResponse(tracks.get("items"), Track)

    get_curator_tracks = getCuratorTracks