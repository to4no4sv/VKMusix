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

class GetPlaylists:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Album, Playlist
    from vkmusix.enums import PlaylistType

    @async_
    async def getPlaylists(self, ownerId: int = None, limit: int = None, offset: int = None, playlistTypes: Union[List[PlaylistType], PlaylistType] = None) -> Union[List[Union[Playlist, Album]], None]:
        """
        Получает плейлисты и (или) альбомы owner'а (пользователь или группа).

        `Пример использования`:

        playlists = client.getPlaylists(
            ownerId=-1,
            limit=10,
        )

        print(playlists)

        :param ownerId: идентификатор owner'а (пользователь или группа). По умолчанию залогиненный пользователь. (``int``, `optional`)
        :param limit: лимит плейлистов и (или) альбомов. (``int``, `optional`)
        :param offset: сколько плейлистов и (или) альбомов пропустить. (``int``, `optional`)
        :param playlistTypes: нужные типы плейлистов. (``Union[list[enums.PlaylistType], enums.PlaylistType]``, `optional`)
        :return: `При успехе`: плейлисты и (или) альбомы (`list[Union[types.Playlist, types.Album]]). `Если owner (пользователь или группа) не найден или плейлисты и (или) альбомы отсутствуют`: ``None``.
        """

        from vkmusix.types import Album, Playlist
        from vkmusix.enums import PlaylistType

        if not ownerId:
            ownerId = await self._getMyId()

        playlists_ = await self._req(
            "getPlaylists",
            {
                "owner_id": ownerId,
                "count": limit,
                "offset": offset,
            },
        )

        playlists = self._finalizeResponse(
            [
                playlist
                for playlist in playlists_.get("items")
            ],
            Playlist,
        )

        if playlistTypes:
            if not isinstance(playlistTypes, list):
                playlistTypes = [playlistTypes]

            playlists = [playlist for playlist in playlists if (isinstance(playlist, Playlist) and (PlaylistType.Own if playlist.own else PlaylistType.Foreign) in playlistTypes) or (isinstance(playlist, Album) and PlaylistType.Album in playlistTypes)]

        return playlists if playlists else None

    get_playlists = getPlaylists