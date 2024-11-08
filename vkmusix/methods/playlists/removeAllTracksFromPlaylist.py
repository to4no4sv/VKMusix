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

class RemoveAllTracksFromPlaylist:
    from vkmusix.aio import async_

    @async_
    async def removeAllTracksFromPlaylist(self, playlistId: int = None, groupId: int = None) -> bool:
        """
        Удаляет все треки из плейлиста пользователя или группы. Метод не работает для плейлистов, привязанных к чату.

        `Пример использования`:

        result = client.removeAllTracksFromPlaylist(
            playlistId=19201020,
        )

        print(result)

        :param playlistId: идентификатор плейлиста. (``int``, `optional`)
        :param groupId: идентификатор группы, из плейлиста которой необходимо удалить треки. (``int``, `optional`)
        :return: `При успехе`: ``True``. `Если плейлист не найден, треки отсутствуют или их не удалось удалить`: ``False``.
        """

        tracks = await self.getPlaylistTracks(
            playlistId,
            groupId,
        )

        if not tracks:
            return False

        ownerIds = [track.ownerId for track in tracks]
        trackIds = [track.trackId for track in tracks]

        result = await self.remove(
            ownerIds,
            trackIds,
            playlistId,
            groupId,
            False,
        )

        return bool(result[0])