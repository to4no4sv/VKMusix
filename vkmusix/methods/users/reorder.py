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

class Reorder:
    from vkmusix.aio import async_

    @async_
    async def reorder(self, trackId: int, beforeTrackId: int = None, afterTrackId: int = None) -> bool:
        """
        Изменяет порядок трека в музыке пользователя. Должен быть заполнен один из параметров на выбор: ``beforeTrackId`` или ``afterTrackId``.

        `Пример использования для перемещения на место перед определённым треком`:

        result = client.reorder(
            trackId=123471901,
            beforeTrackId=123471901,
        )

        print(result)

        `Пример использования для перемещения на место после определённого трека`:

        result = client.reorder(
            trackId=123471901,
            afterTrackId=123471901,
        )

        print(result)

        :return: ``True``.
        """

        if not any((beforeTrackId, afterTrackId)):
            self._raiseError("trackReorderNeedsBeforeOrAfterArgument")

        if all((beforeTrackId, afterTrackId)):
            self._raiseError("trackReorderNeedsOnlyBeforeOrAfterNotBoth")

        response = await self._req(
            "reorder",
            {
                "audio_id": trackId,
                **(
                    {
                        "before": beforeTrackId,
                    }
                    if beforeTrackId else
                    {
                        "after": afterTrackId,
                    }
                ),
            }
        )

        return bool(response)