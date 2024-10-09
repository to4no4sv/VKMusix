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

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def getSearchTrends(self, limit: int = 10, offset: int = 0) -> Union[List[str], str, None]:
        """
        Получает самые частые поисковые запросы в музыке.

        Пример использования:\n
        result = client.getSearchTrends(limit=5)\n
        print(result)

        :param limit: максимальное количество запросов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список самых частых поисковых запросов в музыке в виде строк, самый частый поисковой запрос в музыке в виде строки (если он единственный) или `None` (если поисковые запросы отсутствуют).
        """

        return [item.get("name") for item in (await self._req("getSearchTrends", {"count": limit, "offset": offset})).get("items")]