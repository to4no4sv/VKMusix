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

    from vkmusix.aio import async_
    from vkmusix.types import Playlist

    @async_
    async def createPlaylist(self, title: str, description: str = None, photo: str = None, groupId: int = None, chatId: int = None) -> Union[Playlist, None]:
        """
        Создаёт плейлист в музыке пользователя или группы.

        `Пример использования`:

        playlist = client.createPlaylist(
            title="Лучшая музыка в машину!!!",
        )

        print(playlist)

        :param title: название плейлиста. (``str``)
        :param description: описание плейлиста. (``str``, `optional`)
        :param photo: ссылка на фото плейлиста. Не работает. (``str``, `optional`)
        :param groupId: идентификатор группы, в которой необходимо создать плейлист. (``int``, `optional`)
        :param chatId: идентификатор чата, к которому необходимо привязать плейлист. (``int``, `optional`)
        :return: `При успехе`: информация о созданном плейлисте (``types.Playlist``). `Если плейлист не удалось создать`: ``None``.
        """

        from vkmusix.types import Playlist

        if not groupId:
            groupId = await self._getMyId()

        playlist = await self._req(
            "createPlaylist" if not chatId else "createChatPlaylist",
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

    create_playlist = createPlaylist