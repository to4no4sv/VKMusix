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

class GetRecommendations:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getRecommendations(self, limit: int = None, offset: int = None, ownerId: int = None, trackId: int = None) -> Union[List[Track], None]:
        """
        Получает пользовательские рекомендации, или рекомендации по треку, если заполнены параметры ``ownerId`` и ``trackId``.

        `Пример использования для пользовательских рекомендаций`:

        tracks = client.getRecommendations(
            limit=10,
        )

        print(tracks)

        `Пример использования для рекомендаций по треку`:

        tracks = client.getRecommendations(
            limit=10,
            ownerId=-2001471901,
            trackId=123471901,
        )

        print(tracks)

        :param limit: лимит треков. Для пользовательских рекомендаций минимально 10. (``int``, `optional`)
        :param offset: сколько треков пропустить. (``int``, `optional`)
        :param ownerId: идентификатор владельца трека. (``int``, `optional`)
        :param trackId: идентификатор трека. (``int``, `optional`)
        :return: `При успехе`: рекомендации (``list[types.Track]``). `Если рекомендации отсутствуют или трек не найден`: ``None``.
        """

        from vkmusix.types import Track

        if not all((ownerId, trackId)) and limit < 10:
            limit = 10

        tracks = await self._req(
            "getRecommendations",
            {
                "count": limit,
                "offset": offset,
                **(
                    {
                        "target_audio": f"{ownerId}_{trackId}"
                    }
                    if all((ownerId, trackId)) else dict(),
                ),
            },
        )

        return self._finalizeResponse(tracks.get("items"), Track)

    get_recommendations = getRecommendations