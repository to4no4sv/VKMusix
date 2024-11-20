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
        title (str): название плейлиста.

        subtitle (str, optional): подзаголовок плейлиста, во ВКонтакте отображается серым цветом справа от названия.

        fullTitle (str): полное название плейлиста в формате {title} ({subtitle}).

        description (str, optional): описание плейлиста.

        streams (int): количество прослушиваний плейлиста.

        saves (int): количество сохранений плейлиста пользователями или группами в свою музыку.

        createdAt (datetime): дата и время создания плейлиста.

        updatedAt (datetime): дата и время обновления плейлиста.

        mainColor (str, optional): ???.

        photo (dict, optional): словарь с ссылками на различные размеры обложки плейлиста, отсортированные по возрастанию.

        original (types.Playlist, optional): оригинальный плейлист, если это не созданный, а сохранённый пользователем или группой в свою музыку.

        trackCount (int): количество треков в плейлисте.

        tracks (list[types.Track, optional): треки плейлиста. Доступны при получении через client.getPlaylist(includeTracks=True).

        own (bool, optional): флаг, указывающий, является ли плейлист созданным этим пользователем или группой. Доступен только при получении через client.getPlaylists() или client.getAllPlaylists().

        ownerId (int): идентификатор владельца плейлиста (пользователь или группа).

        playlistId (int): идентификатор плейлиста.

        id (str): полный идентификатор плейлиста в формате {ownerId}_{playlistId}.

        url (str): ссылка на плейлист в формате https://vk.com/music/playlist/{id}.

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types.track import Track

    def __init__(self, playlist: dict, isOwn: bool = None, client: "Client" = None) -> None:
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

        self.streams = playlist.get("plays")
        self.saves = playlist.get("followers")

        self.createdAt = unixToDatetime(playlist.get("create_time"))
        self.updatedAt = unixToDatetime(playlist.get("update_time"))

        photo = playlist.get("photo")
        if not photo:
            photo = playlist.get("thumb")
        self.photo = {int(key.split("_")[1]): value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        self.original = self._client._finalizeResponse(
            playlist.get("original"),
            Playlist,
        )

        tracks = playlist.get("tracks")
        self.trackCount = playlist.get("count") or (len(tracks) if tracks else None)
        self.tracks = tracks

        self.own = isOwn

        self.ownerId = playlist.get("owner_id")
        self.playlistId = playlist.get("id") or playlist.get("playlist_id")
        self.id = f"{self.ownerId}_{self.playlistId}"
        self.url = f"{VK}music/playlist/{self.id}"

        self.raw = playlist


    @async_
    async def get(self, includeTracks: bool = False) -> Union["Playlist", None]:
        """
        Получает информацию о плейлисте.

        `Пример использования`:

        playlist = playlist.get(
            includeTracks=True,
        )

        print(playlist)

        :param includeTracks: флаг, указывающий, небходимо ли также получить треки. (``bool``, `optional`)
        :return: `При успехе`: информация о плейлисте (``types.Playlist``). `Если плейлист не найден`: ``None``.
        """

        return await self._client.getPlaylist(
            self.playlistId,
            self.ownerId,
            includeTracks,
        )


    @async_
    async def getTracks(self, isLarge: bool = False) -> Union[List[Track], None]:
        """
        Получает треки плейлиста.

        `Пример использования`:

        tracks = playlist.getTracks()

        print(tracks)

        :param isLarge: флаг, указывающий, содержит ли плейлист более 1000 треков. По умолчанию ``False``. Если ``True``, будет получена ограниченная информация о всех треках, если ``False`` — только последние 1000 треков, но с полной информацией. Установите ``None``, чтобы библиотека определила автоматически. Игнорируется для приватных плейлистов. (``bool``, `optional`)
        :return: `При успехе`: треки плейлиста (``list[types.Track]``). `Если плейлист не найден или треки отсутствуют`: ``None``.
        """

        return await self._client.getPlaylistTracks(
            self.playlistId,
            self.ownerId,
            isLarge,
        )

    get_tracks = getTracks


    @async_
    async def add(self, groupId: int = None) -> Union["Playlist", None]:
        """
        Добавляет плейлист в музыку пользователя или группы.

        `Пример использования`:

        playlist = playlist.add()

        print(playlist)

        :param groupId: идентификатор группы, в которую необходимо добавить плейлист. (``int``, `optional`)
        :return: `При успехе`: информация о добавленном плейлисте (``types.Playlist``). `Если плейлист не найден`: ``None``.
        """

        return await self._client.addPlaylist(
            self.playlistId,
            self.ownerId,
            groupId,
        )


    @async_
    async def remove(self, groupId: int = None, validateIds: bool = True) -> bool:
        """
        Удаляет плейлист из музыки пользователя или группы.

        `Пример использования`:

        result = playlist.remove()

        print(result)

        :param groupId: идентификатор группы, из которой необходимо удалить плейлист. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить плейлист на наличие в музыке. По умолчанию ``True``. Установите на ``False``, если вы получили плейлист через ``client.getPlaylists()`` или ``client.getAllPlaylists()``. (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если плейлист не найден или не получилось его удалить`: ``False``.
        """

        return await self._client.removePlaylist(
            self.playlistId,
            self.ownerId,
            groupId,
            validateIds,
        )


    @async_
    async def edit(self, title: str = None, description: Union[str, None] = str(), photo: Union[str, None] = str()) -> bool:
        """
        Изменяет информацию о плейлисте.

        `Пример использования`:

        result = playlist.edit(
            title="Лучшая музыка в машину!!!",
        )

        print(result)

        :param title: название плейлиста. (``str``, `optional`)
        :param description: описание плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param photo: ссылка на фото плейлиста. ``None`` для удаления. Не для удаления не работает. (``Union[str, None]``, `optional`)
        :return: `При успехе`: ``True``. `Если информацию о плейлисте не удалось изменить`: ``False``.
        """

        return await self._client.editPlaylist(
            self.playlistId,
            title,
            description,
            photo,
            self.ownerId,
        )


    @async_
    async def copy(self, groupId: int = None, chatId: int = None, title: Union[str, None] = str(), description: Union[str, None] = str(), photo: Union[str, None] = str()) -> Union["Playlist", None]:
        """
        Копирует плейлист в музыку пользователя или группы.

        `Пример использования`:

        playlist = playlist.copy()

        print(playlist)

        :param groupId: идентификатор группы, в которую необходимо скопировать плейлист. (``int``, `optional`)
        :param chatId: идентификатор чата, к которому необходимо привязать скопированный плейлист. (``int``, `optional`)
        :param title: название плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param description: описание плейлиста. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param photo: ссылка на фото плейлиста. ``None`` для удаления. Не для удаления не работает. (``Union[str, None]``, `optional`)
        :return: `При успехе`: информация о скопированном плейлисте (``types.Playlist``). `Если плейлист не найден`: ``None``.
        """

        return await self._client.copyPlaylist(
            self.playlistId,
            self.ownerId,
            groupId,
            chatId,
            title,
            description,
            photo,
        )


    @async_
    async def addTracks(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int]) -> Union[List[bool], bool]:
        """
        Добавляет треки в плейлист пользователя или группы.

        `Пример использования`:

        result = playlist.addTracks(
            ownerIds=-2001471901,
            trackIds=123471901,
        )

        print(result)

        :param ownerIds: идентификаторы владельцев треков. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. (``Union[list[int], int]``)
        :return: `Если треков несколько`: статусы добавления треков (``list[bool]``). `Если трек один`: статус добавления трека (``bool``). `При успехе`: ``True``. `Если трек не удалось добавить`: ``False``.
        """

        return await self._client.add(
            ownerIds,
            trackIds,
            self.playlistId,
            self.ownerId,
        )

    add_tracks = addTracks


    @async_
    async def removeTracks(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], validateIds: bool = True) -> Union[List[bool], bool]:
        """
        Удаляет треки из плейлиста пользователя или группы.

        `Пример использования`:

        result = playlist.removeTracks(
            ownerIds=-2001471901,
            trackIds=123471901,
        )

        print(result)

        :param ownerIds: идентификаторы владельцев треков. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. (``Union[list[int], int]``)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить треки на наличие в плейлисте. По умолчанию ``True``. Установите на ``False``, если вы получили треки через ``client.getPlaylistTracks()``. (``bool``, `optional`)
        :return: `Если треков несколько`: статусы удаления треков (``list[bool]``). `Если трек один`: статус удаления трека (``bool``). `При успехе`: ``True``. `Если трек не удалось удалить`: ``False``.
        """

        return await self._client.remove(
            ownerIds,
            trackIds,
            self.playlistId,
            self.ownerId,
            validateIds,
        )

    remove_tracks = removeTracks


    @async_
    async def removeAllTracks(self) -> bool:
        """
        Удаляет все треки из плейлиста пользователя или группы.

        `Пример использования`:

        result = playlist.removeAllTracks(
            playlistId=19201020,
        )

        print(result)

        :return: `При успехе`: ``True``. `Если плейлист не найден, треки отсутствуют или их не удалось удалить`: ``False``.
        """

        return await self._client.removeAllTracksFromPlaylist(
            self.playlistId,
            self.ownerId,
        )

    remove_all_tracks = removeAllTracks