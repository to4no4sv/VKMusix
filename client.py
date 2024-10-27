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

import asyncio
import httpx
import base64

from typing import Union, List, Type

from vkmusix.aio import asyncFunction
from vkmusix.config import VKAPI, VKAPIVersion, RuCaptchaAPI
from vkmusix.errors import *

from vkmusix.utils import checkFile
from vkmusix.cookies import getCookies, checkCookies
from vkmusix.webClient import Client as WebClient

from vkmusix.methods import *
from vkmusix.enums import Language

class Client(
    Artists,
    Albums,
    Tracks,
    Playlists,
    Searching,
    Users,
    Curators,
    Utils,
):
    """
    Класс для взаимодействия с VK Music.

    Аргументы:
        token (str, optional): Токен доступа к ВКонтакте API.\n
        RuCaptchaKey (str, optional): Ключ для решения капчи через сервис RuCaptcha. Если не указан, капча может потребовать ручного решения.\n
        language (Language, optional): Язык ошибок (например, `ru` для русского, `en` для английского). Если не указан, используются оба языка.\n
        proxies (dict, optional): прокси, которые будут использоваться при запросах. Формат {"протокол": "логин:пароль@IP:порт"}\n
        login (str, optional): Логин аккаунта ВКонтакте. Используется для получения cookie, необходимых для некоторых методов.\n
        password (str, optional): Пароль аккаунта ВКонтакте. Используется для получения cookie, необходимых для некоторых методов.\n
        cookieFilename (str, optional): Название файла c cookie. По умолчанию введённый логин.

    Пример использования:
        from vkmusix.enums import Language
        client = Client(token="yourToken", RuCaptchaKey="yourRuCaptchaKey", language=Language.Russian, proxies={"http": "IP:port", "socks5": "login:password@IP:port"}, login="admin@vkmusix.ru", password="vkmusix.ru", cookieFilename="admin")
        result = client.searchArtists("prombl")
        print(result)
    """


    def __init__(self, token: str = None, RuCaptchaKey: str = None, language: Language = None, proxies: dict = None, login: str = None, password: str = None, cookieFilename: str = None) -> None:
        import sys
        if sys.version_info < (3, 6):
            ruWarning = "Внимание: Работоспособость этой библиотеки гарантируется только при Python 3.6 или выше. Вы используете версию {}."
            enWarning = "Attention: The functionality of this library is guaranteed only for Python 3.6 or higher. You are using version {}."

            from warnings import warn
            warn(
                (ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning)).format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                UserWarning,
            )

        if not token:
            token = input("Получите токен ВКонтакте с правами на аудиозаписи и доступ в любое время на сайте `https://vkhost.github.io/` (приложение VK Admin) и отправьте его: ")

        self._RuCaptchaKey = RuCaptchaKey
        self._language = language if language and isinstance(language, Language) else None

        if not proxies:
            self._proxies = None

        else:
            if not isinstance(proxies, dict):
                self._raiseError("proxyShouldBeDict")

            newProxies = dict()

            for scheme in proxies.keys():
                if scheme.lower() not in ("http", "https", "socks4", "socks5"):
                    self._raiseError("invalidProxyDict")

                proxyURL = proxies.get(scheme)
                scheme = scheme.lower() + ("://" if not scheme.endswith("://") else str())
                newProxies[scheme] = (scheme if "://" not in proxyURL else str()) + proxyURL

            self._proxies = newProxies

        if login or cookieFilename:
            cookieFileExist = False
            if not cookieFilename:
                cookieFilename = login

            if checkFile(f"{cookieFilename}.VKCookie"):
                cookieFileExist = True

            if not cookieFileExist:
                if login and password:
                    cookieFilename = getCookies(login, password, cookieFilename)
                    if isinstance(cookieFilename, dict):
                        self._raiseError(cookieFilename.get("error"))

                else:
                    self._raiseError("VKCookieFileNotFound")

            self._cookies = checkCookies(cookieFilename)
            if isinstance(self._cookies, dict):
                self._raiseError(self._cookies.get("error"))

        else:
            self._cookies = None

        self._session = httpx.AsyncClient(proxies=self._proxies)
        self._client = WebClient(self._session)

        self._params = {
            "access_token": token,
            "v": VKAPIVersion,
        }
        self._closed = False
        self._me = None

        try:
            asyncio.get_running_loop()

        except RuntimeError:
            from .version import __version__
            from packaging import version

            latestVersion = self._client.req("https://pypi.org/pypi/vkmusix/json").get("info").get("version")

            if version.parse(latestVersion) > version.parse(__version__):
                ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/vkmusix). Вы используете версию {__version__}."
                enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/vkmusix) is available. You are using version {__version__}."

                from warnings import warn
                warn(
                    ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning),
                    UserWarning,
                )


    @asyncFunction
    async def checkUpdates(self) -> None:
        if self._closed:
            self._raiseError("sessionClosed")

        from .version import __version__
        from packaging import version

        latestVersion = (await self._client.req("https://pypi.org/pypi/vkmusix/json")).get("info").get("version")

        if version.parse(latestVersion) > version.parse(__version__):
            ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/vkmusix). Вы используете версию {__version__}."
            enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/vkmusix) is available. You are using version {__version__}."

            from warnings import warn
            warn(
                ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning),
                UserWarning,
            )


    def __enter__(self) -> "Client":
        return self


    async def __aenter__(self) -> "Client":
        return self


    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            self.close()

        except SessionAlreadyClosed:
            pass


    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            await self.close()

        except SessionAlreadyClosed:
            pass


    @asyncFunction
    async def close(self) -> None:
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `Client` или использовать метод `reconnect`.
        """

        if self._closed:
            self._raiseError("sessionAlreadyClosed")
            return

        self._closed = True
        await self._session.aclose()


    @asyncFunction
    async def reconnect(self) -> None:
        """
        Пересоздаёт закрытую сессию.
        """

        if not self._closed:
            self._raiseError("sessionAlreadyOpened")
            return

        self._closed = False
        self._session = httpx.AsyncClient(proxies=self._proxies)
        self._client = WebClient(self._session)


    @asyncFunction
    async def _req(self, method: str, params: dict = None, HTTPMethod: str = "GET") -> Union[dict, None]:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = dict()

        else:
            params = {k: v for k, v in params.items() if v is not None}

            limit = params.get("count")

            if limit:
                if not isinstance(limit, int):
                    params["count"] = None

                elif limit < 0:
                    params["count"] = 300

        if "." not in method:
            method = f"audio.{method}"

        url = f"{VKAPI}{method}"
        fullParams = {**params, **self._params}

        req = await self._client.req(url, fullParams, method=HTTPMethod)

        while isinstance(req, dict) and req.get("error"):
            error = req.get("error")
            errorCode = error.get("error_code")

            if errorCode == 3:
                self._raiseError("invalidMethod")

            elif errorCode == 5:
                self._raiseError("VKInvalidToken")

            elif errorCode in [6, 9]:
                self._raiseError("tooHighRequestSendingRate")

            elif errorCode == 10 and method == "audio.createChatPlaylist":
                self._raiseError("chatNotFound")

            elif errorCode == 14:
                captchaUrl = error.get("captcha_img")
                if self._RuCaptchaKey:
                    solve = await self._solveCaptcha(captchaUrl)

                else:
                    solve = input(captchaUrl + "\nВведите решение капчи: ")

                fullParams.update(
                    {
                        "captcha_sid": error.get("captcha_sid"),
                        "captcha_key": solve,
                    }
                )

                req = await self._client.req(url, fullParams)

            elif errorCode in [15, 201, 203]:
                if ": can not restore too late" in error.get("error_msg"):
                    self._raiseError("trackRestorationTimeEnded")

                else:
                    self._raiseError("accessDenied")

            elif errorCode == 18:
                self._raiseError("userWasDeletedOrBanned")

            elif errorCode == [100, 104]:
                return

            else:
                return error

        if isinstance(req, list) and len(req) == 1:
            req = req[0]

        return req


    @asyncFunction
    async def _solveCaptcha(self, captchaUrl: str) -> str:
        imageBytes = await self._client.req(captchaUrl, responseType="file")
        captchaImageInBase64 = base64.b64encode(imageBytes).decode("utf-8")

        RuCaptchaParams = {
            "clientKey": self._RuCaptchaKey,
            "task": {
                "type": "ImageToTextTask",
                "body": captchaImageInBase64,
            },
            "languagePool": "rn",
        }

        taskId = (await self._client.req(RuCaptchaAPI + "createTask", json=RuCaptchaParams, method="POST")).get("taskId")

        while True:
            await asyncio.sleep(5)
            taskResult = await self._client.req(RuCaptchaAPI + "getTaskResult", json={"clientKey": self._RuCaptchaKey, "taskId": taskId}, method="POST")
            errorId = taskResult.get("errorId")

            if errorId == 0 and taskResult.get("status") == "ready":
                return taskResult.get("solution").get("text")

            elif errorId == 1:
                self._raiseError("RuCaptchaInvalidKey")

            elif errorId == 10:
                self._raiseError("RuCaptchaZeroBalance")

            elif errorId == 12:
                taskId = (await self._client.req(RuCaptchaAPI + "createTask", json=RuCaptchaParams, method="POST")).get("taskId")

            elif errorId == 21:
                self._raiseError("RuCaptchaBannedIP")

            elif errorId == 55:
                self._raiseError("RuCaptchaBannedAccount")


    def _raiseError(self, errorType: Union[str, None]) -> None:
        if not errorType:
            return

        errorsDict = {
            "unknown": Unknown,

            "sessionClosed": SessionClosed,
            "sessionAlreadyClosed": SessionAlreadyClosed,
            "sessionAlreadyOpened": SessionAlreadyOpened,

            "VKInvalidToken": VKInvalidToken,
            "VKCookieFileNotFound": VKCookieFileNotFound,
            "VKInvalidCookie": VKInvalidCookie,
            "VKUnsuccessfulLoginAttempt": VKUnsuccessfulLoginAttempt,

            "RuCaptchaInvalidKey": RuCaptchaInvalidKey,
            "RuCaptchaZeroBalance": RuCaptchaZeroBalance,
            "RuCaptchaBannedIP": RuCaptchaBannedIP,
            "RuCaptchaBannedAccount": RuCaptchaBannedAccount,

            "invalidMethod": InvalidMethod,
            "accessDenied": AccessDenied,
            "accessDeniedWithoutCookie": AccessDeniedWithoutCookie,

            "userWasDeletedOrBanned": UserWasDeletedOrBanned,
            "trackRestorationTimeEnded": TrackRestorationTimeEnded,

            "notFound": NotFound,
            "chatNotFound": ChatNotFound,
            "artistNotFound": ArtistNotFound,
            "albumNotFound": AlbumNotFound,
            "trackNotFound": TrackNotFound,
            "lyricsNotFound": LyricsNotFound,
            "playlistNotFound": PlaylistNotFound,

            "noneQuery": NoneQuery,

            "ownerIdsAndTrackIdsTypeDifferent": OwnerIdsAndTrackIdsTypeDifferent,
            "ownerIdsAndTrackIdsLenDifferent": OwnerIdsAndTrackIdsLenDifferent,

            "trackReorderNeedsBeforeOrAfterArgument": TrackReorderNeedsBeforeOrAfterArgument,
            "trackReorderNeedsOnlyBeforeOrAfterNotBoth": TrackReorderNeedsOnlyBeforeOrAfterNotBoth,

            "MP3FileNotFound": MP3FileNotFound,
            "MP3FileTooBig": MP3FileTooBig,

            "tooHighRequestSendingRate": TooHighRequestSendingRate,

            "invalidProxyType": InvalidProxyType,
            "invalidProxyDict": InvalidProxyDict,
        }

        if errorType not in errorsDict:
            errorType = "unknown"

        error = errorsDict.get(errorType)()

        if self._language:
            if self._language == Language.Russian:
                languageAttr = "ru"

            elif self._language == Language.English:
                languageAttr = "en"

            for attr in ["ru", "en"]:
                if attr != languageAttr:
                    delattr(error, attr)

        raise error


    def _finalizeResponse(self, response: Union[List[dict], dict], objectType: Type[any]) -> Union[List[any], None]:
        if not (response or response is False):
            return

        if not isinstance(response, list):
            response = [response]

        for index, obj in enumerate(response):
            from vkmusix.types import Playlist

            if objectType is Playlist:
                playlistType = obj.get("type")

                if playlistType in [0, 5]:
                    obj = objectType(obj, False if obj.get("original") else True, client=self)

                elif playlistType == 1:
                    from vkmusix.types import Album

                    obj = Album(obj, True, client=self)

                else:
                    obj = objectType(obj, client=self)

            else:
                obj = objectType(obj, client=self)

            response[index] = obj

        return response if len(response) > 1 else response[0]
