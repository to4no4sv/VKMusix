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

class Album(Base):
    """
    Класс, представляющий альбом.

    Атрибуты:
        title (str): название альбома.

        subtitle (str, optional): подзаголовок альбома, во ВКонтакте отображается серым цветом справа от названия.

        artist (str): все артисты альбома в виде строки.

        artists (list[types.Artist]): основные артисты альбома.

        featuredArtists (list[types.Artist], optional): приглашённые артисты альбома.

        description (str, optional): описание альбома.

        releaseYear (int): год выхода альбома.

        genres (list[types.Genre], optional): жанры альбома.

        streams (int): количество прослушиваний альбома.

        saves (int): количество сохранений альбома пользователями или группами в свою музыку.

        uploadedAt (datetime): дата и время загрузки альбома (не релиза).

        updatedAt (datetime): дата и время обновления альбома (не релиза).

        exclusive (bool): флаг, указывающий, является ли альбом выпущенным эксклюзивно во ВКонтакте.

        mainColor (str, optional): ???.

        photo (dict, optional): словарь с ссылками на различные размеры обложки альбома, отсортированные по возрастанию.

        original (types.Album, optional): оригинальный альбом, если это не альбом, а плейлист, сохранённый пользователем или группой в свою музыку.

        trackCount (int): количество треков в альбоме.

        tracks (list[types.Track]): треки альбома. Доступны при получении через client.getPlaylist(includeTracks=True).

        ownerId (int): идентификатор владельца альбома.

        albumId или playlistId (int): идентификатор альбома или плейлиста.

        id (str): полный идентификатор альбома в формате {ownerId}_{albumId or playlistId}.

        url (str): ссылка на альбом в формате https://vk.com/music/album/{id}.

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types.track import Track

    def __init__(self, album: dict, playlist: bool = None, client: "Client" = None) -> None:
        import html

        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        from vkmusix.types import Artist, Genre

        super().__init__(client)

        title = album.get("title")
        self.title = html.unescape(title) if title else None

        subtitle = album.get("subtitle")
        self.subtitle = html.unescape(subtitle.replace("\n", " ")) if subtitle else None

        self.fullTitle = f"{self.title} ({self.subtitle})".replace("((", "(").replace("))", ")").replace("([", "(").replace("])", ")") if self.subtitle else self.title

        artists = self._client._finalizeResponse(
            album.get("main_artists"),
            Artist,
        )

        featuredArtists = self._client._finalizeResponse(
            album.get("featured_artists"),
            Artist,
        )

        self.artist = (
            (", ".join([
                artist.nickname
                for artist in artists[:-1]
            ]) + " & " + artists[-1].nickname)
            if len(artists) > 1 else
            artists[0].nickname +

            (
                (" feat. " + (
                    (", ".join([
                        artist.nickname
                        for artist in featuredArtists[:-1]
                    ]) + " & " + featuredArtists[-1].nickname)
                    if len(featuredArtists) > 1 else
                    featuredArtists[0].nickname))
                if featuredArtists else str()
            )
        ) if artists else None

        self.artists = artists
        self.featuredArtists = featuredArtists

        description = album.get("description")
        self.description = description if description else None

        self.releaseYear = album.get("year")

        self.genres = self._client._finalizeResponse(
            album.get("genres"),
            Genre,
        )

        self.streams = album.get("plays")
        self.saves = album.get("followers")

        self.uploadedAt = unixToDatetime(album.get("create_time"))
        self.updatedAt = unixToDatetime(album.get("update_time"))

        self.exclusive = album.get("exclusive")
        self.mainColor = album.get("main_color")

        photo = album.get("photo")
        if not photo:
            photo = album.get("thumb")
        self.photo = {int(key.split("_")[1]): value[:value.rfind("&c_uniq_tag=")][:value.rfind("&type=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        self.original = self._client._finalizeResponse(
            album.get("original"),
            Album,
        )

        tracks = album.get("tracks")
        self.trackCount = album.get("count") or (len(tracks) if tracks else None)
        self.tracks = tracks

        self.ownerId = album.get("owner_id")
        if not playlist:
            self.playlistId = None
            self.albumId = album.get("id") or album.get("album_id") or album.get("playlist_id")
            self.id = f"{self.ownerId}_{self.albumId}"
            self.url = f"{VK}music/album/{self.id}"

        else:
            self.albumId = None
            self.playlistId = album.get("id") or album.get("playlist_id") or album.get("album_id")
            self.id = f"{self.ownerId}_{self.playlistId}"
            self.url = f"{VK}music/playlist/{self.id}"

        self.raw = album


    @async_
    async def get(self, includeTracks: bool = False) -> Union["Album", None]:
        """
        Получает информацию об альбоме.

        `Пример использования`:

        album = album.get(
            includeTracks=True,
        )

        print(album)

        :param includeTracks: флаг, указывающий, небходимо ли также получить треки. (``bool``, `optional`)
        :return: `При успехе`: информация об альбоме (``types.Album``). `Если альбом не найден`: ``None``.
        """

        return await self._client.getPlaylist(
            self.albumId or self.playlistId,
            self.ownerId,
            includeTracks,
        )


    @async_
    async def getTracks(self, isLarge: bool = False) -> Union[List[Track], None]:
        """
        Получает треки альбома.

        `Пример использования`:

        tracks = album.getTracks()

        print(tracks)

        :param isLarge: флаг, указывающий, содержит ли альбом более 1000 треков. По умолчанию ``False``. Если ``True``, будет получена ограниченная информация о всех треках, если ``False`` — только последние 1000 треков, но с полной информацией. Установите ``None``, чтобы библиотека определила автоматически. (``bool``, `optional`)
        :return: `При успехе`: треки альбома (``list[types.Track]``). `Если альбом не найден`: ``None``.
        """

        return await self._client.getPlaylistTracks(
            self.albumId or self.playlistId,
            self.ownerId,
            isLarge,
        )

    get_tracks = getTracks


    @async_
    async def add(self, groupId: int = None) -> Union["Album", None]:
        """
        Добавляет альбом в музыку пользователя или группы.

        `Пример использования`:

        album = album.add()

        print(album)

        :param groupId: идентификатор группы, в которую необходимо добавить альбом. (``int``, `optional`)
        :return: `При успехе`: информация о добавленном альбоме (``types.Album``). `Если альбом не найден`: ``None``.
        """

        return await self._client.addPlaylist(
            self.albumId or self.playlistId,
            self.ownerId,
            groupId,
        )


    @async_
    async def remove(self, groupId: int = None, validateIds: bool = True) -> bool:
        """
        Удаляет альбом из музыки пользователя или группы.

        `Пример использования`:

        result = album.remove()

        print(result)

        :param groupId: идентификатор группы, из которой необходимо удалить альбом. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить альбом на наличие в музыке. По умолчанию ``True``. Установите на ``False``, если вы получили альбом через ``client.getPlaylists()`` или ``client.getAllPlaylists()``. (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если альбом не найден или не получилось его удалить`: ``False``.
        """

        return await self._client.removePlaylist(
            self.albumId or self.playlistId,
            self.ownerId,
            groupId,
            validateIds,
        )


    @async_
    async def copy(self, groupId: int = None, chatId: int = None, title: Union[str, None] = str(), description: Union[str, None] = str(), photo: Union[str, None] = str()) -> Union["Playlist", None]:
        """
        Копирует альбом в музыку пользователя или группы.

        `Пример использования`:

        album = album.copy()

        print(album)

        :param groupId: идентификатор группы, в которую необходимо скопировать альбом. (``int``, `optional`)
        :param chatId: идентификатор чата, к которому необходимо привязать скопированный альбом. (``int``, `optional`)
        :param title: название альбома. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param description: описание альбома. ``None`` для удаления. (``Union[str, None]``, `optional`)
        :param photo: ссылка на фото альбома. ``None`` для удаления. Не для удаления не работает. (``Union[str, None]``, `optional`)
        :return: `При успехе`: информация о скопированном альбоме (``types.Album``). `Если альбом не найден`: ``None``.
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