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
        nickname (str): псевдоним артиста.\n
        photo (dict, optional): словарь с размерами и URL фотографий артиста, отсортированный по размеру.\n
        albums (list[Album], optional): список альбомов артиста, представленных объектами класса `Album`.\n
        tracks (list[Track], optional): список аудиотреков артиста, представленных объектами класса `Track`.\n
        id (str): идентификатор артиста.\n
        url (str): URL страницы артиста.
    """

    from typing import Union, List

    from vkmusix.aio import asyncFunction
    from vkmusix.types.album import Album
    from vkmusix.types.track import Track

    def __init__(self, artist: dict, client: "Client" = None) -> None:
        import re

        from vkmusix.config import VK

        super().__init__(client)

        self.nickname = artist.get("name")

        photo = artist.get("photo")
        if photo:
            photoDict = {f'{photo.get("width")}': re.sub(r"\.(j|jp|jpg)$", str(), photo.get("url")[:photo.get("url").rfind("&c_uniq_tag=")][:photo.get("url").rfind("&type=")]) for photo in photo}
            self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        else:
            photo = artist.get("photos")
            self.photo = dict(sorted({f'{photo.get("width")}': photo.get("url") for photo in photo[0].get("photo")}.items(), key=lambda item: (int(item[0])))) if photo else None

        self.albums = artist.get("albums")
        self.tracks = artist.get("tracks")

        self.id = artist.get("id") or artist.get("artist_id")

        if self.id:
            domain = artist.get("domain")
            self.url = VK + "artist/" + (domain if domain else self.id)

        else:
            self.url = None


    @asyncFunction
    async def get(self, includeAlbums: bool = False, includeTracks: bool = False) -> "Artist":
        """
        Получает информацию об артисте.

        Пример использования:\n
        result = artist.get(includeAlbums=True, includeTracks=True)\n
        print(result)

        :param includeAlbums: флаг, указывающий, необходимо ли включать альбомы артиста в ответ. (bool, по умолчанию `False`)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки артиста в ответ. (bool, умолчанию `False`)
        :return: информация об артисте в виде объекта модели `Artist`.
        """

        return await self._client.getArtist(self.id, includeAlbums, includeTracks)


    @asyncFunction
    async def getAlbums(self) -> Union[List[Album], Album, None]:
        return await self._client.getArtistAlbums(self.id)


    @asyncFunction
    async def getTracks(self) -> Union[List[Track], Track, None]:
        return await self._client.getArtistTracks(self.id)


    @asyncFunction
    async def getRelated(self, limit: int = None) -> Union[List["Artist"], "Artist", None]:
        """
        Получает похожих артистов.

        Пример использования:\n
        result = artist.getRelated(limit=5)\n
        print(result)

        :param limit: максимальное количество артистов, которое необходимо вернуть. (int, необязательно)
        :return: список артистов в виде объектов модели `Artist`, артист в виде объекта модели `Artist` (если он единственственный), или None (если `artistId` неверный или похожие артисты отсутствуют).
        """

        return await self._client.getRelatedArtists(self.id, limit)


    @asyncFunction
    async def follow(self) -> bool:
        """
        Подписывается на обновления музыки артиста.

        Пример использования:\n
        result = artist.follow()\n
        print(result)

        :param artistId: идентификатор артиста, на обновления которого необходимо подписаться. (int)
        :return: `True`, если Вы успешно подписались на обновления музыки артиста, `False` в противном случае.
        """

        return await self._client.followArtist(self.id)


    @asyncFunction
    async def unfollow(self) -> bool:
        """
        Отписывается от обновлений музыки артиста.

        Пример использования:\n
        result = artist.unfollow()\n
        print(result)

        :return: `True`, если Вы успешно отписались от обновлений музыки артиста, `False` в противном случае.
        """

        return await self._client.unfollowArtist(self.id)
