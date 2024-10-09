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

class RemovePlaylist:
    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def removePlaylist(self, playlistId: int, groupId: int = None) -> bool:
        """
        Удаляет плейлист из музыки пользователя или группы.

        Пример использования:\n
        result = client.removePlaylist(playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param playlistId: идентификатор плейлиста, который необходимо удалить. (int)
        :param groupId: идентификатор группы, из которой необходимо удалить плейлист. (int, необязательно)
        :return: `True`, если плейлист успешно удалён, `False` в противном случае.
        """

        if not groupId:
            from vkmusix.utils import getSelfId

            groupId = await getSelfId(self)

        response = await self._req("deletePlaylist", {"owner_id": groupId, "playlist_id": playlistId})

        return bool(response)