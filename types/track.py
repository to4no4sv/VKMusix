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
    from vkmusix.errors import Error

    def __init__(self, track: dict, releaseTrack: bool = False, client: "Client" = None) -> None:
        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        from vkmusix.types.artist import Artist
        from vkmusix.types.album import Album
        from vkmusix.types.genre import Genre

        super().__init__(client)

        self.title = track.get("title")
        self.subtitle = track.get("subtitle")

        title = track.get("title")
        self.title = title if title else None

        subtitle = track.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        artist = track.get("artist")
        self.artist = artist if artist else None

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
                self.releaseTrack = Track({"owner_id": releaseTrackOwnerId, "track_id": releaseTrackTrackId}, True, client=self._client)

        self.ownerId = track.get("owner_id")
        self.trackId = track.get("id") or track.get("track_id")

        self.id = f"{self.ownerId}_{self.trackId}"
        self.url = VK + f"audio{self.id}"


    @asyncFunction
    async def get(self, includeLyrics: bool = False) -> Union["Track", Error]:
        return await self._client.get(self.ownerId, self.trackId, includeLyrics)


    @asyncFunction
    async def download(self, filename: str = None, directory: str = None) -> Union[str, None, Error]:
        return await self._client.download(filename=filename, directory=directory, track=self)


    @asyncFunction
    async def getRecommendations(self, limit: int = 10, offset: int = 0) -> Union[List["Track"], "Track", None, Error]:
        return await self._client.getRecommendations(limit, offset, self.ownerId, self.trackId)


    @asyncFunction
    async def add(self, playlistId: int = None, groupId: int = None) -> Union[bool, Error]:
        return (await self._client.add(self.ownerId, self.trackId, playlistId, groupId))[0]


    @asyncFunction
    async def remove(self, playlistId: int = None, groupId: int = None, reValidateIds: bool = True) -> Union[bool, Error]:
        return (await self._client.remove(self.ownerId, self.trackId, playlistId, groupId, reValidateIds))[0]


    @asyncFunction
    async def edit(self, title: Union[str, int] = None, artist: Union[str, int] = None, lyrics: Union[str, int] = None, genreId: int = None, removeFromSearchResults: bool = None) -> Union[bool, Error]:
        return await self._client.edit(self.ownerId, self.trackId, title, artist, lyrics, genreId, removeFromSearchResults)


    @asyncFunction
    async def restore(self) -> Union[bool, Error]:
        return await self._client.restore(self.ownerId, self.trackId)


    @asyncFunction
    async def reorder(self, beforeTrackId: int = None, afterTrackId: int = None) -> Union[bool, Error]:
        return await self._client.reorder(self.trackId, beforeTrackId, afterTrackId)


    @asyncFunction
    async def setBroadcast(self, groupIds: Union[List[str], str] = None) -> Union[bool, Error]:
        return await self._client.setBroadcast(self.ownerId, self.trackId, groupIds)