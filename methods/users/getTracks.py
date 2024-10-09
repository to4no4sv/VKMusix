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

class GetTracks:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def getTracks(self, groupId: int = None) -> Union[List[Track], Track, None]:
        """
        Получает треки пользователя или группы по его (её) идентификатору. (Временно не работает)

        Пример использования:\n
        result = client.getTracks(groupId=-215973356)\n
        print(result)

        :param groupId: идентификатор пользователя или группы. (int, по умолчанию текущий пользователь)
        :return: список аудиотреков в виде объектов класса `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если треки отсутствуют).
        """

        raise NotImplementedError

        from vkmusix.config import VK, headers

        if not groupId:
            from vkmusix.utils import getSelfId

            groupId = await getSelfId(self)

        tracks = await self._client.req(VK + "audios" + str(groupId), cookies=self._cookies if hasattr(self, "_cookies") else None, headers=headers, responseType="code")
        tracks = await self._getTracks(tracks)

        return tracks