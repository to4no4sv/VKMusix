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

class Edit:
    from vkmusix.aio import async_

    @async_
    async def edit(self, ownerId: int, trackId: int, title: str = None, artist: str = None, lyrics: str = None, genreId: int = None, removeFromSearchResults: bool = None) -> bool:
        """
        Изменяет информацию о треке.

        `Пример использования`:

        result = client.edit(
            ownerId=-2001471901,
            trackId=123471901,
            filename="Маленький ярче — LARILARI",
            title="LARILARI",
            artist="Маленький ярче",
            genreId=21,
            removeFromSearchResults=True,
        )

        print(result)

        :param ownerId: идентификатор владельца трека. (``int``)
        :param trackId: идентификатор трека. (``int``)
        :param title: название трека. (``str``, `optional`)
        :param artist: артисты трека. (``str``, `optional`)
        :param lyrics: текст трека. (``str``, `optional`)
        :param genreId: идентификатор жанра трека. (``int``, `optional`)
        :param removeFromSearchResults: флаг, указывающий, необходимо ли исключить трек из поиска. По умолчанию ``False``. (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если информацию о треке не удалось изменить`: ``False``.
        """

        if not any((title, artist, lyrics is not None, genreId is not None, removeFromSearchResults is not None)):
            return False

        response = await self._req(
            "edit",
            {
                "owner_id": ownerId,
                "audio_id": trackId,
                **({"title": title} if title else dict()),
                **({"artist": artist} if artist else dict()),
                **({"lyrics": lyrics} if lyrics is not None else dict()),
                **({"genre_id": genreId} if genreId is not None else dict()),
                **({"no_search": removeFromSearchResults} if removeFromSearchResults is not None else dict()),
            },
        )

        return bool(response)