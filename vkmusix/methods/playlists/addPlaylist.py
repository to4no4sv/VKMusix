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

    from vkmusix.aio import async_
    from vkmusix.types import Album, Playlist

    @async_
    async def addPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None) -> Union[Playlist, Album, None]:
        """
        Добавляет плейлист или альбом в музыку пользователя или группы.

        `Пример использования`:

        playlist = client.addPlaylist(
            playlistId=19201020,
            ownerId=-2000201020,
        )

        print(playlist)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :param groupId: идентификатор группы, в которую необходимо добавить плейлист или альбом. (``int``, `optional`)
        :return: `При успехе`: информация о добавленном плейлисте или альбоме (``Union[types.Playlist, types.Album]``). `Если плейлист или альбом не найден`: ``None``.
        """

        from vkmusix.errors import NotFound
        from vkmusix.types import Playlist

        if not ownerId:
            ownerId = await self._getMyId()

        try:
            playlist = await self._req(
                "followPlaylist",
                {
                    "owner_id": ownerId,
                    "playlist_id": playlistId,
                    **(
                        {
                            "group_id": groupId,
                        }
                        if groupId else dict()
                    )
                }
            )

        except NotFound:
            return

        ownerId = playlist.get("owner_id")
        playlistId = playlist.get("playlist_id")

        if not all((ownerId, playlistId)):
            return

        return Playlist(
            {
                "owner_id": ownerId,
                "playlist_id": playlistId,
            },
            True,
            self,
        )

    add_playlist = addPlaylist