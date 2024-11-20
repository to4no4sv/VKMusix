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

class Track(Base):
    """
    Класс, представляющий трек.

    Атрибуты:
        title (str): название трека.

        subtitle (str, optional): подзаголовок трека, во ВКонтакте отображается серым цветом справа от названия.

        fullTitle (str): полное название трека в формате {title} ({subtitle}).

        artist (str): все артисты трека в виде строки.

        artists (list[types.Artist], optional): основные артисты трека. Доступно только для официально загруженных треков.

        featuredArtists (list[types.Artist], optional): приглашённые артисты трека. Доступно только для оффициально загруженных треков.

        duration (int): длительность трека в секундах.

        genre (types.Genre, optional): жанр трека.

        lyrics (str, optional): текст трека.

        hasLyrics (bool, optional): флаг, указывающий, имеет ли трек текст. Отсутствует, если lyrics не None.

        uploadedAt (datetime): дата и время загрузки трека (не релиза).

        fileUrl (str, optional) — ссылка на файл трека в формате .M3U8. Отсутствует, если трек доступен только с подпиской, а залогиненный пользователь её не имеет.

        album (types.Album, optional): альбом, на котором присутствует этот трек. В некоторых случаях может быть доступно и не для оффициально загруженных треков.

        partNumber (int, optional): ???.

        explicit (bool, optional): флаг, указывающий, есть ли в треке ненормативная лексика. Доступно только для оффициально загруженных треков.

        licensed (bool, optional): флаг, указывающий, ???

        focus (bool, optional): флаг, указывающий, является ли трек фокус-треком на альбоме.

        shortsAllowed (bool, optional): флаг, указывающий, доступен ли этот трек для использования в ВК Клипах.

        storiesAllowed (bool, optional): флаг, указывающий, доступен ли этот трек для использования в историях.

        releaseTrack (types.Track, optional): официально загруженный трек, который ВКонтакте считает максимально похожим на данный. Может быть этим же треком.

        ownerId (int): идентификатор владельца трека (пользователь или группа).

        trackId (int): идентификатор трека.

        id (str): полный идентификатор трека в формате {ownerId}_{trackId}.

        url (str): ссылка на трек в формате https://vk.com/audio{id}

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.enums import Extension

    def __init__(self, track: dict, releaseTrack: bool = None, client: "Client" = None) -> None:
        import html

        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        from vkmusix.types import Artist, Album, Genre

        super().__init__(client)

        title = track.get("title")
        self.title = html.unescape(title) if title else None

        subtitle = track.get("subtitle")
        self.subtitle = html.unescape(subtitle.replace("\n", " ")) if subtitle else None

        self.fullTitle = f"{self.title} ({self.subtitle})".replace("((", "(").replace("))", ")").replace("([", "(").replace("])", ")") if self.subtitle else self.title

        artist = track.get("artist")
        self.artist = html.unescape(artist) if artist else None

        self.artists = self._client._finalizeResponse(
            track.get("main_artists"),
            Artist,
        )

        self.featuredArtists = self._client._finalizeResponse(
            track.get("featured_artists"),
            Artist,
        )

        self.duration = track.get("duration")

        genreId = track.get("genre_id")
        self.genre = Genre(
            genreId=genreId,
            client=self._client,
        ) if genreId else None

        self.lyrics = track.get("lyrics")
        self.hasLyrics = track.get("has_lyrics") if not self.lyrics else None

        self.uploadedAt = unixToDatetime(track.get("date"))

        self.fileUrl = track.get("url") or None

        self.album = self._client._finalizeResponse(
            track.get("album"),
            Album,
        )

        self.partNumber = track.get("part_number")

        self.explicit = track.get("is_explicit")

        self.licensed = track.get("is_licensed")
        self.focus = track.get("is_focus_track")

        self.shortsAllowed = track.get("short_videos_allowed")
        self.storiesAllowed = track.get("stories_allowed")

        self.releaseTrack = None
        if not releaseTrack:
            releaseTrackId = track.get("release_audio_id")

            if releaseTrackId:
                releaseTrackOwnerId, releaseTrackTrackId = tuple(map(int, releaseTrackId.split("_")))
                self.releaseTrack = Track(
                    {
                        "owner_id": releaseTrackOwnerId,
                        "track_id": releaseTrackTrackId,
                    },
                    True,
                    client=self._client,
                )

        self.ownerId = track.get("owner_id")
        self.trackId = track.get("id") or track.get("track_id")
        self.id = f"{self.ownerId}_{self.trackId}"
        self.url = f"{VK}audio{self.id}"

        self.raw = track


    @async_
    async def get(self, includeLyrics: bool = False) -> Union["Track", None]:
        """
        Получает информацию о треке.

        `Пример использования`:

        track = track.get(
            includeLyrics=True,
        )

        print(track)

        :param includeLyrics: флаг, указывающий, небходимо ли также получить текст. (``bool``, `optional`)
        :return: `При успехе`: информация о треке (``types.Track``). `Если трек не найден`: ``None``.
        """

        return await self._client.get(
            self.ownerId,
            self.trackId,
            includeLyrics,
        )


    @async_
    async def getLyrics(self) -> Union[str, None]:
        """
        Получает текст трека.

        `Пример использования`:

        lyrics = track.getLyrics()

        print(lyrics)

        :return: `При успехе`: текст трека (``str``). `Если трек не найден или текст отсутствует`: ``None``.
        """

        return await self._client.getLyrics(
            self.ownerId,
            self.trackId,
        )


    @async_
    async def download(self, filename: str = None, directory: str = None, extension: Extension = None, metadata: bool = False) -> Union[str, None]:
        """
        Скачивает трек.

        `Пример использования`:

        from vkmusix.enums import Extension

        path = track.download(
            extension=Extension.OPUS,
            metadata=True,
        )

        print(path)

        :param filename: имя файла с треком. По умолчанию ``{artist} — {fullTitle}``. Поддерживаемые переменные для динамического имени: ``artist``, ``title``, ``subtitle``, ``fullTitle``, ``album``. Пример динамического имени файла: ``{artist} - {title} ({album})``. (``str``, `optional`)
        :param directory: путь к директории, в которую загрузить трек. (``str``, `optional`)
        :param extension: расширение файла с треком. По умолчанию ``Extension.MP3``. (``enums.Extension``, `optional`)
        :param metadata: флаг, указывающий, необходимо ли добавить метаданные (артист, название, альбом, обложка) к файлу с треком. По умолчанию ``False``. Игнорируется, если параметр ``extension`` равен ``Extension.TS``. (``bool``, `optional`)
        :return: `При успехе`: полный путь к загруженному файлу (``str``). `Если трек не найден или недоступен для загрузки`: ``None``.
        """

        return await self._client.download(
            filename=filename,
            directory=directory,
            extension=extension,
            metadata=metadata,
            track=self,
        )


    @async_
    async def getRecommendations(self, limit: int = None, offset: int = None) -> Union[List["Track"], None]:
        """
        Получает рекомендации по треку.

        `Пример использования`:

        tracks = track.getRecommendations(
            limit=10,
        )

        print(tracks)

        :param limit: лимит треков. (``int``, `optional`)
        :param offset: сколько треков пропустить. (``int``, `optional`)
        :return: `При успехе`: рекомендации (``list[types.Track]``). `Если рекомендации отсутствуют или трек не найден`: ``None``.
        """

        return await self._client.getRecommendations(
            limit,
            offset,
            self.ownerId,
            self.trackId,
        )


    @async_
    async def add(self, playlistId: int = None, groupId: int = None) -> bool:
        """
        Добавляет трек в музыку или плейлист пользователя или группы.

        `Пример использования`:

        result = track.add()

        print(result)

        :param playlistId: идентификатор плейлиста, в который необходимо добавить трек. (``int``, `optional`)
        :param groupId: идентификатор группы, в музыку или плейлист которой необходимо добавить трек. (``int``, `optional`)
        :return: `При успехе`: ``True``. `Если трек не удалось добавить`: ``False``.
        """

        return await self._client.add(
            self.ownerId,
            self.trackId,
            playlistId,
            groupId,
        )


    @async_
    async def remove(self, playlistId: int = None, groupId: int = None, validateIds: bool = True) -> bool:
        """
        Удаляет трек из музыки или плейлиста пользователя или группы.

        `Пример использования`:

        result = track.remove()

        print(result)

        :param playlistId: идентификатор плейлиста, из которого необходимо удалить трек. Метод не работает для плейлистов, привязанных к чату (``int``, `optional`)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить трек. (``int``, `optional`)
        :param validateIds: флаг, указывающий, необходимо ли перепроверить трек на наличие в музыке или плейлисте. По умолчанию ``True``. Установите на ``False``, если вы получили трек через ``client.getTracks()`` (при удалении из музыки) или ``client.getPlaylistTracks()`` (при удалении из плейлиста). (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если трек не удалось удалить`: ``False``.
        """

        return await self._client.remove(
            self.ownerId,
            self.trackId,
            playlistId,
            groupId,
            validateIds,
        )


    @async_
    async def edit(self, title: str = None, artist: str = None, lyrics: str = None, genreId: int = None, removeFromSearchResults: bool = None) -> bool:
        """
        Изменяет информацию о треке.

        `Пример использования`:

        result = track.edit(
            filename="Маленький ярче — LARILARI",
            title="LARILARI",
            artist="Маленький ярче",
            genreId=21,
            removeFromSearchResults=True,
        )

        print(result)

        :param title: название трека. По умолчанию берётся из метаданных файла. (``str``, `optional`)
        :param artist: артисты трека. По умолчанию берётся из метаданных файла. (``str``, `optional`)
        :param lyrics: текст трека. (``str``, `optional`)
        :param genreId: идентификатор жанра трека. (``int``, `optional`)
        :param removeFromSearchResults: флаг, указывающий, необходимо ли исключить трек из поиска. По умолчанию ``False``. (``bool``, `optional`)
        :return: `При успехе`: ``True``. `Если информацию о треке не удалось изменить`: ``False``.
        """

        return await self._client.edit(
            self.ownerId,
            self.trackId,
            title,
            artist,
            lyrics,
            genreId,
            removeFromSearchResults,
        )


    @async_
    async def restore(self) -> bool:
        """
        Восстанавливает удалённый трек.

        `Пример использования`:

        result = track.restore()

        print(result)

        :return: `При успехе`: ``True``. `Если трек не удалось восстановить`: ``False``.
        """

        return await self._client.restore(
            self.ownerId,
            self.trackId,
        )


    @async_
    async def reorder(self, beforeTrackId: int = None, afterTrackId: int = None) -> bool:
        """
        Изменяет порядок трека в музыке пользователя. Должен быть заполнен один из параметров на выбор: ``beforeTrackId`` или ``afterTrackId``.

        `Пример использования для перемещения на место перед определённым треком`:

        result = track.reorder(
            beforeTrackId=123471901,
        )

        print(result)

        `Пример использования для перемещения на место после определённого трека`:

        result = track.reorder(
            afterTrackId=123471901,
        )

        print(result)

        :return: ``True``.
        """

        return await self._client.reorder(
            self.trackId,
            beforeTrackId,
            afterTrackId,
        )


    @async_
    async def setBroadcast(self, groupIds: Union[List[int], int] = None) -> bool:
        """
        Транслирует трек в статус owner'а (пользователь или группа).

        `Пример использования для трансляции трека в статус залогиненного пользователя`:

        result = track.setBroadcast()

        print(result)

        `Пример использования для трансляции трека в статус группы`:

        result = track.setBroadcast(
            groupIds=1,
        )

        print(result)

        :param groupIds: идентификаторы групп, трансляцию в статус которых необходимо начать. По умолчанию залогиненный пользователь. (``Union[list[int], int]``, `optional`)
        :return: `При успехе`: ``True``. `В противном случае`: ``False``.
        """

        return await self._client.setBroadcast(
            self.ownerId,
            self.trackId,
            groupIds,
        )