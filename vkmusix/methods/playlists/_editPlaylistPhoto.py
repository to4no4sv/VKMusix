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

class _EditPlaylistPhoto:
    from typing import Union

    async def _editPlaylistPhoto(self, playlistId: int, photo: Union[str, None] = str(), groupId: int = None) -> bool:
        if photo == str():
            return False

        if not groupId:
            groupId = await self._getMyId()

        params = {
            "playlist_id": playlistId,
            "owner_id": groupId,
        }

        if photo is None:
            method = "deletePlaylistCoverPhoto"

        else:
            raise NotImplementedError

            method = "setPlaylistCoverPhoto"
            params = {
                **params,
                **{
                    "photo": photo,
                },
            }

        response = await self._req(method, params)

        return bool(response)