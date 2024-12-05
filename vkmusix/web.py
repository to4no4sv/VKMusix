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

from typing import Union
import asyncio
import re
import json as jsonlib
from enum import Enum

import httpx

from vkmusix import aio

retries = 5
timeout = 20
sleepTime = .25

def addHTTPsToUrl(url: str) -> str:
    if not ('https://' in url or 'http://' in url):
        url = 'https://' + url

    return url

class ResponseType(Enum):
    JSON = 'JSON'
    CODE = 'CODE'
    FILE = 'FILE'
    RESPONSE = 'RESPONSE'

class Method(Enum):
    GET = 'GET'
    POST = 'POST'

class Client:
    def __init__(self, client: httpx.AsyncClient = None) -> None:
        self.client = client or httpx.AsyncClient()

    @aio.async_
    async def __call__(
        self,
        url: str,
        params: dict = None,
        json: dict = None,
        data: Union[str, dict] = None,
        cookies: dict = None,
        headers: dict = None,
        files: dict = None,
        responseType: ResponseType = ResponseType.JSON,
        method: Method = Method.GET,
    ) -> any:
        retriesLocal = retries

        url = addHTTPsToUrl(url)

        if cookies and isinstance(cookies, list):
            cookies_ = dict()
            for index, cookie in enumerate(cookies):
                cookies_[cookie.get('name')] = cookie.get('value')
            cookies = cookies_

        while retriesLocal > 0:
            try:
                response = await self.client.request(
                    method.value,
                    url,
                    params=params,
                    json=json,
                    data=data,
                    cookies=cookies,
                    headers=headers,
                    files=files,
                    timeout=httpx.Timeout(timeout),
                    follow_redirects=False,
                )

                if responseType == ResponseType.JSON:
                    try:
                        responseJson = response.json()

                    except jsonlib.JSONDecodeError:
                        return

                    if 'response' in responseJson:
                        responseJson = responseJson.get('response')

                    return responseJson

                elif responseType == ResponseType.CODE:
                    responseText = response.text
                    return re.sub(r"<br/>", "\n", responseText)

                elif responseType == ResponseType.FILE:
                    return response.content

                elif responseType == ResponseType.RESPONSE:
                    return response

            except (httpx.TimeoutException, httpx.ConnectError, httpx.RequestError, httpx.ReadError):
                retriesLocal -= 1
                await asyncio.sleep(sleepTime)

            except asyncio.TimeoutError:
                retriesLocal -= 1
                await asyncio.sleep(sleepTime)