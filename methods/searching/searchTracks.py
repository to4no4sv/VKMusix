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

class SearchTracks:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def searchTracks(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Track], Track, None]:
        """
        Ищет аудиотреки по запросу.

        Пример использования:\n
        result = client.searchTracks(query="prombl — zapreti", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный) или `None` (если ничего не найдено).
        """

        from vkmusix.types import Track

        return await self._searchItems("search", (query, limit, offset), Track)