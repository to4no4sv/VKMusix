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

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Playlist

    @asyncFunction
    async def searchPlaylists(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Playlist], Playlist, None]:
        """
        Ищет плейлисты по запросу.

        Пример использования:\n
        result = client.searchPlaylists(query="Релизы 20.10.2023", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество плейлистов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список плейлистов в виде объектов модели `Playlist`, плейлист в виде объекта модели `Playlist` (если он единственный) или `None` (если ничего не найдено).
        """

        from vkmusix.types import Playlist

        return await self._searchItems("searchPlaylists", (query, limit, offset), Playlist)