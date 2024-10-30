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

class Get:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def get(self, ownerId: int, trackId: int, includeLyrics: bool = False) -> Union[Track, None]:
        """
        Получает информацию о треке.

        `Пример использования`:

        track = client.get(
            ownerId=-2001471901,
            trackId=123471901,
            includeLyrics=True,
        )

        print(track)

        :param ownerId: идентификатор владельца трека. (``int``)
        :param trackId: идентификатор трека. (``int``)
        :param includeLyrics: флаг, указывающий, небходимо ли также получить текст. (``bool``, `optional`)
        :return: `При успехе`: информация о треке (``types.Track``). `Если трек не найден`: ``None``.
        """

        from asyncio import gather

        from vkmusix.types import Track

        id = f"{ownerId}_{trackId}"

        tasks = [self._req(
            "getById",
            {
                "audios": id,
            },
        )]

        if includeLyrics:
            tasks.append(self.getLyrics(ownerId, trackId))

        responses = await gather(*tasks)

        track = responses[0]
        if not track:
            return

        if includeLyrics:
            track["lyrics"] = responses[1]

        return self._finalizeResponse(track, Track)