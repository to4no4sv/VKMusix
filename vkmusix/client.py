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

from typing import Union, List, Type
import asyncio
import base64

import httpx

from vkmusix import config, enums, errors, methods, web, aio

class Client(methods.Methods):
    """
    Класс, который вы будете использовать для каждого взаимодействия с VK Music.

    Параметры:
        token (str, optional): Токен доступа к ВКонтакте API с правами на аудио.\n
        RuCaptchaKey (str, optional): Ключ доступа к RuCaptcha API для автоматического решения капч через этот сервис. Если не указан, капча потребует ручного решения.\n
        language (enums.Language, optional): Язык ошибок (например, Language.Russian для русского, Language.English для английского). Если не указан, используются все языки.\n
        proxy (dict, optional): Прокси, которые будут использоваться при запросах. Формат: {"http": "IP:port"} или {"socks5": "login:password@IP:port"}.\n

    Создания экземпляра:
        from vkmusix import Client
        from vkmusix.enums import Language

        client = Client(
            token="...",
            RuCaptchaKey="...",
            language=Language.Russian or Language.English,
            proxy={
                "http": "IP:port",
                "socks5": "login:password@IP:port",
            },
        ) # Все параметры необязательны

        # Или с использованием with

        with Client(
            token="...",
            RuCaptchaKey="...",
            language=Language.Russian or Language.English,
            proxy={
                "http": "IP:port",
                "socks5": "login:password@IP:port",
            },
        ) as client:
            ...
    """


    def __init__(self, token: str = None, RuCaptchaKey: str = None, language: enums.Language = None, proxy: dict = None) -> None:
        self._language = language if language and isinstance(language, enums.Language) else None

        import sys
        if sys.version_info < (3, 6):
            ruWarning = "Внимание: Работоспособость этой библиотеки гарантируется только при Python 3.6 или выше. Вы используете версию {}."
            enWarning = "Attention: The functionality of this library is guaranteed only for Python 3.6 or higher. You are using version {}."

            from warnings import warn
            warn(
                (
                    ruWarning if self._language == enums.Language.Russian
                    else (
                        enWarning if self._language == enums.Language.English
                        else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning
                    )
                ).format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                UserWarning,
            )

        if not token:
            token = input("Получите токен ВКонтакте с правами на аудиозаписи и доступ в любое время на сайте `https://vkhost.github.io/` (приложение VK Admin) и отправьте его: ")

        self._RuCaptchaKey = RuCaptchaKey

        if not proxy:
            self._proxy = None

        else:
            if not isinstance(proxy, dict):
                self._raiseError("invalidProxyType")

            newProxy = dict()

            for scheme in proxy.keys():
                if scheme.lower() not in ("http", "https", "socks4", "socks5"):
                    self._raiseError("invalidProxyDict")

                proxyURL = proxy.get(scheme)
                scheme = scheme.lower() + ("://" if not scheme.endswith("://") else str())
                newProxy[scheme] = (scheme if "://" not in proxyURL else str()) + proxyURL

            self._proxy = newProxy

        self._session = httpx.AsyncClient(proxies=self._proxy)
        self._client = web.Client(self._session)

        self._params = {
            "access_token": token,
            "v": config.VKAPIVersion,
        }
        self._closed = False
        self._me = None

        try:
            asyncio.get_running_loop()

        except RuntimeError:
            from .version import __version__
            from packaging import version

            latestVersion = self._client("https://pypi.org/pypi/vkmusix/json").get("info").get("version")

            if version.parse(latestVersion) > version.parse(__version__):
                ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/vkmusix). Вы используете версию {__version__}."
                enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/vkmusix) is available. You are using version {__version__}."

                from warnings import warn
                warn(
                    ruWarning if self._language == enums.Language.Russian
                    else (
                        enWarning if self._language == enums.Language.English
                        else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning
                    ),
                    UserWarning,
                )


    @aio.async_
    async def checkUpdates(self) -> None:
        if self._closed:
            self._raiseError("sessionClosed")

        from .version import __version__
        from packaging import version

        latestVersion = (await self._client("https://pypi.org/pypi/vkmusix/json")).get("info").get("version")

        if version.parse(latestVersion) > version.parse(__version__):
            ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/vkmusix). Вы используете версию {__version__}."
            enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/vkmusix) is available. You are using version {__version__}."

            from warnings import warn
            warn(
                ruWarning if self._language == enums.Language.Russian
                else (
                    enWarning if self._language == enums.Language.English
                    else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning
                ),
                UserWarning,
            )


    def __enter__(self) -> "Client":
        return self


    async def __aenter__(self) -> "Client":
        return self


    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            self.close()

        except errors.SessionAlreadyClosed:
            pass


    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            await self.close()

        except errors.SessionAlreadyClosed:
            pass


    @aio.async_
    async def close(self) -> None:
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `Client` или использовать метод `client.reconnect()`.
        """

        if self._closed:
            self._raiseError("sessionAlreadyClosed")
            return

        self._closed = True
        await self._session.aclose()


    @aio.async_
    async def reconnect(self) -> None:
        """
        Пересоздаёт закрытую сессию.
        """

        if not self._closed:
            self._raiseError("sessionAlreadyOpened")
            return

        self._closed = False
        self._session = httpx.AsyncClient(proxies=self._proxy)
        self._client = web.Client(self._session)


    @aio.async_
    async def _getMyId(self) -> int:
        if not self._me:
            self._me = await self.getMe()

        return self._me.get("id")


    @aio.async_
    async def _req(self, method: str, params: dict = None, json: dict = None, data: any = None, cookies: dict = None, headers: dict = None, files: dict = None, version: float = None, httpMethod: str = None) -> Union[dict, None]:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = dict()

        else:
            params = {
                k: v
                for k, v in params.items()
                if v is not None
            }

            limit = params.get("count")

            if limit:
                if not isinstance(limit, int):
                    params["count"] = None

                elif limit < 0:
                    params["count"] = 300

        if "." not in method:
            method = f"audio.{method}"

        url = f"{config.VKAPI}{method}"
        fullParams = {**params, **self._params}

        if version:
            fullParams["v"] = version

        response = await self._client(
            url,
            fullParams,
            json,
            data,
            cookies,
            headers,
            files,
            method=httpMethod if httpMethod and isinstance(httpMethod, web.Method) else web.Method.GET,
        )

        while True:
            if not response or not isinstance(response, dict):
                break

            error = response.get("error")

            if not error:
                break

            errorCode = error.get("error_code")
            errorMessage = error.get("error_msg")

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

                response = await self._client(url, fullParams)

            elif errorCode in [15, 201, 203]:
                if ": can not restore too late" in errorMessage:
                    self._raiseError("trackRestorationTimeEnded")

                else:
                    self._raiseError("accessDenied")

            elif errorCode == 18:
                self._raiseError("userWasDeletedOrBanned")

            elif errorCode == 100:
                if "One of the parameters" in errorMessage:
                    return error

                return

            elif errorCode == 104:
                if method in ["audio.getLyrics", "audio.getPlaylistById", "catalog.getSection"]:
                    return

                self._raiseError("notFound")

            else:
                return error

        if isinstance(response, list) and len(response) == 1:
            response = response[0]

        return response


    @aio.async_
    async def _solveCaptcha(self, captchaUrl: str) -> str:
        imageBytes = await self._client(captchaUrl, responseType=web.ResponseType.FILE)
        captchaImageInBase64 = base64.b64encode(imageBytes).decode("utf-8")

        RuCaptchaParams = {
            "clientKey": self._RuCaptchaKey,
            "task": {
                "type": "ImageToTextTask",
                "body": captchaImageInBase64,
            },
            "languagePool": "rn",
        }

        taskId = (await self._client(
            f"{config.RuCaptchaAPI}createTask",
            json=RuCaptchaParams,
            method=web.Method.POST,
        )).get("taskId")

        while True:
            await asyncio.sleep(5)
            taskResult = await self._client(
                f"{config.RuCaptchaAPI}getTaskResult",
                json={
                    "clientKey": self._RuCaptchaKey,
                    "taskId": taskId,
                },
                method=web.Method.POST,
            )
            errorId = taskResult.get("errorId")

            if errorId == 0 and taskResult.get("status") == "ready":
                return taskResult.get("solution").get("text")

            elif errorId == 1:
                self._raiseError("RuCaptchaInvalidKey")

            elif errorId == 10:
                self._raiseError("RuCaptchaZeroBalance")

            elif errorId == 12:
                taskId = (await self._client(
                    f"{config.RuCaptchaAPI}createTask",
                    json=RuCaptchaParams,
                    method=web.Method.POST,
                )).get("taskId")

            elif errorId == 21:
                self._raiseError("RuCaptchaBannedIP")

            elif errorId == 55:
                self._raiseError("RuCaptchaBannedAccount")


    def _raiseError(self, errorType: Union[str, None]) -> None:
        if not errorType:
            return

        errorsDict = {
            "unknown": errors.Unknown,

            "sessionClosed": errors.SessionClosed,
            "sessionAlreadyClosed": errors.SessionAlreadyClosed,
            "sessionAlreadyOpened": errors.SessionAlreadyOpened,

            "VKInvalidToken": errors.VKInvalidToken,

            "RuCaptchaInvalidKey": errors.RuCaptchaInvalidKey,
            "RuCaptchaZeroBalance": errors.RuCaptchaZeroBalance,
            "RuCaptchaBannedIP": errors.RuCaptchaBannedIP,
            "RuCaptchaBannedAccount": errors.RuCaptchaBannedAccount,

            "invalidMethod": errors.InvalidMethod,
            "accessDenied": errors.AccessDenied,

            "userWasDeletedOrBanned": errors.UserWasDeletedOrBanned,
            "trackRestorationTimeEnded": errors.TrackRestorationTimeEnded,

            "notFound": errors.NotFound,
            "chatNotFound": errors.ChatNotFound,

            "noneQuery": errors.NoneQuery,

            "ownerIdsAndTrackIdsTypeDifferent": errors.OwnerIdsAndTrackIdsTypeDifferent,
            "ownerIdsAndTrackIdsLenDifferent": errors.OwnerIdsAndTrackIdsLenDifferent,

            "trackReorderNeedsBeforeOrAfterArgument": errors.TrackReorderNeedsBeforeOrAfterArgument,
            "trackReorderNeedsOnlyBeforeOrAfterNotBoth": errors.TrackReorderNeedsOnlyBeforeOrAfterNotBoth,

            "MP3FileNotFound": errors.MP3FileNotFound,
            "MP3FileTooBig": errors.MP3FileTooBig,

            "tooHighRequestSendingRate": errors.TooHighRequestSendingRate,

            "invalidProxyType": errors.InvalidProxyType,
            "invalidProxyDict": errors.InvalidProxyDict,
        }

        if errorType not in errorsDict:
            errorType = "unknown"

        error = errorsDict.get(errorType)()

        if self._language:
            if self._language == enums.Language.Russian:
                languageAttr = "ru"

            elif self._language == enums.Language.English:
                languageAttr = "en"

            for attr in ["ru", "en"]:
                if attr != languageAttr:
                    delattr(error, attr)

        raise error


    def _finalizeResponse(self, response: Union[List[dict], dict], objectType: Type[any]) -> Union[List[any], None]:
        if not response or isinstance(response, bool):
            return

        wasList = True
        if not isinstance(response, list):
            wasList = False
            response = [response]

        for index, obj in enumerate(response):
            from vkmusix.types import Album, Playlist

            if objectType in [Album, Playlist]:
                type_ = obj.get("type")

                if type_ in [0, 5]:
                    obj = Playlist(obj, False if obj.get("original") else True, client=self)

                elif type_ == 1:
                    obj = Album(obj, True, client=self)

                else:
                    obj = objectType(obj, client=self)

            else:
                obj = objectType(obj, client=self)

            response[index] = obj

        return response if wasList else response[0]