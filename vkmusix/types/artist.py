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

class Artist(Base):
    """
    Класс, представляющий артиста.

    Атрибуты:
        nickname (str): псевдоним артиста.

        photo (dict, optional): словарь с ссылками на различные размеры фотографии артиста, отсортированные по возрастанию.

        albums (list[types.Album], optional): альбомы артиста. Доступны при получении через client.getArtist(includeAlbums=True).

        tracks (list[types.Track], optional): треки артиста. Доступны при получении через client.getArtist(includeTracks=True).

        domain (str, optional): уникальное имя артиста, использующееся в ссылке. Недоступно для Various Artists.

        id (int, optional): идентификатор артиста. Недоступен для Various Artists.

        url (str, optional): ссылка на артиста в формате https://vk.com/artist/{domain or id}. Недоступна для Various Artists.

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types.album import Album
    from vkmusix.types.track import Track

    def __init__(self, artist: dict, client: "Client" = None) -> None:
        import re
        import html

        from vkmusix.config import VK

        super().__init__(client)

        nickname = artist.get("name")
        self.nickname = html.unescape(nickname) if nickname else None

        photo = artist.get("photo")
        if photo:
            photoDict = {int(photo.get("width")): re.sub(r"\.(j|jp|jpg)$", str(), photo.get("url")[:photo.get("url").rfind("&c_uniq_tag=")][:photo.get("url").rfind("&type=")]) for photo in photo}
            self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        else:
            photo = artist.get("photos")
            self.photo = dict(sorted({int(photo.get("width")): photo.get("url") for photo in photo[0].get("photo")}.items(), key=lambda item: (int(item[0])))) if photo else None

        self.albums = artist.get("albums")
        self.tracks = artist.get("tracks")

        domain = artist.get("domain")
        id = artist.get("id") or artist.get("artist_id")
        self.domain = domain if domain != id else None
        self.id = id
        self.url = f"{VK}artist/{self.domain or self.id}" if self.domain or self.id else None

        self.raw = artist


    @async_
    async def get(self, includeAlbums: bool = False, includeTracks: bool = False) -> Union["Artist", None]:
        """
        Получает информацию об артисте.

        `Пример использования`:

        artist = artist.get(
            includeAlbums=True,
            includeTracks=True,
        )

        print(artist)

        :param includeAlbums: флаг, указывающий, небходимо ли также получить альбомы. (``bool``, `optional`)
        :param includeTracks: флаг, указывающий, небходимо ли также получить треки. (``bool``, `optional`)
        :return: `При успехе`: информация об артисте (``types.Artist``). `Если артист не найден`: ``None``.
        """

        return await self._client.getArtist(
            self.id,
            includeAlbums,
            includeTracks,
        )


    @async_
    async def getAlbums(self, limit: int = None, offset: int = None) -> Union[List[Album], None]:
        """
        Получает альбомы артиста.

        `Пример использования`:

        albums = artist.getAlbums(
            limit=10,
        )

        print(albums)

        :param limit: лимит альбомов. (``int``, `optional`)
        :param offset: сколько альбомов пропустить. (``int``, `optional`)
        :return: `При успехе`: альбомы артиста (``list[types.Album]``). `Если артист не найден или альбомы отсутствуют`: ``None``.
        """

        return await self._client.getArtistAlbums(
            self.id,
            limit,
            offset,
        )

    get_albums = getAlbums


    @async_
    async def getTracks(self, limit: int = None, offset: int = None) -> Union[List[Track], None]:
        """
        Получает треки артиста из раздела «Популярное».

        `Пример использования`:

        tracks = artist.getTracks(
            limit=10,
        )

        print(tracks)

        :param limit: лимит треков. (``int``, `optional`)
        :param offset: сколько треков пропустить. (``int``, `optional`)
        :return: `При успехе`: треки артиста (``list[types.Track]``). `Если артист не найден или треки отсутствуют`: ``None``.
        """

        return await self._client.getArtistTracks(
            self.id,
            limit,
            offset,
        )

    get_tracks = getTracks


    @async_
    async def getRelated(self, limit: int = None, offset: int = None) -> Union[List["Artist"], None]:
        """
        Получает похожих артистов.

        `Пример использования`:

        artists = artist.getRelated(
            limit=10,
        )

        print(artists)

        :param limit: лимит артистов. (``int``, `optional`)
        :param offset: сколько артистов пропустить. (``int``, `optional`)
        :return: `При успехе`: похожие артисты (``list[types.Artist]``). `Если артист не найден или похожие артисты отсутствуют`: ``None``.
        """

        return await self._client.getRelatedArtists(
            self.id,
            limit,
            offset,
        )

    get_related = getRelated


    @async_
    async def follow(self) -> bool:
        """
        Подписывается на обновления музыки артиста.

        `Пример использования`:

        result = artist.follow()

        print(result)

        :return: `При успехе`: ``True``. `Если артист не найден`: ``False``.
        """

        return await self._client.followArtist(self.id)


    @async_
    async def unfollow(self) -> bool:
        """
        Отписывается от обновлений музыки артиста.

        `Пример использования`:

        result = artist.unfollow()

        print(result)

        :return: `При успехе`: ``True``. `Если артист не найден`: ``False``.
        """

        return await self._client.unfollowArtist(self.id)