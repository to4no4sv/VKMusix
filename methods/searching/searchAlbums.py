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

class SearchAlbums:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Album

    @asyncFunction
    async def searchAlbums(self, query: str, limit: int = None, offset: int = None) -> Union[List[Album], Album, None]:
        """
        Ищет альбомы по запросу.

        Пример использования:\n
        result = client.searchAlbums(query="prombl — npc", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество альбомов, которое необходимо вернуть. (int, необязательно)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список альбомов в виде объектов модели `Album`, альбом в виде объекта модели `Album` (если он единственный) или `None` (если ничего не найдено).
        """

        from vkmusix.types import Album

        return await self._searchItems("searchAlbums", (query, limit, offset), Album)
