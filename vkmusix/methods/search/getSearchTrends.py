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

class GetSearchTrends:
    from typing import Union, List

    from vkmusix.aio import async_

    @async_
    async def getSearchTrends(self, limit: int = None, offset: int = None) -> Union[List[str], None]:
        """
        Получает популярные поисковые запросы.

        `Пример использования`:

        searches = client.getSearchTrends(
            limit=10,
        )

        print(searches)

        :param limit: лимит поисковых запросов. (``int``, `optional`)
        :param offset: сколько поисковых запросов пропустить. (``int``, `optional`)
        :return: `При успехе`: поисковые запросы (``list[str]``). `Если поисковые запросы отсутствуют`: ``None``.
        """

        searchTrends = await self._req(
            "getSearchTrends",
            {
                "count": limit,
                "offset": offset,
            },
        )

        searchTrends = [
            item.get("name")
            for item in searchTrends.get("items")
        ]

        return searchTrends if searchTrends else None

    get_search_trends = getSearchTrends