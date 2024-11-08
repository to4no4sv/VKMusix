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

class GetArtistAlbums:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Album

    @async_
    async def getArtistAlbums(self, artistId: int, limit: int = None, offset: int = None) -> Union[List[Album], None]:
        """
        Получает альбомы артиста.

        `Пример использования`:

        albums = client.getArtistAlbums(
            artistId=5696274288194638935,
            limit=10,
        )

        print(albums)

        :param artistId: идентификатор артиста. (``int``)
        :param limit: лимит альбомов. (``int``, `optional`)
        :param offset: сколько альбомов пропустить. (``int``, `optional`)
        :return: `При успехе`: альбомы артиста (``list[types.Album]``). `Если артист не найден или альбомы отсутствуют`: ``None``.
        """

        from vkmusix.types import Album

        albums = await self._req(
            "getAlbumsByArtist",
            {
                "artist_id": artistId,
                "count": limit,
                "offset": offset,
            },
        )

        return self._finalizeResponse(albums.get("items"), Album)

    get_artist_albums = getArtistAlbums