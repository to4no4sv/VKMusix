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

class SearchArtists:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Artist

    @async_
    async def searchArtists(self, query: str, limit: int = None, offset: int = None) -> Union[List[Artist], None]:
        """
        Ищет артистов.

        `Пример использования`:

        artists = client.searchArtists(
            query="Маленький ярче",
            limit=10,
        )

        print(artists)

        :param query: поисковой запрос. (``str``)
        :param limit: лимит артистов. (``int``, `optional`)
        :param offset: сколько артистов пропустить. (``int``, `optional`)
        :return: `При успехе`: найденные артисты (``list[types.Artist]``). `Если артисты не найдены`: ``None``.
        """

        from vkmusix.types import Artist

        return await self._search(
            "searchArtists",
            (query, limit, offset),
            Artist,
        )

    search_artists = searchArtists