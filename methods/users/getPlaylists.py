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

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Album, Playlist
    from vkmusix.enums import PlaylistType

    @asyncFunction
    async def getPlaylists(self, ownerId: int = None, limit: int = None, offset: int = None, playlistTypes: Union[PlaylistType, List[PlaylistType]] = None) -> Union[List[Union[Playlist, Album]], Playlist, Album, None]:
        """
        Получает плейлисты пользователя или группы.

        Пример использования:\n
        from vkmusix.enums import PlaylistType
        result = client.getPlaylists(ownerId=-215973356, limit=10, offset=5, playlistTypes=PlaylistType.Own)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, плейлисты которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :param limit: максимальное количество объектов каждого типа, которое необходимо вернуть. (int, необязательно, максимально 10)
        :param offset: количество результатов каждого типа, которые необходимо пропустить. (int, необязательно)
        :param playlistTypes: типы плейлистов, которые необходимо получить. (PlaylistType или List[PlaylistType], необязательно)
        :return: список плейлистов в виде объектов модели `Playlist` или `Album`, плейлист в виде объекта модели `Playlist` или `Album` (если он единственственный), или `None` (если плейлисты отсутствуют).
        """

        from vkmusix.types import Album, Playlist
        from vkmusix.enums import PlaylistType

        if not ownerId:
            from vkmusix.utils import getSelfId

            ownerId = await getSelfId(self)

        if not isinstance(playlistTypes, list):
            playlistTypes = [playlistTypes]

        playlists_ = await self._req("getPlaylists", {"owner_id": ownerId, "count": limit, "offset": offset})

        playlists = self._finalizeResponse([playlist for playlist in playlists_.get("items")], Playlist)

        if not isinstance(playlists, list):
            playlists = [playlists]

        playlists = [playlist for playlist in playlists if (isinstance(playlist, Playlist) and (PlaylistType.Own if playlist.own else PlaylistType.Foreign) in playlistTypes) or (isinstance(playlist, Album) and PlaylistType.Album in playlistTypes)]

        return (playlists if len(playlists) > 1 else playlists[0]) if playlists else None