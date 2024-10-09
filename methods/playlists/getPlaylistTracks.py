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

class GetPlaylistTracks:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def getPlaylistTracks(self, playlistId: int, ownerId: int = None) -> Union[List[Track], Track, None]:
        from vkmusix.config import VK, headers
        from vkmusix.utils import getSelfId

        if not ownerId:
            ownerId = await getSelfId(self)

        tracks = await self._client.req(f"{VK}music/playlist/{ownerId}_{playlistId}", cookies=self._cookies, headers=headers, responseType="code")

        return await self._getTracks(tracks)