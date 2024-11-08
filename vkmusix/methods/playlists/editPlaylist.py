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

class EditPlaylist:
    from typing import Union

    from vkmusix.aio import async_

    @async_
    async def editPlaylist(self, playlistId: int, title: str = None, description: Union[str, None] = str(), photo: Union[str, None] = str(), groupId: int = None) -> bool:
        """
        Изменяет информацию о плейлисте.

        `Пример использования`:

        result = client.editPlaylist(
            playlistId=19201020,
            title="Лучшая музыка в машину!!!",
        )

        print(result)

        :param playlistId: идентификатор плейлиста. (``int``)
        :param title: название плейлиста. (``str``, `optional`)
        :param description: описание плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param photo: ссылка на фото плейлиста. ``None`` для удаления. Не для удаления не работает. (``Union[str, None]``, `optional`)
        :param groupId: идентификатор группы, в которой находится плейлист. (``int``, `optional`)
        :return: `При успехе`: ``True``. `Если информацию о плейлисте не удалось изменить`: ``False``.
        """

        if not any((title, description is not None, photo is not None)):
            return False

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        params = {
            "playlist_id": playlistId,
            "owner_id": groupId,
            **({"title": title} if title else dict()),
            **({"description": description} if description != str() else dict())
        }

        if any(("title" in params, "description" in params)):
            response = await self._req("editPlaylist", params)
            editInfoStatus = bool(response)

        else:
            editInfoStatus = None

        if any((editInfoStatus is True, editInfoStatus is None)) and photo != str():
            editPhotoStatus = await self._editPlaylistPhoto(playlistId, photo, groupId)
            if editInfoStatus is None:
                editInfoStatus = editPhotoStatus

        return editInfoStatus

    edit_playlist = editPlaylist