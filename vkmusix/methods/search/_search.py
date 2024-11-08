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

from vkmusix.types import Artist, Album, Track, Playlist, SearchResults

classes = {
    Artist: "artists",
    Album: "albums",
    Track: "audios",
    Playlist: "playlists"
}

class _Search:
    from typing import Union, List, Type

    async def _search(self, method: str, params: tuple, itemClass: Union[List[Type[Union[Artist, Album, Track, Playlist]]], Type[Union[Artist, Album, Track, Playlist]]]) -> Union[SearchResults, None]:
        query, limit, offset = params[0], params[1], params[2]
        if not query:
            return self._raiseError("noneQuery")

        params = {
            "q": query,
            "count": limit,
            "offset": offset,
        }

        response = await self._req(method, params)

        if not isinstance(response, dict):
            return

        if isinstance(itemClass, list):
            results = dict()
            for model, key in classes.items():
                modelObjects = response.get(key)
                if modelObjects:
                    modelObjects = modelObjects.get("items")

                if not modelObjects:
                    continue

                results[model] = self._finalizeResponse(modelObjects, model)

            return SearchResults(
                artists=results.get(Artist),
                albums=results.get(Album),
                tracks=results.get(Track),
                playlists=results.get(Playlist),
            ) if results else None

        else:
            items = response.get("items")
            return self._finalizeResponse(items, itemClass)