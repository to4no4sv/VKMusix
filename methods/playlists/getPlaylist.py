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
    from vkmusix.aio import asyncFunction
    from vkmusix.types import Playlist

    @asyncFunction
    async def getPlaylist(self, playlistId: int, ownerId: int, includeTracks: bool = False) -> Playlist:
        """
        Получает информацию о плейлисте по его идентификатору.

        Пример использования:\n
        result = client.getPlaylist(playlistId=1, ownerId=-215973356, includeTracks=True)\n
        print(result)

        :param playlistId: идентификатор плейлиста, информацию о котором необходимо получить. (int)
        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки плейлиста в ответ. (bool, по умолчанию `False`)
        :return: информация о плейлисте в виде объекта модели `Playlist`.
        """

        from asyncio import gather

        from vkmusix.types import Playlist

        tasks = [self._req("getPlaylistById", {"owner_id": ownerId, "playlist_id": playlistId})]

        if includeTracks:
            tasks.append(self.getPlaylistTracks(playlistId, ownerId))

        responses = await gather(*tasks)

        playlist = responses[0]
        if not playlist:
            self._raiseError("playlistNotFound")

        if includeTracks:
            playlist["tracks"] = responses[1]

        return self._finalizeResponse(playlist, Playlist)