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

class GetPlaylistTracks:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def getPlaylistTracks(self, playlistId: int, ownerId: int = None, isLarge: bool = False) -> Union[List[Track], None]:
        """
        Получает треки плейлиста или альбома.

        `Пример использования`:

        tracks = client.getPlaylistTracks(
            playlistId=19201020,
            ownerId=-2000201020,
        )

        print(tracks)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :param isLarge: флаг, указывающий, содержит ли плейлист или альбом более 1000 треков. По умолчанию ``False``. Если ``True``, будет получена ограниченная информация о всех треках, если ``False`` — только последние 1000 треков, но с полной информацией. Установите ``None``, чтобы библиотека определила автоматически. Игнорируется для приватных плейлистов. (``bool``, `optional`)
        :return: `При успехе`: треки плейлиста или альбома (``list[types.Track]``). `Если плейлист или альбом не найден или треки отсутствуют`: ``None``.
        """

        from vkmusix.config import VK, headers

        if not ownerId:
            ownerId = await self._getMyId()

        if isLarge is None:
            playlist = await self.getPlaylist(
                playlistId,
                ownerId,
            )

            if not playlist:
                return

            isLarge = playlist.trackCount and playlist.trackCount > 1000

        if not isLarge:
            tracks = await self._client.req(
                f"{VK}music/playlist/{ownerId}_{playlistId}",
                headers=headers,
                responseType="response",
            )

            statusCode = tracks.status_code

            if statusCode == 404:
                return

            while statusCode == 302:
                tracks = await self._client.req(
                    f'{VK}{tracks.headers.get("Location")}',
                    headers=headers,
                    responseType="response",
                )
                statusCode = tracks.status_code

            tracks = await self._parseWebTracks(tracks.text)

        else:
            tracks = None

        if not tracks:
            tracks = (await self._req(
                "getAudioIdsBySource",
                {
                    "source": "playlist",
                    "entity_id": f"{ownerId}_{playlistId}",
                },
            )).get("audios")

            tracks = await self._parseAPITracks(tracks)

        return tracks if tracks else None

    get_playlist_tracks = getPlaylistTracks