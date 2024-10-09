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

class SetBroadcast:
    from typing import Union, List

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def setBroadcast(self, ownerId: int = None, trackId: int = None, groupIds: Union[List[str], str] = None) -> bool:
        """
        Устанавливает (удаляет) аудиотрек в (из) статус(а) пользователя или группы.

        Пример использования для установки аудиотрека в статус пользователя:\n
        result = client.setBroadcast(ownerId=474499156, trackId=456637846)\n
        print(result)

        Пример использования для установки аудиотрека в статус группы:\n
        result = client.setBroadcast(ownerId=474499156, trackId=456637846, groupdIds="yourGroupId")\n
        print(result)

        Пример использования для удаления аудиотрека из статуса пользователя:\n
        result = client.setBroadcast()\n
        print(result)

        Пример использования для удаления аудиотрека из статуса группы:\n
        result = client.setBroadcast(groupdIds="yourGroupId")\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int, необязательно)
        :param trackId: идентификатор аудиотрека, который необходимо установить в статус. (int, необязательно)
        :param groupIds: идентификатор(ы) групп(ы), в (из) статус(а) которой необходимо установить (удалить) аудиотрек. (int, по умолчанию текущий пользователь)
        :return: `True`, если аудиотрек успешно установлен (удалён) в (из) статус(а), `False` в противном случае.
        """

        response = await self._req(
            "setBroadcast",
            {
                **(
                    {
                        "audio": f"{ownerId}_{trackId}"
                    }
                    if ownerId and trackId else dict()
                ),
                **(
                    {
                        "target_ids": groupIds
                    }
                    if groupIds else dict()
                )
            },
        )

        return bool(response)