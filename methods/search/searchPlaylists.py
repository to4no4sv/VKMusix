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

class SearchPlaylists:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Playlist

    @async_
    async def searchPlaylists(self, query: str, limit: int = None, offset: int = None) -> Union[List[Playlist], None]:
        """
        Ищет плейлисты.

        `Пример использования`:

        playlists = client.searchPlaylists(
            query="Маленький ярче",
            limit=10,
        )

        print(playlists)

        :param query: поисковой запрос. (``str``)
        :param limit: лимит плейлистов. (``int``, `optional`)
        :param offset: сколько плейлистов пропустить. (``int``, `optional`)
        :return: `При успехе`: найденные плейлисты (``list[types.Playlist]``). `Если плейлисты не найдены`: ``None``.
        """

        from vkmusix.types import Playlist

        return await self._search(
            "searchPlaylists",
            (query, limit, offset),
            Playlist,
        )

    search_playlists = searchPlaylists