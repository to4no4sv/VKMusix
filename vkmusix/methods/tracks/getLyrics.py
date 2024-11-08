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

class GetLyrics:
    from typing import Union

    from vkmusix.aio import async_

    @async_
    async def getLyrics(self, ownerId: int, trackId: int) -> Union[str, None]:
        """
        Получает текст трека.

        `Пример использования`:

        lyrics = client.getLyrics(
            ownerId=-2001471901,
            trackId=123471901,
        )

        print(lyrics)

        :param ownerId: идентификатор владельца трека. (``int``)
        :param trackId: идентификатор трека. (``int``)
        :return: `При успехе`: текст трека (``str``). `Если трек не найден или текст отсутствует`: ``None``.
        """

        lyrics = await self._req(
            "getLyrics",
            {
                "audio_id": f"{ownerId}_{trackId}",
            },
        )

        if not lyrics:
            return

        lyrics = lyrics.get("lyrics")

        if not lyrics:
            return

        timestamps = lyrics.get("timestamps")

        return "\n".join([line.get("line") for line in timestamps if line.get("line") is not None]) if timestamps else lyrics.get("text")

    get_lyrics = getLyrics