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
    from vkmusix.aio import async_

    @async_
    async def removePlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None, validateIds: bool = True) -> bool:
        """
        Удаляет плейлист или альбом из музыки пользователя или группы.

        `Пример использования`:

        result = client.removePlaylist(
            playlistId=19201020,
            ownerId=-2000201020,
        )

        print(result)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :param groupId: идентификатор группы, из которой необходимо удалить плейлист или альбом. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить плейлист или альбом на наличие в музыке. По умолчанию ``True``. Установите на ``False``, если вы получили плейлист или альбом через ``client.getPlaylists()`` или ``client.getAllPlaylists()``. (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если плейлист или альбом не найден или не получилось его удалить`: ``False``.
        """

        from vkmusix.errors import NotFound

        if not ownerId:
            ownerId = await self._getMyId()

        if not groupId:
            groupId = await self._getMyId()

        if validateIds:
            from vkmusix.enums import PlaylistType

            existPlaylists = await self.getAllPlaylists(
                groupId,
                [
                    PlaylistType.Foreign,
                    PlaylistType.Album,
                ],
            )

            if not existPlaylists:
                return False

            playlist = await self.getPlaylist(
                playlistId,
                ownerId,
            )

            for existPlaylist in existPlaylists:
                original = existPlaylist.original

                if not original:
                    continue

                if original.id == playlist.id:
                    playlistId = existPlaylist.playlistId or existPlaylist.albumId
                    break

        try:
            result = await self._req(
                "deletePlaylist",
                {
                    "owner_id": groupId,
                    "playlist_id": playlistId,
                },
            )

        except NotFound:
            return False

        return bool(result)

    remove_playlist = removePlaylist