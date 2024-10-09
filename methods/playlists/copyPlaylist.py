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

class CopyPlaylist:
    from typing import Union

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Playlist

    @asyncFunction
    async def copyPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None, chatId: int = None, newTitle: Union[str, None] = str(), newDescription: Union[str, None] = str(), newPhoto: Union[str, None] = str()) -> Union[Playlist, None]:
        """
        Копирует плейлист, принадлежий пользователю или группе в музыку пользователя или группы.

        Пример использования:\n
        result = client.copyPlaylist(playlistId=1, ownerId=-215973356, groupId="yourGroupId", newTitle=None, newDescription=None, newPhoto=None)\n
        print(result)

        :param playlistId: идентификатор плейлиста, который необходимо скопировать. (int)
        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param groupId: идентификатор группы, в которую необходимо скопировать плейлист. (int, необязательно)
        :param chatId: идентификатор чата, к которому небходимо привязать плейлист. (int, формат: `2000000000 + идентификатор чата`, необязательно)
        :param newTitle: новое название плейлиста, `None` для использования текущих даты и времени. (str или None, по умолчанию оригинальное название)
        :param newDescription: новое описание плейлиста, `None` для удаления описания. (str или None, по умолчанию оригинальное описание)
        :param newPhoto: новая обложка плейлиста, `None` для удаления обложки. (str или None, по умолчанию оригинальная обложка)
        :return: скопированный плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id`, `url` и `own`, если плейлист успешно скопирован, `None` в противном случае.
        """

        from datetime import datetime

        from vkmusix.config import utcTz, moscowTz

        if not ownerId:
            from vkmusix.utils import getSelfId

            ownerId = await getSelfId(self)

        playlist = await self.getPlaylist(playlistId, ownerId, True)

        title = playlist.title
        description = playlist.description
        photo = playlist.photo

        if newTitle != str():
            title = newTitle if newTitle is not None else datetime.utcnow().replace(tzinfo=utcTz).astimezone(moscowTz).strftime("%d.%m.%Y / %H:%M:%S")

        if newDescription != str():
            description = newDescription

        if newPhoto != str():
            photo = None

        elif photo:
            _, photo = photo.popitem()

        newPlaylist = await self.createPlaylist(title, description, photo, groupId, chatId)

        tracks = playlist.tracks
        if tracks:
            ownerIds, trackIds = zip(*[(track.ownerId, track.trackId) for track in tracks[::-1]])
            await newPlaylist.addTrack(list(ownerIds), list(trackIds))

        return newPlaylist