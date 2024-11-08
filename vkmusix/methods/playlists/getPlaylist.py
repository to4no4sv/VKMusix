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

class GetPlaylist:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import Album, Playlist

    @async_
    async def getPlaylist(self, playlistId: int, ownerId: int = None, includeTracks: bool = False) -> Union[Playlist, Album, None]:
        """
        Получает информацию о плейлисте или альбоме.

        `Пример использования`:

        playlist = client.getPlaylist(
            playlistId=19201020,
            ownerId=-2000201020,
            includeTracks=True,
        )

        print(playlist)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :param includeTracks: флаг, указывающий, небходимо ли также получить треки. (``bool``, `optional`)
        :return: `При успехе`: информация о плейлисте или альбоме (``Union[types.Playlist, types.Album]``). `Если плейлист или альбом не найден`: ``None``.
        """

        from asyncio import gather

        from vkmusix.types import Playlist

        if not ownerId:
            ownerId = await self._getMyId()

        tasks = [
            self._req(
                "getPlaylistById",
                {
                    "owner_id": ownerId,
                    "playlist_id": playlistId,
                },
            )
        ]

        if includeTracks:
            tasks.append(self.getPlaylistTracks(playlistId, ownerId, None))

        responses = await gather(*tasks)

        playlist = responses[0]
        if not playlist:
            return

        if isinstance(playlist, dict):
            errorMessage = playlist.get("error_msg")

            if errorMessage == "One of the parameters specified was missing or invalid: playlist_id should be greater than 0":
                return

        if includeTracks:
            playlist["tracks"] = responses[1]

        return self._finalizeResponse(playlist, Playlist)

    get_playlist = getPlaylist