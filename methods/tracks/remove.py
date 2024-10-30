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

class Remove:
    from typing import Union, List

    from vkmusix.aio import async_

    @async_
    async def remove(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], playlistId: int = None, groupId: int = None, validateIds: bool = True) -> List[bool]:
        """
        Удаляет треки из музыки или плейлиста пользователя или группы.

        `Пример использования`:

        result = client.remove(
            ownerIds=-2001471901,
            trackIds=123471901,
        )

        print(result)

        :param ownerIds: идентификатор владельца треков. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. (``Union[list[int], int]``)
        :param playlistId: идентификатор плейлиста, из которого необходимо удалить треки. Метод не работает для плейлистов, привязанных к чату (``int``, `optional`)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить треки. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить треки на наличие в музыке или плейлисте. По умолчанию ``True``. Установите на ``False``, если вы получили треки через ``client.getTracks()`` (при удалении из музыки) или ``client.getPlaylistTracks()`` (при удалении из плейлиста). (``bool``, `optional`)
        :return: Статусы удаления треков (``list[bool]``). `При успехе`: ``True``. `Если трек не удалось удалить`: ``False``.
        """

        if type(ownerIds) != type(trackIds):
            self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        elif isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        if not all((isinstance(ownerIds, list), isinstance(trackIds, list))):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            groupId = await self._getMyId()

        if validateIds and playlistId: # and playlistId временно
            if playlistId:
                existTracks = await self.getPlaylistTracks(playlistId, groupId)

            else:
                existTracks = NotImplemented

            if not existTracks and playlistId:
                return [False] * len(ownerIds)

            for index, (ownerId, trackId) in enumerate(zip(ownerIds, trackIds)):
                if not playlistId:
                    continue

                track = await self.get(ownerId, trackId)

                trackTitle = track.title
                trackArtists = track.artists
                if not trackArtists:
                    trackArtists = track.artist

                for existTrack in existTracks:
                    existTrackTitle = existTrack.title
                    existTrackArtists = existTrack.artists
                    if not existTrackArtists:
                        existTrackArtists = existTrack.artist

                    existTrackOwnerId = existTrack.ownerId
                    existTrackId = existTrack.trackId

                    if existTrackTitle == trackTitle and existTrackArtists == trackArtists:
                        ownerIds[index] = existTrackOwnerId
                        trackIds[index] = existTrackId
                        break

        from asyncio import Semaphore, gather

        deleteSemaphore = Semaphore(2)
        if playlistId:
            if groupId > 0:
                groupId = -groupId

            async def removeTrackFromPlaylist(id: str, semaphore: Semaphore) -> bool:
                async with semaphore:
                    response = await self._req(
                        "removeFromPlaylist",
                        {
                            "audio_ids": id,
                            "owner_id": groupId,
                            "playlist_id": playlistId,
                        },
                    )

                    return bool(response)

            tasks = [removeTrackFromPlaylist(f"{ownerId}_{trackId}", deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        else:
            async def removeTrack(ownerId: int, trackId: int, semaphore: Semaphore) -> bool:
                async with semaphore:
                    response = await self._req(
                        "delete",
                        {
                            "owner_id": ownerId,
                            "audio_id": trackId,
                            "group_id": groupId,
                        },
                    )

                    return bool(response)

            tasks = [removeTrack(ownerId, trackId, deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        results = await gather(*tasks)

        return list(results)