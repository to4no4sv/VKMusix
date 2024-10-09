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

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def getRecommendations(self, limit: int = None, offset: int = None, ownerId: int = None, trackId: int = None) -> Union[List[Track], Track, None]:
        """
        Получает рекомендации аудиотреков для пользователя или похожие на аудиотрек.

        Пример использования для рекомендаций пользователя:\n
        result = client.getRecommendations(limit=20)\n
        print(result)

        Пример использования для рекомендаций по аудиотреку:\n
        result = client.getRecommendations(limit=5, ownerId=474499156, trackId=456637846)\n
        print(result)

        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, необязательно, минимально для пользовательских рекомендаций 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа).
        :param trackId: идентификатор аудиотрека, похожие на который необходимо получить.
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если рекомендации или похожие треки отсутствуют).
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
                    if all((ownerId, trackId)) else dict()
                )
            }
        )

        return self._finalizeResponse(tracks.get("items"), Track)