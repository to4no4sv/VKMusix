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

    from vkmusix.aio import async_
    from vkmusix.types import Playlist

    @async_
    async def copyPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None, chatId: int = None, title: Union[str, None] = str(), description: Union[str, None] = str(), photo: Union[str, None] = str()) -> Union[Playlist, None]:
        """
        Копирует плейлист или альбом в музыку пользователя или группы.

        `Пример использования`:

        playlist = client.copyPlaylist(
            playlistId=19201020,
            ownerId=-2000201020,
        )

        print(playlist)

        :param playlistId: идентификатор плейлиста или альбома. (``int``)
        :param ownerId: идентификатор владельца плейлиста или альбома (пользователь или группа). (``int``, `optional`)
        :param groupId: идентификатор группы, в которую необходимо скопировать плейлист или альбом. (``int``, `optional`)
        :param chatId: идентификатор чата, к которому необходимо привязать скопированный плейлист или альбом. (``int``, `optional`)
        :param title: название плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param description: описание плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param photo: ссылка на фото плейлиста. ``None`` для удаления. Не для удаления не работает. (``Union[str, None]``, `optional`)
        :return: `При успехе`: информация о скопированном плейлисте или альбоме (``Union[types.Playlist, types.Album]``). `Если плейлист или альбом не найден`: ``None``.
        """

        from datetime import datetime

        if not ownerId:
            ownerId = await self._getMyId()

        playlist = await self.getPlaylist(playlistId, ownerId)

        title_ = playlist.title
        description_ = playlist.description
        photo_ = playlist.photo

        if title != str():
            title_ = title if title is not None else datetime.utcnow().strftime("%d.%m.%Y / %H:%M:%S")

        if description != str():
            description_ = description

        if photo != str():
            photo_ = None if True else photo

        elif photo_:
            _, photo_ = photo_.popitem()

        newPlaylist = await self.createPlaylist(
            title_,
            description_,
            photo_,
            groupId,
            chatId,
        )

        tracks = await playlist.getTracks(True)
        if tracks:
            ownerIds, trackIds = zip(*[(track.ownerId, track.trackId) for track in tracks[::-1]])
            await newPlaylist.addTracks(list(ownerIds), list(trackIds))

        return newPlaylist

    copy_playlist = copyPlaylist