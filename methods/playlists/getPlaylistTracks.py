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
    async def getPlaylistTracks(self, playlistId: int, ownerId: int = None) -> Union[List[Track], None]:
        """
        Получает треки плейлиста или альбома.

        `Пример использования`:

        tracks = client.getPlaylistTracks(
            ownerId=-2000201020,
            albumId=19201020,
        )

        print(tracks)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :return: `При успехе`: треки плейлиста или альбома (``list[types.Track]``). `Если плейлист или альбом не найден или треки отсутствуют`: ``None``.
        """

        from vkmusix.config import VK, headers
        from vkmusix.types import Track

        if not ownerId:
            ownerId = await self._getMyId()

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

        tracks = await self._getTracks(tracks.text)

        if not tracks:
            tracks = (await self._req(
                "getAudioIdsBySource",
                {
                    "playlist_id": f"{ownerId}_{playlistId}",
                },
                version=5.195,
            )).get("audios")

            if tracks:
                for index, id in enumerate(tracks):
                    if id.count("_") == 3:
                        id = id[:id.rfind("_")]

                    ownerId, trackId = id.split("_")[:2]
                    tracks[index] = {
                        "owner_id": int(ownerId),
                        "track_id": int(trackId),
                    }

                return self._finalizeResponse(tracks, Track)

        return tracks if tracks else None

    get_playlist_tracks = getPlaylistTracks