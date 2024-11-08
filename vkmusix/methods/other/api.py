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

class Api:
    from typing import Union, List

    from vkmusix.aio import async_

    @async_
    async def api(self, method: str, params: dict = None, json: dict = None, data: Union[str, dict] = None, cookies: dict = None, headers: dict = None, files: dict = None, version: int = None, httpMethod: str = None) -> Union[dict, List[dict], bool, int, None]:
        """
        Отправляет запрос к любому методу Вконтакте API.

        `Пример использования`:

        result = client.api(
            method="wall.post",
            data={
                "message": "Привет!",
            },
            httpMethod="POST",
        )

        print(result)

        :param method: метод, к которому необходимо отправить запрос. (``str``)
        :param params: параметры в ссылке. (``dict``, `optional`)
        :param json: тело запроса в формате JSON. (``dict``, `optional`)
        :param data: данные в теле запроса. (``Union[str, dict]``, `optional`)
        :param cookies: cookie запроса. (``dict``, `optional`)
        :param headers: HTTP-заголовки запроса. (``dict``, `optional`)
        :param files: файлы для загрузки. Для POST-запросов. (``dict``, `optional`)
        :param version: версия ВКонтакте API. (``float``, `optional`)
        :param httpMethod: HTTP-метод запроса. По умолчанию GET. (``str``, `optional`)
        :return: Ответ ВКонтакте API (``Union[dict, List[dict], bool, int, None]``).
        """

        return await self._req(
            method=method,
            params=params,
            json=json,
            data=data,
            cookies=cookies,
            headers=headers,
            files=files,
            version=version,
            httpMethod=httpMethod.upper() if httpMethod and isinstance(httpMethod, str) else "GET",
        )