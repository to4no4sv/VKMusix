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

class AddPlaylist:
    from typing import Union

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Playlist

    @asyncFunction
    async def addPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None) -> Union[Playlist, None]:
        """
        Добавляет плейлист в музыку пользователя или группы.

        Пример использования:\n
        result = client.addPlaylist(playlistId=1, ownerId=-215973356, groupId="yourGroupId")\n
        print(result)

        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param playlistId: идентификатор плейлиста, который необходимо добавить. (int)
        :param groupId: идентификатор группы, в которую необходимо добавить плейлист. (int, необязательно)
        :return: добавленный плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id`, `url` и `own`, если плейлист успешно добавлен, `None` в противном случае.
        """

        from vkmusix.types import Playlist

        if not ownerId:
            from vkmusix.utils import getSelfId

            ownerId = await getSelfId(self)

        response = await self._req(
            "followPlaylist",
            {
                "owner_id": ownerId,
                "playlist_id": playlistId,
                **(
                    {
                        "group_id": groupId
                    }
                    if groupId else dict()
                )
            }
        )

        return Playlist(
            {
                "owner_id": groupId,
                "playlist_id": playlistId,
            },
            True,
            self,
        )