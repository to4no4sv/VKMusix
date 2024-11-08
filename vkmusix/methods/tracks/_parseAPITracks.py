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

class _ParseAPITracks:
    from typing import Union, List, Dict

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def _parseAPITracks(self, tracks: Union[List[Dict[str, str]], None]) -> Union[List[Track], None]:
        from vkmusix.types import Track

        if not tracks:
            return

        if not isinstance(tracks, list):
            tracks = [tracks]

        for idx, track in enumerate(tracks):
            id = track.get("audio_id")

            if id.count("_") == 3:
                id = id[:id.rfind("_")]

            ownerId, trackId = id.split("_")[:2]
            tracks[idx] = {
                "owner_id": int(ownerId),
                "track_id": int(trackId),
            }

        return self._finalizeResponse(tracks, Track)