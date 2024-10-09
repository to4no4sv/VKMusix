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

    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types.track import Track

    def __init__(self, album: dict, playlist: bool = False, client: "Client" = None) -> None:
        from vkmusix.config import VK
        from vkmusix.utils import unixToDatetime

        from vkmusix.types.artist import Artist
        from vkmusix.types.genre import Genre

        super().__init__(client)

        title = album.get("title")
        self.title = title if title else None

        subtitle = album.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        description = album.get("description")
        self.description = description if description else None

        mainArtists = album.get("main_artists")
        self.artists = [Artist(mainArtist, client=self._client) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = album.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist, client=self._client) for featuredArtist in featuredArtists] if featuredArtists else None

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

        trackCount = album.get("count")
        self.trackCount = trackCount if trackCount else None

        tracks = album.get("tracks")
        self.tracks = tracks if tracks else None

        self.exclusive = album.get("exclusive")

        self.ownerId = album.get("owner_id")
        if not playlist:
            self.playlistId = None
            self.albumId = album.get("id") or album.get("album_id") or album.get("playlist_id")
            self.id = f"{self.ownerId}_{self.albumId}"
            self.url = VK + "music/album/" + self.id

        else:
            self.albumId = None
            self.playlistId = album.get("id") or album.get("playlist_id") or album.get("album_id")
            self.id = f"{self.ownerId}_{self.playlistId}"
            self.url = VK + "music/playlist/" + self.id


    @asyncFunction
    async def get(self, includeTracks: bool = False) -> "Album":
        return await self._client.getAlbum(self.ownerId, self.albumId or self.playlistId, includeTracks)


    @asyncFunction
    async def getTracks(self) -> Union[List[Track], Track]:
        return await self._client.getAlbumTracks(self.ownerId, self.albumId or self.playlistId)