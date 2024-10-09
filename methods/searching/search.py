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
    from typing import Union, Dict

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Artist, Album, Track, Playlist

    @asyncFunction
    async def search(self, query: str, limit: int = 10, offset: int = 0) -> Union[Dict[str, Union[Artist, Album, Track, Playlist]], None]:
        """
        Ищет артистов, альбомы, аудиотреки и плейлисты по запросу.

        Пример использования:\n
        result = client.search(query="prombl", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество объектов каждого типа, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов каждого типа, которые необходимо пропустить. (int, необязательно)
        :return: словарь содержащий один, несколько или все ключи из `artists`, `albums`, `tracks`, `playlists` (если ничего не найдено, то ключ отсутствует), или `None` (если ничего не найдено). Каждый из ключей содержит список объектов этого типа в виде объектов модели или объект этого типа в виде объекта модели (если он единственный).
        """

        from vkmusix.types import Artist, Album, Track, Playlist

        return await self._search("searchMain", (query, limit, offset), [Artist, Album, Track, Playlist])