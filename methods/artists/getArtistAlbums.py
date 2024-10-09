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

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Album

    @asyncFunction
    async def getArtistAlbums(self, artistId: int) -> Union[List[Album], Album, None]:
        from vkmusix.types import Album

        albums = await self._req("getAlbumsByArtist", {"artist_id": artistId})

        return self._finalizeResponse(albums.get("items"), Album)