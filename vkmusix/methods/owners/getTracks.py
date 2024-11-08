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

class GetTracks:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getTracks(self, sectionId: str) -> Union[List[Track], None]:
        """
        Получает треки из раздела музыки.

        `Пример использования`:

        tracks = client.getTracks(
            sectionId="PUlQVA8GR0R3W0tMF1kSOSceDR9aRzQEKgQKHRcYSV5kUUREDQ1bU35cXFoXAFtEfEZYWhcBSVxkDAwYUEYKCmRHS0IXDlpKZFpcVA8FR0R0XUtMGAZTX3ZeUUEASQ",
        )

        print(tracks)

        :param sectionId: идентификатор раздела музыки. (``str``)
        :return: `При успехе`: треки (``list[types.Track]``). `Если раздел не найден или треки отсутствуют`: ``None``.
        """

        tracks = (await self._req(
            "getAudioIdsBySource",
            {
                "source": "catalog",
                "entity_id": sectionId,
            },
        )).get("audios")

        tracks = await self._parseAPITracks(tracks)

        return tracks

    get_tracks = getTracks