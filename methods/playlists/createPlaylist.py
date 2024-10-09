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

class CreatePlaylist:
    from typing import Union

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Playlist

    @asyncFunction
    async def createPlaylist(self, title: Union[str, int], description: Union[str, int] = None, photo: str = None, groupId: int = None, chatId: int = None) -> Union[Playlist, None]:
        """
        Создаёт плейлист в музыке пользователя или группы.

        Пример использования:\n
        result = client.createPlaylist(title="prombl — npc", description="Release Date: December 24, 2021", "photo"="yourPhotoFilename", "groupId"="yourGroupId", chatId="yourChatId")\n
        print(result)

        :param title: название плейлиста. (str)
        :param description: описание плейлиста. (str, необязательно)
        :param photo: фото плейлиста. (str, необязательно, временно не работает)
        :param groupId: идентификатор группы, в которой необходимо создать плейлист. (int, необязательно)
        :param chatId: идентификатор чата, к которому небходимо привязать плейлист. (int, формат: `2000000000 + идентификатор чата`, необязательно)
        :return: созданный плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id`, `url` и `own`, если плейлист успешно создан, `None` в противном случае.
        """

        from vkmusix.types import Playlist

        if not groupId:
            from vkmusix.utils import getSelfId

            groupId = await getSelfId(self)

        playlist = await self._req(
            "createPlaylist"
            if not chatId else "createChatPlaylist",
            {
                "title": title,
                "description": description,
                "owner_id": groupId
            }
        )

        playlistId = playlist.get("id")
        if chatId:
            groupId = playlist.get("owner_id")

        """if photo:
            await self._editPlaylistPhoto(playlistId, photo, groupId)"""

        return Playlist(
            {
                "owner_id": groupId,
                "playlist_id": playlistId,
            },
            True,
            self,
        )