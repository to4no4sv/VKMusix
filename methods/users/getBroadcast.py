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

class GetBroadcast:
    from typing import Union

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def getBroadcast(self, id: int = None) -> Union[Track, None, bool]:
        """
        Получает аудиотрек, транслируемый в статус.

        Пример использования для текущего пользователя:\n
        result = client.getBroadcast()\n
        print(result)

        Пример использования для любого пользователя:\n
        result = client.getBroadcast(id=1)\n
        print(result)

        :param id: идентификатор пользователя или группы, аудиотрек из статуса которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :return: аудиотрек в виде объекта модели `Track`, `None` (если ничего не проигрывается), или `False` (если музыка не транслируется в статус, работает только для текущего пользователя).
        """

        broadcast = await self._req("status.get", ({"user_id": id} if id > 0 else {"group_id": -id}) if id else None)

        audio = broadcast.get("audio")
        if audio:
            from vkmusix.types import Track

            return self._finalizeResponse(audio, Track)

        from vkmusix.utils import getSelfId

        if not id or id == (await getSelfId(self)):
            isBroadcastEnabled = (await self._req("getBroadcast")).get("enabled")
            if not bool(isBroadcastEnabled):
                return False