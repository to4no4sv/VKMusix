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

class GetNew:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getNew(self) -> Union[List[Track], None]:
        """
        Получает треки, вышедшие недавно.

        `Пример использования`:

        tracks = client.getNew()

        print(tracks)

        :return: `При успехе`: треки (``list[types.Track]``). `Если треки отсутствуют`: ``None``.
        """

        from vkmusix.config import playlistsOwnerId

        tracks = await self.getPlaylistTracks(2, playlistsOwnerId)

        return tracks

    get_new = getNew