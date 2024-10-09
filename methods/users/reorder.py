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
    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def reorder(self, trackId: int, beforeTrackId: int = None, afterTrackId: int = None) -> bool:
        """
        Изменяет порядок аудиотрека в музыке пользователя. Должен быть заполнен один из параметров на выбор: `beforeTrackId` или `afterTrackId`.

        Пример использования для перемещения на место перед определённым треком:\n
        result = client.reorder(trackId="yourTrackId", beforeTrackId="yourBeforeTrackId")\n
        print(result)

        Пример использования для перемещения на место после определённого трека:\n
        result = client.reorder(trackId="yourTrackId", afterTrackId="yourAfterTrackId")\n
        print(result)

        :param trackId: идентификатор аудиотрека, порядок которого необходимо изменить. (int)
        :param beforeTrackId: идентификатор аудиотрека перед которым необходимо поместить аудиотрек. (int, необязательно)
        :param afterTrackId: идентификатор аудиотрека после которого необходимо поместить аудиотрек. (int, необязательно)
        :return: `True`, если порядок трека успешно изменён, `False` в противном случае.
        """

        if not any((beforeTrackId, afterTrackId)):
            return self._raiseError("trackReorderNeedsBeforeOrAfterArgument")

        if all((beforeTrackId, afterTrackId)):
            return self._raiseError("trackReorderNeedsOnlyBeforeOrAfterNotBoth")

        response = await self._req("reorder", {"audio_id": trackId, **({"before": beforeTrackId} if beforeTrackId else {"after": afterTrackId})})
        return bool(response)