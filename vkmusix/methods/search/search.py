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

class Search:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import SearchResults

    @async_
    async def search(self, query: str, limit: int = None, offset: int = None) -> Union[SearchResults, None]:
        """
        Ищет артистов, альбомы, треки и плейлисты.

        `Пример использования`:

        searchResults = client.search(
            query="Маленький ярче",
            limit=10,
        )

        print(searchResults)

        :param query: поисковой запрос. (``str``)
        :param limit: лимит объектов каждого типа. (``int``, `optional`)
        :param offset: сколько объектов каждого типа пропустить. (``int``, `optional`)
        :return: `При успехе`: результаты поиска (``types.SearchResults``). `Если ничего не найдено`: ``None``.
        """

        from vkmusix.types import Artist, Album, Track, Playlist

        return await self._search(
            "searchMain",
            (query, limit, offset),
            [Artist, Album, Track, Playlist],
        )