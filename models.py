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

import re
import pytz
from typing import Union, List, Tuple
from datetime import datetime

from .aio import asyncFunction
from .errors import Error
from .config import VK, moscowTz
from .encoder import _BaseModel


def unixToDatetime(seconds: int) -> datetime:
    UTC = datetime.utcfromtimestamp(seconds)
    return UTC.replace(tzinfo=pytz.utc).astimezone(moscowTz)


class Artist(_BaseModel):
    """
    Класс, представляющий артиста.

    Атрибуты:
        nickname (str): псевдоним артиста.\n
        photo (dict, optional): словарь с размерами и URL фотографий артиста, отсортированный по размеру.\n
        albums (list[Album], optional): список альбомов артиста, представленных объектами класса `Album`.\n
        tracks (list[Track], optional): список аудиотреков артиста, представленных объектами класса `Track`.\n
        id (str): идентификатор артиста.\n
        url (str): URL страницы артиста.
    """

    def __init__(self, artist: dict, client: "Client" = None) -> None:
        super().__init__(client)

        self.nickname = artist.get("name")

        photo = artist.get("photo")
        if photo:
            photoDict = {f'{photo.get("width")}': re.sub(r"\.(j|jp|jpg)$", str(), photo.get("url")[:photo.get("url").rfind("&c_uniq_tag=")]) for photo in photo}
            self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        else:
            photo = artist.get("photos")
            self.photo = dict(sorted({f'{photo.get("width")}': photo.get("url") for photo in photo[0].get("photo")}.items(), key=lambda item: (int(item[0])))) if photo else None

        albums = artist.get("albums")
        self.albums = [Album(album, self._client) for album in albums] if albums else None

        tracks = artist.get("tracks")
        self.tracks = [Track(track, self._client) for track in tracks] if tracks else None

        if self.nickname not in ["Various Artists", "Various Artist"]:
            self.id = artist.get("id") or artist.get("artist_id")
            domain = artist.get("domain")
            self.url = VK + "artist/" + (domain if domain else self.id)

        else:
            self.id = None
            self.url = None


    @asyncFunction
    async def get(self, includeAlbums: bool = False, includeTracks: bool = False) -> Union["Artist", Error]:
        return await self._client.getArtist(self.id, includeAlbums, includeTracks)


    @asyncFunction
    async def getRelated(self, limit: int = 10) -> Union[List["Artist"], "Artist", None, Error]:
        return await self._client.getRelatedArtists(self.id, limit)


    @asyncFunction
    async def follow(self) -> Union[bool, Error]:
        return await self._client.followArtist(self.id)


    @asyncFunction
    async def unfollow(self) -> Union[bool, Error]:
        return await self._client.unfollowArtist(self.id)


class Album(_BaseModel):
    """
    Класс, представляющий альбом.

    Атрибуты:
        title (str): название альбома.\n
        subtitle (str, optional): подзаголовок альбома, если он присутствует.\n
        description (str, optional): описание альбома, если оно присутствует.\n
        artists (list[Artist]): список основных артистов альбома, представленных объектами класса `Artist`.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов альбома, представленных объектами класса `Artist`.\n
        releaseYear (int, optional): год выпуска альбома.\n
        genres (list[Genre], optional): список жанров альбома, представленных объектами класса Genre.\n
        plays (int, optional): количество прослушиваний альбома.\n
        uploadedAt (datetime, optional): дата и время загрузки альбома (UTC +03:00).\n
        updatedAt (datetime, optional): дата и время последнего обновления информации об альбоме (UTC +03:00).\n
        photo (dict, optional): словарь с размерами и URL фотографий альбома, отсортированный по размеру.\n
        tracks (list[Track], optional): список аудиотреков альбома, где каждый аудиотрек представлен объектом класса `Track`.\n
        exclusive (bool, optional): флаг, указывающий, является ли альбом эксклюзивным.\n
        ownerId (str): идентификатор владельца альбома.\n
        albumId (str): идентификатор альбома.\n
        id (str): комбинированный идентификатор в формате `ownerId_albumId`.\n
        url (str): URL страницы альбома.
    """

    def __init__(self, album: dict, playlist: bool = False, client: "Client" = None) -> None:
        super().__init__(client)
        title = album.get("title")
        self.title = title if title else None

        subtitle = album.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        description = album.get("description")
        self.description = description if description else None

        mainArtists = album.get("main_artists")
        self.artists = [Artist(mainArtist, self._client) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = album.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist, self._client) for featuredArtist in featuredArtists] if featuredArtists else None

        releaseYear = album.get("year")
        self.releaseYear = releaseYear if releaseYear else None

        genres = album.get("genres")
        if genres:
            for index, genre in enumerate(genres):
                genres[index] = Genre(genre)
        self.genres = genres if genres else None

        plays = album.get("plays")
        self.plays = plays if plays else None

        followers = album.get("followers")
        self.followers = followers if followers else None

        uploadedAt = album.get("create_time")
        self.uploadedAt = unixToDatetime(uploadedAt) if uploadedAt else None

        updatedAt = album.get("update_time")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        photo = album.get("photo")
        if not photo:
            photo = album.get("thumb")
        self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")][:value.rfind("&type=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        original = album.get("original")
        self.original = Album(original, client=self._client) if original else None

        tracksCount = album.get("count")
        self.tracksCount = tracksCount if tracksCount else None

        tracks = album.get("tracks")
        self.tracks = tracks if tracks else None

        self.exclusive = album.get("exclusive")

        self.ownerId = album.get("owner_id")
        if not playlist:
            self.playlistId = None
            self.albumId = album.get("id") or album.get("album_id")
            self.id = f"{self.ownerId}_{self.albumId}"
            self.url = VK + "music/album/" + self.id

        else:
            self.albumId = None
            self.playlistId = album.get("id") or album.get("playlist_id")
            self.id = f"{self.ownerId}_{self.playlistId}"
            self.url = VK + "music/playlist/" + self.id


    @asyncFunction
    async def get(self, includeTracks: bool = False) -> Union["Album", Error]:
        return await self._client.getAlbum(self.ownerId, self.albumId or self.playlistId, includeTracks)


class Track(_BaseModel):
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
        fileUrl (str, optional): ссылка на MP3-файл.\n
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

    def __init__(self, track: dict, client: "Client" = None, releaseTrack: bool = False) -> None:
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
        self.artists = [Artist(mainArtist, self._client) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = track.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist, self._client) for featuredArtist in featuredArtists] if featuredArtists else None

        genreId = track.get("genre_id")
        self.genre = Genre(genreId=genreId, client=self._client) if genreId else None

        self.explicit = track.get("is_excplicit")

        duration = track.get("duration")
        self.duration = duration if duration else None

        fileUrl = track.get("url")
        self.fileUrl = fileUrl[:fileUrl.rfind("?siren=1")] if fileUrl else None

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
                self.releaseTrack = Track({"owner_id": releaseTrackOwnerId, "track_id": releaseTrackTrackId}, self._client, True)

        self.ownerId = track.get("owner_id")
        self.trackId = track.get("id") or track.get("track_id")

        self.id = f"{self.ownerId}_{self.trackId}"
        self.url = VK + f"audio{self.id}"


    @asyncFunction
    async def get(self, includeLyrics: bool = False) -> Union["Track", Error]:
        return await self._client.get(self.ownerId, self.trackId, includeLyrics)


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


class Playlist(_BaseModel):
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

    def __init__(self, playlist: dict, isOwn: bool = False, client: "Client" = None) -> None:
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

        createddAt = playlist.get("create_time")
        self.createdAt = unixToDatetime(createddAt) if createddAt else None

        updatedAt = playlist.get("update_time")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        photo = playlist.get("photo")
        if not photo:
            photo = playlist.get("thumb")
        self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        original = playlist.get("original")
        self.original = Playlist(original, self._client) if original else None

        tracksCount = playlist.get("count")
        self.tracksCount = tracksCount if tracksCount else None

        tracks = playlist.get("tracks")
        self.tracks = tracks if tracks else None

        self.ownerId = playlist.get("owner_id")
        self.playlistId = playlist.get("id") or playlist.get("playlist_id")
        self.id = f"{self.ownerId}_{self.playlistId}"
        self.url = VK + "music/playlist/" + self.id

        self.own = isOwn


    @asyncFunction
    async def get(self, includeTracks: bool = False) -> Union["Playlist", Error]:
        return await self._client.getPlaylist(self.playlistId, self.ownerId, includeTracks)


    @asyncFunction
    async def add(self, groupId: int = None) -> Union[int, None, Error]:
        return await self._client.addPlaylist(self.playlistId, self.ownerId, groupId)


    @asyncFunction
    async def remove(self, groupId: int = None) -> Union[bool, Error]:
        return await self._client.removePlaylist(self.playlistId, groupId)


    @asyncFunction
    async def edit(self, title: Union[str, int] = None, description: Union[str, int] = None, photo: str = None, groupId: int = None) -> Union[bool, Error]:
        return await self._client.editPlaylist(self.playlistId, title, description, photo, groupId)


    @asyncFunction
    async def copy(self, groupId: int = None, newTitle: Union[str, None] = str(), newDescription: Union[str, None] = str(), newPhoto: Union[str, None] = str()) -> Union["Playlist", None, Error]:
        return await self._client.copyPlaylist(self.playlistId, self.ownerId, groupId, newTitle, newDescription, newPhoto)


    @asyncFunction
    async def addTrack(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]]) -> Union[Tuple[Union[bool, Error]], Error]:
        return await self._client.add(ownerIds, trackIds, self.playlistId, self.ownerId)


    @asyncFunction
    async def removeTrack(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], reValidateIds: bool = True) -> Union[Tuple[Union[bool, Error]], Error]:
        return await self._client.remove(ownerIds, trackIds, self.playlistId, self.ownerId, reValidateIds)


trackGenres = {
    1: "Рок",
    2: "Поп",
    3: "Рэп и Хип-хоп",
    4: "Расслабляющая",
    5: "House и Танцевальная",
    6: "Инструментальная",
    7: "Метал",
    8: "Дабстеп",
    10: "Drum & Bass",
    11: "Транс",
    12: "Шансон",
    13: "Этническая",
    14: "Акустическая",
    15: "Регги",
    16: "Классическая",
    17: "Инди-поп",
    18: "Другая",
    19: "Скит",
    21: "Альтернатива",
    22: "Электро-поп и Диско",
    1001: "Джаз и Блюз"
}


class Genre(_BaseModel):
    """
    Класс, представляющий жанр аудиотрека или альбома.

    Атрибуты:
        title (str): название жанра.\n
        id (str): идентификатор жанра.\n
    """

    def __init__(self, genre: dict = None, genreId: int = None, client: "Client" = None) -> None:
        super().__init__(client)
        if genreId:
            self.title = trackGenres.get(genreId, "Неизвестен")

            self.id = genreId

        else:
            self.title = genre.get("name")

            self.id = genre.get("id") or genre.get("genre_id")
