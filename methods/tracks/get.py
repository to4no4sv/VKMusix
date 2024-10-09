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

class Get:
    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def get(self, ownerId: int, trackId: int, includeLyrics: bool = False) -> Track:
        """
        Получает информацию об аудиотреке по его идентификатору.

        Пример использования:\n
        result = client.get(ownerId=474499244, trackId=456638035, includeLyrics=True)\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int)
        :param trackId: идентификатор аудиотрека, информацию о котором необходимо получить. (int)
        :param includeLyrics: флаг, указывающий, необходимо ли включать текст трека в ответ. (bool, по умолчанию `False`)
        :return: информация об аудиотреке в виде объекта модели `Track`.
        """

        from asyncio import gather

        from vkmusix.types import Track

        id = f"{ownerId}_{trackId}"

        tasks = [self._req("getById", {"audios": id})]

        if includeLyrics:
            tasks.append(self.getLyrics(ownerId, trackId))

        responses = await gather(*tasks)

        track = responses[0]
        if not track:
            self._raiseError("trackNotFound")

        if includeLyrics:
            track["lyrics"] = responses[1]

        return self._finalizeResponse(track, Track)