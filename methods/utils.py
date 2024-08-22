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

from typing import Union, List

from ..aio import asyncFunction
from ..errors import Error
from ..utils import addHTTPsToUrl


class Utils:
    @asyncFunction
    async def APIReq(self, method: str, params: dict = None, HTTPMethod: str = "GET") -> Union[dict, List[dict], bool, int, Error]:
        """
        Отправляет запрос к любому методу VK API с указанными параметрами.

        Пример использования для создания поста на своей страничке с текстом «Примет, мир!»:\n
        result = client.APIReq(method="wall.post", params={"message": "Привет, мир!"}, HTTPMethod="POST")\n
        print(result)

        :param method: метод, к которому необходимо отправить запрос. (str)
        :param params: параметры запроса в виде словаря. Ключи и значения зависят от метода API. (dict, необязательно)
        :param HTTPMethod: HTTP-метод для запроса. Может быть `GET`, `POST`, `PUT`, `DELETE` и т.д.
        :return: результат выполнения запроса, тип и структура данных зависят от метода API.
        """

        if params is None:
            params = dict()

        return await self._VKReq(method, params, HTTPMethod)


    @asyncFunction
    async def getSelf(self) -> Union[dict, Error]:
        """
        Получает информацию о текущем пользователе.

        Пример использования:\n
        result = client.getSelf()\n
        print(result)

        :return: словарь с информацией о текущем пользователе с гарантированными ключами: `id`, `first_name` и `last_name`.
        """

        return await self._VKReq("users.get")


    @asyncFunction
    async def createVKccUrl(self, url: str) -> Union[str, Error]:
        """
        Создаёт сокращённую ссылку с доменом «vk.cc».

        Пример использования:\n
        result = client.createVKccUrl(url="google.com")\n
        print(result)

        :param url: ссылка, которую необходимо сократить. (str)
        :return: сокращённая ссылка с доменом «vk.cc».
        """

        url = addHTTPsToUrl(url)

        return (await self._VKReq("utils.getShortLink", {"url": url})).get("short_url")