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
    Класс, представляющий аудиотрек.

    Атрибуты:
        title (str): название аудиотрека.\n
        subtitle (str, optional): подзаголовок аудиотрека, если он присутствует.\n
        artists (list[Artist], optional): список основных артистов аудиотрека, представленных объектами класса `Artist`.\n
        artist (str): основной(ые) артист(ы) аудиотрека.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов аудиотрека, представленных объектами класса `Artist`.\n
        genre (Genre, optional): жанр аудиотрека, представленный объектом класса `Genre`.\n
        explicit (bool, optional): флаг, указывающий, есть ли в треке ненормативная лексика.\n
        duration (int): продолжительность аудиотрека в секундах.\n
        fileUrl (str, optional): ссылка на m3u8-файл.\n
        lyrics (str, optional): текст аудиотрека.\n
        hasLyrics (bool, optional): флаг, указывающий, имеет ли аудиотрек текст.\n
        uploadedAt (datetime, optional): дата и время загрузки аудиотрека (UTC +03:00).\n
        album (Album, optional): альбом, к которому принадлежит аудиотрек, представленный объектом класса `Album`.\n
        releaseTrack (Track, optional): аудиотрек, загруженный официально, похожий на данный.\n
        ownerId (str): идентификатор владельца аудиотрека.\n
        trackId (str): идентификатор аудиотрека.\n
        id (str): комбинированный идентификатор в формате `ownerId_trackId`.\n
        url (str): URL страницы аудиотрека.
    """

    from typing import Union, List

    from vkmusix.aio import asyncFunction

    def __init__(self, track: dict, releaseTrack: bool = False, client: "Client" = None) -> None:
        import html

        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        from vkmusix.types.artist import Artist
        from vkmusix.types.album import Album
        from vkmusix.types.genre import Genre

        super().__init__(client)

        title = track.get("title")
        self.title = html.unescape(title) if title else None

        subtitle = track.get("subtitle")
        self.subtitle = html.unescape(subtitle.replace("\n", " ")) if subtitle else None

        self.fullTitle = f"{self.title} ({self.subtitle})".replace("((", "(").replace("))", ")").replace("([", "(").replace("])", ")") if self.subtitle else self.title

        artist = track.get("artist")
        self.artist = html.unescape(artist) if artist else None

        mainArtists = track.get("main_artists")
        self.artists = [Artist(mainArtist, client=self._client) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = track.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist, client=self._client) for featuredArtist in featuredArtists] if featuredArtists else None

        genreId = track.get("genre_id")
        self.genre = Genre(genreId=genreId, client=self._client) if genreId else None

        self.explicit = track.get("is_excplicit")

        duration = track.get("duration")
        self.duration = duration if duration else None

        self.fileUrl = track.get("url")

        lyrics = track.get("lyrics")
        self.lyrics = lyrics if lyrics else None
        self.hasLyrics = track.get("has_lyrics") if not lyrics else None

        uploadedAt = track.get("date")
        self.uploadedAt = unixToDatetime(uploadedAt) if uploadedAt else None

        album = track.get("album")
        self.album = Album(album, client=self._client) if album else None

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
        self.url = VK + f"audio{self.id}"

        self.raw = track


    @asyncFunction
    async def get(self, includeLyrics: bool = False) -> "Track":
        """
        Получает информацию об аудиотреке.

        Пример использования:\n
        result = track.get(includeLyrics=True)\n
        print(result)

        :param includeLyrics: флаг, указывающий, необходимо ли включать текст трека в ответ. (bool, по умолчанию `False`)
        :return: информация об аудиотреке в виде объекта модели `Track`.
        """

        return await self._client.get(self.ownerId, self.trackId, includeLyrics)


    @asyncFunction
    async def getLyrics(self) -> Union[str, None]:
        return await self._client.getLyrics(self.ownerId, self.trackId)


    @asyncFunction
    async def download(self, filename: str = None, directory: str = None) -> Union[str, None]:
        """
        Загружает аудиотрек в формате MP3.

        :param filename: название файла с аудиотреком. (str, по умолчанию `{artist} -- {title}`)
        :param directory: путь к директории, в которую загрузить файл. (str, по умолчанию `os.getcwd()`)
        :return: полный путь к загруженному файлу, если аудиотрек успешно загружен, иначе `None`.
        """

        return await self._client.download(filename=filename, directory=directory, track=self)


    @asyncFunction
    async def getRecommendations(self, limit: int = None, offset: int = None) -> Union[List["Track"], "Track", None]:
        """
        Получает похожие на аудиотрек.

        Пример использования:\n
        result = track.getRecommendations(limit=20)\n
        print(result)

        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, необязательно)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если похожие треки отсутствуют).
        """

        return await self._client.getRecommendations(limit, offset, self.ownerId, self.trackId)


    @asyncFunction
    async def add(self, playlistId: int = None, groupId: int = None) -> bool:
        """
        Добавляет аудиотрек в музыку или плейлист пользователя или группы.

        Пример использования:\n
        result = track.add(playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param playlistId: идентификатор плейлиста, в который необходимо добавить аудиотрек. (int, необязательно)
        :param groupId: идентификатор группы, в музыку или плейлист которой необходимо добавить аудиотрек. (int, необязательно)
        :return: `True`, если аудиотрек успешно добавлен, `False` в противном случае.
        """

        return await self._client.add(self.ownerId, self.trackId, playlistId, groupId)


    @asyncFunction
    async def remove(self, playlistId: int = None, groupId: int = None, reValidateIds: bool = True) -> bool:
        """
        Удаляет аудиотрек из музыки или плейлиста пользователя или группы.

        Пример использования:\n
        result = track.remove(playlistId="yourPlaylistId", groupId="yourGroupId", reValidateIds=False)\n
        print(result)

        :param playlistId: идентификатор плейлиста, из которого необходимо удалить аудиотрек(и). (int, необязательно, метод временно не работает для плейлистов, привязанных к чату)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить аудиотрек(и). (int, необязательно)
        :param reValidateIds: флаг, указывающий, необходимо ли перепроверить идентификатор(ы) аудитрека(ов) по находящимся в плейлисте. (bool, по умолчанию `True`)
        :return: `True`, если аудиотрек успешно удалён, `False` в противном случае.
        """

        return await self._client.remove(self.ownerId, self.trackId, playlistId, groupId, reValidateIds)


    @asyncFunction
    async def edit(self, title: Union[str, int] = None, artist: Union[str, int] = None, lyrics: Union[str, int] = None, genreId: int = None, removeFromSearchResults: bool = None) -> bool:
        """
        Изменяет информацию об аудиотреке.

        Пример использования:\n
        result = track.edit(title="zapreti", artist="prombl", "lyrics"=str(), "genreId"=3, removeFromSearchResults=True)\n
        print(result)

        :param title: новое название аудиотрека. (str, необязательно)
        :param artist: новый(е) артист(ы) аудиотрека. (str, необязательно)
        :param lyrics: новый текст аудиотрека. (str, необязательно)
        :param genreId: новый жанр аудиотрека (в виде идентификатора). (int, необязательно)
        :param removeFromSearchResults: флаг, указывающий, будет ли аудиотрек скрыт из поисковой выдачи. (bool, необязательно)
        :return: `True`, если информация аудиотрека успешно обновлена, `False` в противном случае.
        """

        return await self._client.edit(self.ownerId, self.trackId, title, artist, lyrics, genreId, removeFromSearchResults)


    @asyncFunction
    async def restore(self) -> bool:
        """
        Восстанавливает удалённый аудиотрек.

        Пример использования:\n
        result = track.restore()\n
        print(result)

        :return: `True`, если аудиотрек успешно восстановлен, `False` в противном случае.
        """

        return await self._client.restore(self.ownerId, self.trackId)


    @asyncFunction
    async def reorder(self, beforeTrackId: int = None, afterTrackId: int = None) -> bool:
        """
        Изменяет порядок аудиотрека в музыке пользователя. Должен быть заполнен один из параметров на выбор: `beforeTrackId` или `afterTrackId`.

        Пример использования для перемещения на место перед определённым треком:\n
        result = track.reorder(beforeTrackId="yourBeforeTrackId")\n
        print(result)

        Пример использования для перемещения на место после определённого трека:\n
        result = track.reorder(afterTrackId="yourAfterTrackId")\n
        print(result)

        :param beforeTrackId: идентификатор аудиотрека перед которым необходимо поместить аудиотрек. (int, необязательно)
        :param afterTrackId: идентификатор аудиотрека после которого необходимо поместить аудиотрек. (int, необязательно)
        :return: `True`, если порядок трека успешно изменён, `False` в противном случае.
        """

        return await self._client.reorder(self.trackId, beforeTrackId, afterTrackId)


    @asyncFunction
    async def setBroadcast(self, groupIds: Union[List[str], str] = None) -> bool:
        """
        Устанавливает (удаляет) аудиотрек в (из) статус(а) пользователя или группы.

        Пример использования для установки аудиотрека в статус пользователя:\n
        result = track.setBroadcast()\n
        print(result)

        Пример использования для установки аудиотрека в статус группы:\n
        result = track.setBroadcast(groupdIds="yourGroupId")\n
        print(result)

        Пример использования для удаления аудиотрека из статуса пользователя:\n
        result = track.setBroadcast()\n
        print(result)

        Пример использования для удаления аудиотрека из статуса группы:\n
        result = track.setBroadcast(groupdIds="yourGroupId")\n
        print(result)

        :param groupIds: идентификатор(ы) групп(ы), в (из) статус(а) которой необходимо установить (удалить) аудиотрек. (int, по умолчанию текущий пользователь)
        :return: `True`, если аудиотрек успешно установлен (удалён) в (из) статус(а), `False` в противном случае.
        """

        return await self._client.setBroadcast(self.ownerId, self.trackId, groupIds)
