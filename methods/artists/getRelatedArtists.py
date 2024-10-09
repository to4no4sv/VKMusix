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

class GetRelatedArtists:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Artist

    @asyncFunction
    async def getRelatedArtists(self, artistId: int, limit: int = 10) -> Union[List[Artist], Artist, None]:
        """
        Получает похожих артистов.

        Пример использования:\n
        result = client.getRelatedArtists(artistId=5696274288194638935, limit=5)\n
        print(result)

        :param artistId: идентификатор артиста, похожих на которого необходимо получить. (int)
        :param limit: максимальное количество артистов, которое необходимо вернуть. (bool, по умолчанию 10)
        :return: список артистов в виде объектов модели `Artist`, артист в виде объекта модели `Artist` (если он единственственный), или None (если `artistId` неверный или похожие артисты отсутствуют).
        """

        from vkmusix.types import Artist

        artists = await self._req("getRelatedArtistsById", {"artist_id": artistId, "count": limit})

        return self._finalizeResponse(artists.get("artists"), Artist)