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

class Add:
    from typing import Union, List

    from vkmusix.aio import async_

    @async_
    async def add(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], playlistId: int = None, groupId: int = None) -> Union[List[bool], bool]:
        """
        Добавляет треки в музыку или плейлист пользователя или группы.

        `Пример использования`:

        result = client.add(
            ownerIds=-2001471901,
            trackIds=123471901,
        )

        print(result)

        :param ownerIds: идентификаторы владельцев треков. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. (``Union[list[int], int]``)
        :param playlistId: идентификатор плейлиста, в который необходимо добавить треки. (``int``, `optional`)
        :param groupId: идентификатор группы, в музыку или плейлист которой необходимо добавить треки. (``int``, `optional`)
        :return: `Если треков несколько`: статусы добавления треков (``list[bool]``). `Если трек один`: статус добавления трека (``bool``). `При успехе`: ``True``. `Если трек не удалось добавить`: ``False``.
        """

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

        method = "add"
        if playlistId:
            method += "ToPlaylist"

        results = list()

        if playlistId:
            def chunks(iterable):
                iterator = iter(iterable)
                for first in iterator:
                    yield [first] + list(islice(iterator, 49))

            for trackChunk in chunks(zip(ownerIds, trackIds)):
                ids = ",".join(
                    f"{ownerId}_{trackId}"
                    for ownerId, trackId in trackChunk
                )

                try:
                    response = await self._req(
                        method,
                        {
                            "owner_id": groupId,
                            "audio_ids": ids,
                            "playlist_id": playlistId,
                        },
                    )

                    results.append([bool(response)] * len(trackChunk))

                except AccessDenied:
                    print(1)
                    results.extend([False] * len(trackChunk))

        else:
            for ownerId, trackId in zip(ownerIds, trackIds):
                try:
                    response = await self._req(
                        method,
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