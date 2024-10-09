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

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def editPlaylist(self, playlistId: int, title: Union[str, int] = None, description: Union[str, int] = None, photo: str = None, groupId: int = None) -> bool:
        """
        Изменяет информацию плейлиста, принадлежащего пользователю или группе.

        Пример использования:\n
        result = client.editPlaylist(playlistId="yourPlaylistId", title="prombl — npc", description="Release Date: December 24, 2021", photo="yourPhotoFilename", groupId="yourGroupId")\n
        print(result)

        :param playlistId: идентификатор плейлиста, информацию которого необходимо изменить.
        :param title: новое название плейлиста. (Необязательно)
        :param description: новое описание плейлиста. (Необязательно)
        :param photo: новое фото плейлиста. (Необязательно)
        :param groupId: идентификатор группы, в которой находится плейлист. (Необязательно)
        :return: `True`, если информация плейлиста успешно обновлена, `False` в противном случае.
        """

        if not any((title, description is not None, photo is not None)):
            return False

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        params = {
            "playlist_id": playlistId,
            "owner_id": groupId,
            **({"title": title} if title else {}),
            **({"description": description} if description is not None else {})
        }

        if not any(("title" in params, "description" in params, photo is not None)):
            return False

        else:
            if any(("title" in params, "description" in params)):
                response = await self._req("editPlaylist", params)
                editInfoStatus = bool(response)

            else:
                editInfoStatus = None

        if any((editInfoStatus is True, editInfoStatus is None)) and photo is not None:
            editPhotoStatus = await self._editPlaylistPhoto(playlistId, photo, groupId)
            if editInfoStatus is None:
                editInfoStatus = editPhotoStatus

        return editInfoStatus