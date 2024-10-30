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
    async def add(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], playlistId: int = None, groupId: int = None) -> List[bool]:
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
        :return: Статусы добавления треков (``list[bool]``). `При успехе`: ``True``. `Если трек не удалось добавить`: ``False``.
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

        method = "add"
        if playlistId:
            method += "ToPlaylist"

        results = list()
        for ownerId, trackId in zip(ownerIds, trackIds):
            response = await self._req(
                method,
                {
                    **(
                        {
                            "owner_id": ownerId,
                            "audio_id": trackId,
                            "group_id": groupId,
                        }
                        if not playlistId else
                        {
                            "owner_id": groupId,
                            "audio_ids": f"{ownerId}_{trackId}",
                        }
                    ),
                    "playlist_id": playlistId,
                },
            )

            results.append(bool(response))

        return results