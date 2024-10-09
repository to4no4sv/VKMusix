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

class CreateVKccUrl:
    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def createVKccUrl(self, url: str) -> str:
        """
        Создаёт сокращённую ссылку с доменом «vk.cc».

        Пример использования:\n
        result = client.createVKccUrl(url="google.com")\n
        print(result)

        :param url: ссылка, которую необходимо сократить. (str)
        :return: сокращённая ссылка с доменом «vk.cc».
        """

        from vkmusix.utils import addHTTPsToUrl

        url = addHTTPsToUrl(url)

        return (await self._req("utils.getShortLink", {"url": url})).get("short_url")