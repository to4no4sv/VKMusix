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
    from typing import Union, List, Tuple

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def add(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], playlistId: int = None, groupId: int = None) -> Union[Tuple[bool], bool]:
        """
        Добавляет аудиотрек в музыку или плейлист пользователя или группы.

        Пример использования:\n
        result = client.add(ownerIds=474499244, trackIds=456638035, playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо добавить. (int или list)
        :param playlistId: идентификатор плейлиста, в который необходимо добавить аудиотрек. (int, необязательно)
        :param groupId: идентификатор группы, в музыку или плейлист которой необходимо добавить аудиотрек. (int, необязательно)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно добавлен(ы), `False` в противном случае.
        """

        if type(ownerIds) != type(trackIds):
            self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        elif isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        if not (isinstance(ownerIds, list) and isinstance(trackIds, list)):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            from vkmusix.utils import getSelfId

            groupId = await getSelfId(self)

        method = "add"
        if playlistId:
            method += "ToPlaylist"

        results = list()
        for ownerId, trackId in zip(ownerIds, trackIds):
            response = await self._req(method, {**({"owner_id": ownerId, "audio_id": trackId, "group_id": groupId} if not playlistId else {"owner_id": groupId, "audio_ids": f"{ownerId}_{trackId}"}), "playlist_id": playlistId})
            results.append(bool(response))

        return results[0] if len(results) == 0 else tuple(results)