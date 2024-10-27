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
        streams (int, optional): количество прослушиваний плейлиста.\n
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
        import html

        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        super().__init__(client)

        title = playlist.get("title")
        self.title = html.unescape(title) if title else None

        subtitle = playlist.get("subtitle")
        self.subtitle = html.unescape(subtitle.replace("\n", " ")) if subtitle else None

        self.fullTitle = f"{self.title} ({self.subtitle})".replace("((", "(").replace("))", ")").replace("([", "(").replace("])", ")") if self.subtitle else self.title

        description = playlist.get("description")
        self.description = description if description else None

        streams = playlist.get("plays")
        self.streams = streams if streams else None

        saves = playlist.get("followers")
        self.saves = saves if saves else None

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
        self.url = f"{VK}music/playlist/{self.id}"

        self.own = isOwn

        self.raw = playlist


    @asyncFunction
    async def get(self, includeTracks: bool = False) -> "Playlist":
        """
        Получает информацию о плейлисте по его идентификатору.

        Пример использования:\n
        result = playlist.get(includeTracks=True)\n
        print(result)

        :param includeTracks: флаг, указывающий, необходимо ли включать треки плейлиста в ответ. (bool, по умолчанию `False`)
        :return: информация о плейлисте в виде объекта модели `Playlist`.
        """

        return await self._client.getPlaylist(self.playlistId, self.ownerId, includeTracks)


    @asyncFunction
    async def getTracks(self) -> Union[List[Track], Track, None]:
        return await self._client.getPlaylistTracks(self.playlistId, self.ownerId)


    @asyncFunction
    async def add(self, groupId: int = None) -> Union["Playlist", None]:
        """
        Добавляет плейлист в музыку пользователя или группы.

        Пример использования:\n
        result = playlist.add(groupId="yourGroupId")\n
        print(result)

        :param groupId: идентификатор группы, в которую необходимо добавить плейлист. (int, необязательно)
        :return: добавленный плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id`, `url` и `own`, если плейлист успешно добавлен, `None` в противном случае.
        """

        return await self._client.addPlaylist(self.playlistId, self.ownerId, groupId)


    @asyncFunction
    async def remove(self) -> bool:
        """
        Удаляет плейлист из музыки пользователя или группы.

        Пример использования:\n
        result = playlist.remove()\n
        print(result)

        :return: `True`, если плейлист успешно удалён, `False` в противном случае.
        """

        return await self._client.removePlaylist(self.playlistId, self.ownerId)


    @asyncFunction
    async def edit(self, title: Union[str, int] = None, description: Union[str, int] = None, photo: str = None) -> bool:
        """
        Изменяет информацию плейлиста, принадлежащего пользователю или группе.

        Пример использования:\n
        result = playlist.edit(title="prombl — npc", description="Release Date: December 24, 2021", photo="yourPhotoFilename")\n
        print(result)

        :param title: новое название плейлиста. (Необязательно)
        :param description: новое описание плейлиста. (Необязательно)
        :param photo: новое фото плейлиста. (Необязательно)
        :return: `True`, если информация плейлиста успешно обновлена, `False` в противном случае.
        """

        return await self._client.editPlaylist(self.playlistId, title, description, photo, self.ownerId)


    @asyncFunction
    async def copy(self, groupId: int = None, chatId: int = None, newTitle: Union[str, None] = str(), newDescription: Union[str, None] = str(), newPhoto: Union[str, None] = str()) -> Union["Playlist", None]:
        """
        Копирует плейлист, принадлежий пользователю или группе в музыку пользователя или группы.

        Пример использования:\n
        result = playlist.copy(groupId="yourGroupId", chatId="yourChatId", newTitle=None, newDescription=None, newPhoto=None)\n
        print(result)

        :param groupId: идентификатор группы, в которую необходимо скопировать плейлист. (int, необязательно)
        :param chatId: идентификатор чата, к которому небходимо привязать плейлист. (int, формат: `2000000000 + идентификатор чата`, необязательно)
        :param newTitle: новое название плейлиста, `None` для использования текущих даты и времени. (str или None, по умолчанию оригинальное название)
        :param newDescription: новое описание плейлиста, `None` для удаления описания. (str или None, по умолчанию оригинальное описание)
        :param newPhoto: новая обложка плейлиста, `None` для удаления обложки. (str или None, по умолчанию оригинальная обложка)
        :return: скопированный плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id`, `url` и `own`, если плейлист успешно скопирован, `None` в противном случае.
        """

        return await self._client.copyPlaylist(self.playlistId, self.ownerId, groupId, chatId, newTitle, newDescription, newPhoto)


    @asyncFunction
    async def addTracks(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]]) -> Union[Tuple[bool], bool]:
        """
        Добавляет аудиотрек в плейлист пользователя или группы.

        Пример использования:\n
        result = playlist.addTrack(ownerIds=474499244, trackIds=456638035)\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо добавить. (int или list)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно добавлен(ы), `False` в противном случае.
        """

        return await self._client.add(ownerIds, trackIds, self.playlistId, self.ownerId)


    @asyncFunction
    async def removeTracks(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], reValidateIds: bool = True) -> Union[Tuple[bool], bool]:
        """
        Удаляет аудиотрек из плейлиста пользователя или группы.

        Пример использования:\n
        result = playlist.removeTracks(ownerIds=474499244, trackIds=456638035, reValidateIds=False)\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо удалить. (int или list)
        :param reValidateIds: флаг, указывающий, необходимо ли перепроверить идентификатор(ы) аудитрека(ов) по находящимся в плейлисте. (bool, по умолчанию `True`)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно удалён(ы), `False` в противном случае.
        """

        return await self._client.remove(ownerIds, trackIds, self.playlistId, self.ownerId, reValidateIds)
