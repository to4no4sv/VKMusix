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

class SearchResults(Base):
    """
    Класс, представляющий результаты поиска.

    Атрибуты:
        artists (list[types.Artist], optional): найденные артисты.

        albums (list[types.Album], optional): найденные альбомы.

        tracks (list[types.Track], optional): найденные треки.

        playlists (list[types.Playlist], optional): найденные плейлисты.
    """

    from typing import Union, List

    from vkmusix.types import Artist, Album, Track, Playlist

    def __init__(self, artists: Union[List[Artist], None] = None, albums: Union[List[Album], None] = None, tracks: Union[List[Track], None] = None, playlists: Union[List[Playlist], None] = None) -> None:
        self.artists = artists
        self.albums = albums
        self.tracks = tracks
        self.playlists = playlists