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
    from typing import Union, List, Tuple

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def remove(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], playlistId: int = None, groupId: int = None, reValidateIds: bool = True) -> Union[Tuple[bool], bool]:
        """
        Удаляет аудиотрек из музыки или плейлиста пользователя или группы.

        Пример использования:\n
        result = client.remove(ownerIds=474499244, trackIds=456638035, playlistId="yourPlaylistId", groupId="yourGroupId", reValidateIds=False)\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо удалить. (int или list)
        :param playlistId: идентификатор плейлиста, из которого необходимо удалить аудиотрек(и). (int, необязательно, метод временно не работает для плейлистов, привязанных к чату)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить аудиотрек(и). (int, необязательно)
        :param reValidateIds: флаг, указывающий, необходимо ли перепроверить идентификатор(ы) аудитрека(ов) по находящимся в плейлисте. (bool, по умолчанию `True`)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно удалён(ы), `False` в противном случае.
        """

        if type(ownerIds) != type(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        elif isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        if not (isinstance(ownerIds, list) and isinstance(trackIds, list)):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            from vkmusix.utils import getSelfId

            groupId = await getSelfId(self)

        if reValidateIds:
            if playlistId:
                existTracks = await self.getPlaylistTracks(playlistId, groupId)

            else:
                existTracks = await self.getTracks(groupId)

            if not existTracks and playlistId:
                return (False,)

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
                    response = await self._req("removeFromPlaylist", {"audio_ids": id, "owner_id": groupId, "playlist_id": playlistId})
                    return bool(response)

            tasks = [removeTrackFromPlaylist(f"{ownerId}_{trackId}", deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        else:
            async def removeTrack(ownerId: int, trackId: int, semaphore: Semaphore) -> bool:
                async with semaphore:
                    response = await self._req("delete", {"owner_id": ownerId, "audio_id": trackId, "group_id": groupId})
                    return bool(response)

            tasks = [removeTrack(ownerId, trackId, deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        results = await gather(*tasks)

        return results[0] if len(results) == 1 else tuple(results)