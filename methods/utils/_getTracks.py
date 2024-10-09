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

class _GetTracks:
    from typing import Union, List

    from vkmusix.types import Track

    async def _getTracks(self, tracks: str) -> Union[List[Track]]:
        import re

        from vkmusix.types import Track

        tracks = re.sub(r"\\/", "/", re.sub(r"false", "False", re.sub(r"true", "True", re.sub(r"null", "None", tracks))))

        try:
            tracks = eval(tracks[tracks.rfind("[["): tracks.rfind("]]") + 2])

        except SyntaxError:
            self._raiseError("accessDenied" + ("WithoutCookie" if not hasattr(self, "_cookies") else ""))

        if isinstance(tracks, list):
            for index, track in enumerate(tracks):
                if len(track) < 20:
                    tracks[index] = None
                    continue

                album = track[19]
                if album:
                    album.append(dict(zip(["photo_160", "photo_300"], track[14].split(",")[::-1])))

                tracks[index] = self._finalizeResponse(
                    {
                        "owner_id": track[1],
                        "track_id": track[0],
                        "title": track[3],
                        "artist": track[4],
                        "subtitle": track[16],
                        "main_artists": track[17],
                        "featured_artists": track[18],
                        "duration": track[5],
                        "album": {
                            "owner_id": album[0],
                            "album_id": album[1],
                            **({
                                   "photo": album[3]
                               }
                               if len(album) == 4 else dict()
                               )
                        }
                        if album else dict(),
                        "release_audio_id": track[-2],
                    },
                    Track,
                )

            tracks = [track for track in tracks if track]

            if not tracks or all(track is None for track in tracks):
                tracks = None

        return tracks