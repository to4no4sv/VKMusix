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

class GetSections:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Section

    @async_
    async def getSections(self, ownerId: int = None) -> Union[List[Section], None]:
        """
        Получает разделы музыки owner'а (пользователь или группа).

        `Пример использования`:

        sections = client.getSections()

        print(sections)

        :param ownerId: идентификатор owner'а (пользователь или группа). По умолчанию залогиненный пользователь. (``int``, `optional`)
        :return: `При успехе`: разделы музыки (``List[types.Section]``). `Если owner (пользователь или группа) не найден`: ``None``.
        """

        from vkmusix.types import Section

        if not ownerId:
            ownerId = await self._getMyId()

        catalog = await self._req(
            "catalog.getAudio",
            {
                "owner_id": ownerId,
            },
        )

        catalog = catalog.get("catalog")
        sections = catalog.get("sections")

        if not sections:
            return

        return self._finalizeResponse(sections, Section)

    get_sections = getSections