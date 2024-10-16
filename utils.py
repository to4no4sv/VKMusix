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

import os
import platform

from typing import Union

from datetime import datetime

from vkmusix.config import utcTz, moscowTz

async def getSelfId(self: "Client") -> int:
    if not self._me:
        self._me = await self.getMe()

    return self._me.get("id")


def unixToDatetime(seconds: int) -> datetime:
    UTC = datetime.utcfromtimestamp(seconds)
    return UTC.replace(tzinfo=utcTz).astimezone(moscowTz)


def addHTTPsToUrl(url: str) -> str:
    if not ("https://" in url or "http://" in url):
        url = "https://" + url

    return url


def fileExistsCaseInsensitive(filename: str) -> Union[str, None]:
    directory, filename = os.path.split(filename)
    if not directory:
        directory = "."

    for root, _, files in os.walk(directory):
        for name in files:
            if name.lower() == filename.lower():
                return os.path.join(root, name)

    return


def checkFile(filename: str) -> Union[str, None]:
    if os.path.isfile(filename):
        return filename

    system = platform.system()
    if system not in ["Linux", "Darwin"]:
        return

    filename = fileExistsCaseInsensitive(filename)
    if not filename:
        return
