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

class GetArtist:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import Artist

    @async_
    async def getArtist(self, artistId: int, includeAlbums: bool = False, includeTracks: bool = False) -> Union[Artist, None]:
        """
        Получает информацию об артисте.

        `Пример использования`:

        artist = client.getArtist(
            artistId=5696274288194638935,
            includeAlbums=True,
            includeTracks=True,
        )

        print(artist)

        :param artistId: идентификатор артиста. (``int``)
        :param includeAlbums: флаг, указывающий, небходимо ли также получить альбомы. (``bool``, `optional`)
        :param includeTracks: флаг, указывающий, небходимо ли также получить треки. (``bool``, `optional`)
        :return: `При успехе`: информация об артисте (``types.Artist``). `Если артист не найден`: ``None``.
        """

        from asyncio import gather

        from vkmusix.types import Artist

        tasks = [self._req(
            "getArtistById",
            {
                "artist_id": artistId,
            },
        )]

        if includeAlbums:
            tasks.append(self.getArtistAlbums(artistId))

        if includeTracks:
            tasks.append(self.getArtistTracks(artistId))

        responses = await gather(*tasks)

        artist = responses[0]

        if not artist.get("name"):
            return

        if includeAlbums:
            artist["albums"] = responses[1]

        if includeTracks:
            artist["tracks"] = responses[2 if includeAlbums else 1]

        return self._finalizeResponse(artist, Artist)

    get_artist = getArtist