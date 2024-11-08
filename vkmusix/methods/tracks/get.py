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

class Get:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def get(self, ownerIds: Union[List[int], int], trackIds: Union[List[int], int], includeLyrics: bool = False) -> Union[List[Track], Track, None]:
        """
        Получает информацию о треках.

        `Пример использования`:

        track = client.get(
            ownerIds=-2001471901,
            trackIds=123471901,
            includeLyrics=True,
        )

        print(track)

        :param ownerIds: идентификаторы владельцев треков. Максимум 343. (``Union[list[int], int]``)
        :param trackIds: идентификаторы треков. Максимум 343. (``Union[list[int], int]``)
        :param includeLyrics: флаг, указывающий, небходимо ли также получить текст. (``bool``, `optional`)
        :return: `Если треков несколько`: информация о треках (``list[types.Track]``). `Если трек один`: информация о треке (``types.Track``). `При успехе`: информация о треке (``types.Track``). `Если трек не найден`: ``None``.
        """

        from asyncio import gather

        from vkmusix.types import Track

        if type(ownerIds) != type(trackIds):
            self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        elif isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        wasList = isinstance(ownerIds, list)

        if not all((isinstance(ownerIds, list), isinstance(trackIds, list))):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        ids =  [
            f"{ownerId}_{trackId}"
            for ownerId, trackId in zip(
                ownerIds,
                trackIds,
            )
        ]

        tasks = [
            self._req(
                "getById",
                {
                    "audios": ",".join(ids),
                },
            ),
        ]

        if includeLyrics:
            for id in ids:
                ownerId, trackId = id.split("_")
                tasks.append(
                    self.getLyrics(
                        ownerId,
                        trackId,
                    ),
                )

        responses = await gather(*tasks)

        tracks = responses[0]
        if not tracks:
            return

        if not isinstance(tracks, list):
            tracks = [tracks]

        if includeLyrics:
            lyrics = responses[1:]

            for idx, track in enumerate(tracks):
                track["lyrics"] = lyrics[idx] if lyrics else None

        return self._finalizeResponse(tracks if wasList else tracks[0], Track)