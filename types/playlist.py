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

from .base import Base

class Playlist(Base):
    """
    Класс, представляющий плейлист.

    Атрибуты:
        title (str): название плейлиста.\n
        subtitle (str, optional): подзаголовок плейлиста, если он присутствует.\n
        description (str, optional): описание плейлиста, если оно присутствует.\n
        plays (int, optional): количество прослушиваний плейлиста.\n
        createdAt (datetime, optional): дата и время создания плейлиста (UTC +03:00).\n
        updatedAt (datetime, optional): дата и время последнего добавления (удаления) аудиотрека в (из) плейлист(а) (UTC +03:00).\n
        photo (dict, optional): словарь с размерами и URL фотографий плейлиста, отсортированный по размеру.\n
        tracks (list[Track], optional): список аудиотреков плейлиста, где каждый аудиотрек представлен объектом класса `Track`.\n
        ownerId (str): идентификатор владельца плейлиста.\n
        playlistId (str): идентификатор плейлиста.\n
        id (str): комбинированный идентификатор в формате `ownerId_playlistId`.\n
        url (str): URL страницы плейлиста.
    """

    from typing import Union, List, Tuple

    from vkmusix.aio import asyncFunction
    from vkmusix.types.track import Track

    def __init__(self, playlist: dict, isOwn: bool = False, client: "Client" = None) -> None:
        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        super().__init__(client)

        title = playlist.get("title")
        self.title = title if title else None

        subtitle = playlist.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        description = playlist.get("description")
        self.description = description if description else None

        plays = playlist.get("plays")
        self.plays = plays if plays else None

        followers = playlist.get("followers")
        self.followers = followers if followers else None

        createdAt = playlist.get("create_time")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None

        updatedAt = playlist.get("update_time")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        photo = playlist.get("photo")
        if not photo:
            photo = playlist.get("thumb")
        self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        original = playlist.get("original")
        self.original = Playlist(original, client=self._client) if original else None

        trackCount = playlist.get("count")
        self.trackCount = trackCount if trackCount else None

        tracks = playlist.get("tracks")
        self.tracks = tracks if tracks else None

        self.ownerId = playlist.get("owner_id")
        self.playlistId = playlist.get("id") or playlist.get("playlist_id")
        self.id = f"{self.ownerId}_{self.playlistId}"
        self.url = VK + "music/playlist/" + self.id

        self.own = isOwn


    @asyncFunction
    async def get(self, includeTracks: bool = False) -> "Playlist":
        return await self._client.getPlaylist(self.playlistId, self.ownerId, includeTracks)


    @asyncFunction
    async def getTracks(self) -> Union[List[Track], Track, None]:
        return await self._client.getPlaylistTracks(self.playlistId, self.ownerId)


    @asyncFunction
    async def add(self, groupId: int = None) -> Union["Playlist", None]:
        return await self._client.addPlaylist(self.playlistId, self.ownerId, groupId)


    @asyncFunction
    async def remove(self, groupId: int = None) -> bool:
        return await self._client.removePlaylist(self.playlistId, groupId)


    @asyncFunction
    async def edit(self, title: Union[str, int] = None, description: Union[str, int] = None, photo: str = None, groupId: int = None) -> bool:
        return await self._client.editPlaylist(self.playlistId, title, description, photo, groupId)


    @asyncFunction
    async def copy(self, groupId: int = None, chatId: int = None, newTitle: Union[str, None] = str(), newDescription: Union[str, None] = str(), newPhoto: Union[str, None] = str()) -> Union["Playlist", None]:
        return await self._client.copyPlaylist(self.playlistId, self.ownerId, groupId, chatId, newTitle, newDescription, newPhoto)


    @asyncFunction
    async def addTrack(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]]) -> Union[Tuple[bool], bool]:
        return await self._client.add(ownerIds, trackIds, self.playlistId, self.ownerId)


    @asyncFunction
    async def removeTrack(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], reValidateIds: bool = True) -> Union[Tuple[bool], bool]:
        return await self._client.remove(ownerIds, trackIds, self.playlistId, self.ownerId, reValidateIds)