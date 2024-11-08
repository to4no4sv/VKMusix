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

import re
import asyncio

from json import JSONDecodeError

import httpx

retries = 5
timeout = 20
sleepTime = .25

def addHTTPsToUrl(url: str) -> str:
    if not ("https://" in url or "http://" in url):
        url = "https://" + url

    return url

class Client:
    from typing import Union

    from vkmusix.aio import async_

    def __init__(self, client: httpx.AsyncClient = None) -> None:
        self.client = client or httpx.AsyncClient()


    @async_
    async def request(self, url: str, params: dict = None, json: dict = None, data: Union[str, dict] = None, cookies: dict = None, headers: dict = None, files: dict = None, responseType: str = "json", method: str = "GET") -> any:
        responseType = responseType.lower()
        retriesLocal = retries

        url = addHTTPsToUrl(url)

        if cookies and isinstance(cookies, list):
            cookies_ = dict()
            for index, cookie in enumerate(cookies):
                cookies_[cookie.get("name")] = cookie.get("value")
            cookies = cookies_

        while retriesLocal > 0:
            try:
                response = await self.client.request(
                    method,
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

                if responseType == "json":
                    try:
                        responseJson = response.json()

                    except JSONDecodeError:
                        return

                    if "response" in responseJson:
                        responseJson = responseJson.get("response")

                    return responseJson

                elif responseType == "code":
                    responseText = response.text
                    return re.sub(r"<br/>", "\n", responseText)

                elif responseType == "file":
                    return response.content

                elif responseType == "response":
                    return response

            except (httpx.TimeoutException, httpx.ConnectError, httpx.RequestError, httpx.ReadError):
                retriesLocal -= 1
                await asyncio.sleep(sleepTime)

            except asyncio.TimeoutError:
                retriesLocal -= 1
                await asyncio.sleep(sleepTime)

    req = request