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

class GetAllPlaylists:
    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Album, Playlist
    from vkmusix.enums import PlaylistType

    @asyncFunction
    async def getAllPlaylists(self, ownerId: int = None, playlistTypes: Union[PlaylistType, List[PlaylistType]] = None) -> Union[List[Union[Playlist, Album]], Playlist, Album, None]:
        """
        Получает все плейлисты пользователя или группы.

        Пример использования:\n
        from vkmusix.enums import PlaylistType
        result = client.getAllPlaylists(ownerId=-215973356, playlistTypes=PlaylistType.Own)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, плейлисты которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :param playlistTypes: типы плейлистов, которые необходимо получить. (PlaylistType или List[PlaylistType], необязательно)
        :return: список плейлистов в виде объектов модели `Playlist` или `Album`, плейлист в виде объекта модели `Playlist` или `Album` (если он единственственный), или `None` (если плейлисты отсутствуют).
        """

        from asyncio import gather

        from vkmusix.types import Album, Playlist
        from vkmusix.enums import PlaylistType

        if not ownerId:
            from vkmusix.utils import getSelfId

            ownerId = await getSelfId(self)

        if not isinstance(playlistTypes, list):
            playlistTypes = [playlistTypes]

        playlistsPerReq = 10

        method = "getPlaylists"
        params = {"owner_id": ownerId, "count": playlistsPerReq}
        playlists_ = await self._req(method, params)

        playlists = [playlist for playlist in playlists_.get("items")]
        count = playlists_.get("count")
        offset = count if count < playlistsPerReq else playlistsPerReq

        if offset < count:
            tasks = list()
            while offset < count:
                tasks.append(self._req(method, {**params, **{"offset": offset}}))
                offset += playlistsPerReq

            playlists_ = await gather(*tasks)
            for playlistGroup in playlists_:
                for playlist in playlistGroup.get("items"):
                    playlists.append(playlist)

        playlists = self._finalizeResponse(playlists, Playlist)

        if not isinstance(playlists, list):
            playlists = [playlists]

        playlists = [playlist for playlist in playlists if (isinstance(playlist, Playlist) and (PlaylistType.Own if playlist.own else PlaylistType.Foreign) in playlistTypes) or (isinstance(playlist, Album) and PlaylistType.Album in playlistTypes)]

        return (playlists if len(playlists) > 1 else playlists[0]) if playlists else None