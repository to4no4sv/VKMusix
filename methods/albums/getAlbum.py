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

class GetAlbum:
    from vkmusix.aio import asyncFunction
    from vkmusix.types import Album

    @asyncFunction
    async def getAlbum(self, ownerId: int, albumId: int, includeTracks: bool = False) -> Album:
        """
        Получает информацию об альбоме по его идентификатору.

        Пример использования:\n
        result = client.getAlbum(ownerId=-2000837600, albumId=16837600, includeTracks=True)\n
        print(result)

        :param ownerId: идентификатор владельца альбома (пользователь или группа). (int)
        :param albumId: идентификатор альбома, информацию о котором необходимо получить. (int)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки альбома в ответ. (bool, по умолчанию `False`)
        :return: информация об альбоме в виде объекта модели `Album`.
        """

        from asyncio import gather

        from vkmusix.types import Album

        tasks = [self._req("getPlaylistById", {"owner_id": ownerId, "playlist_id": albumId})]

        if includeTracks:
            tasks.append(self.getAlbumTracks(ownerId, albumId))

        responses = await gather(*tasks)

        album = responses[0]
        if not album:
            self._raiseError("albumNotFound")

        if includeTracks:
            album["tracks"] = responses[1]

        return self._finalizeResponse(album, Album)