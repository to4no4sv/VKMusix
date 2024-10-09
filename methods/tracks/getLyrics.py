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

class GetLyrics:
    from typing import Union

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def getLyrics(self, ownerId: int, trackId: int) -> Union[str, None]:
        from vkmusix.errors import NotFound

        lyrics = await self._req("getLyrics", {"audio_id": f"{ownerId}_{trackId}"})

        if isinstance(lyrics, NotFound):
            return

        lyrics = lyrics.get("lyrics")
        timestamps = lyrics.get("timestamps")

        return "\n".join([line.get("line") for line in timestamps if line.get("line") is not None] if timestamps else lyrics.get("text"))