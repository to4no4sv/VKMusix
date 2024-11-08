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
    async def remove(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], playlistId: int = None, groupId: int = None, validateIds: bool = True) -> Union[List[bool], bool]:
        """
        Удаляет треки из музыки или плейлиста пользователя или группы.

        `Пример использования`:

        result = client.remove(
            ownerIds=-2001471901,
            trackIds=123471901,
        )

        print(result)

        :param ownerIds: идентификаторы владельцев треков. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. (``Union[list[int], int]``)
        :param playlistId: идентификатор плейлиста, из которого необходимо удалить треки. Метод не работает для плейлистов, привязанных к чату. (``int``, `optional`)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить треки. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить треки на наличие в музыке или плейлисте. По умолчанию ``True``. Установите на ``False``, если вы получили треки через ``client.getTracks()`` или ``client.getSection()`` (при удалении из музыки) или ``client.getPlaylistTracks()`` (при удалении из плейлиста). (``bool``, `optional`)
        :return: `Если треков несколько`: статусы удаления треков (``list[bool]``). `Если трек один`: статус удаления трека (``bool``). `При успехе`: ``True``. `Если трек не удалось удалить`: ``False``.
        """

        import asyncio

        from itertools import islice

        from vkmusix.errors import AccessDenied

        if type(ownerIds) != type(trackIds):
            self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        elif isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        wasList = isinstance(ownerIds, list)

        if not all((isinstance(ownerIds, list), isinstance(trackIds, list))):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            groupId = await self._getMyId()

        if validateIds:
            if playlistId:
                existTracks = await self.getPlaylistTracks(
                    playlistId,
                    groupId,
                )

                if not existTracks:
                    return [False] * len(ownerIds)

            else:
                sections = await self.getSections(
                    groupId,
                )

                if not sections:
                    return [False] * len(ownerIds)

                subsections = (await sections[0].get()).subsections

                existTracks = await subsections[0].getTracks()

                if not existTracks:
                    return [False] * len(ownerIds)

                existOwnerIds = [track.ownerId for track in existTracks]
                existTrackIds = [track.trackId for track in existTracks]

                batchSize = 343
                tasks = [
                    self.get(
                        existOwnerIds[i:i + batchSize],
                        existTrackIds[i:i + batchSize]
                    )
                    for i in range(0, len(existTracks), batchSize)
                ]

                batches = await asyncio.gather(*tasks)

                existTracks = [
                    track
                    for batch in batches if batch
                    for track in batch
                ]

            for idx, (ownerId, trackId) in enumerate(zip(ownerIds, trackIds)):
                track = await self.get(ownerId, trackId)

                trackFullTitle = track.fullTitle
                trackArtists = str(track.artists) or track.artist

                for existTrack in existTracks:
                    existTrackFullTitle = existTrack.fullTitle
                    existTrackArtists = str(existTrack.artists) or existTrack.artist

                    if existTrackFullTitle == trackFullTitle and existTrackArtists == trackArtists:
                        ownerIds[idx] = existTrack.ownerId
                        trackIds[idx] = existTrack.trackId
                        break

        results = list()

        if playlistId:
            def chunks(iterable):
                iterator = iter(iterable)
                for first in iterator:
                    yield [first] + list(islice(iterator, 99))

            for trackChunk in chunks(zip(ownerIds, trackIds)):
                ids = ",".join(
                    f"{ownerId}_{trackId}"
                    for ownerId, trackId in trackChunk
                )

                try:
                    response = await self._req(
                        "removeFromPlaylist",
                        {
                            "owner_id": groupId,
                            "audio_ids": ids,
                            "playlist_id": playlistId,
                        },
                    )

                    results.append([bool(response)] * len(trackChunk))

                except AccessDenied:
                    results.extend([False] * len(trackChunk))

        else:
            for ownerId, trackId in zip(ownerIds, trackIds):
                try:
                    response = await self._req(
                        "delete",
                        {
                            "owner_id": ownerId,
                            "audio_id": trackId,
                            "group_id": groupId,
                        },
                    )
                    results.append(bool(response))

                except AccessDenied:
                    results.append(False)

        return results if wasList else results[0]