import asyncio
import httpx
import base64

from typing import Union, List, Type

from .aio import asyncFunction
from .models import Artist, Album, Track, Playlist
from .config import VKAPI, VKAPIVersion, RuCaptchaAPI
from .errors import errorsDict, createErrorClass, Error
from .cookies import getCookies, checkCookies
from .utils import checkFile
from .webClient import Client as WebClient

from .methods.utils import Utils
from .methods.search import Search
from .methods.update import Update
from .methods.get import Get


class Client(Utils, Search, Get, Update):
    """
    Класс для взаимодействия с VK Music.

    Аргументы:
        VKToken (str, optional): Токен доступа к ВКонтакте API.\n
        RuCaptchaKey (str, optional): Ключ для решения капчи через сервис RuCaptcha. Если не указан, капча может потребовать ручного решения.\n
        errorsLanguage (str, optional): Язык ошибок (например, `ru` для русского, `en` для английского). Если не указан, используются оба языка.\n
        login (str, optional): Логин аккаунта ВКонтакте. Используется для получения cookie, необходимых для некоторых методов.\n
        password (str, optional): Пароль аккаунта ВКонтакте. Используется для получения cookie, необходимых для некоторых методов.\n
        cookieFilename (str, optional): Название файла c cookie. По умолчанию введённый логин.

    Пример использования:
        client = Client(VKToken="yourVKToken", RuCaptchaKey="yourRuCaptchaKey", errorsLanguage="ru", login="admin@vkmusix.ru", password="vkmusix.ru", cookieFilename="admin")
        result = client.searchArtists("prombl")
        print(result)
    """


    def __init__(self, VKToken: str = None, RuCaptchaKey: str = None, errorsLanguage: str = None, login: str = None, password: str = None, cookieFilename: str = None) -> None:
        if not VKToken:
            VKToken = input("Получите токен ВКонтакте с правами на аудиозаписи и доступ в любое время на сайте `https://vkhost.github.io/` (приложение VK Admin) и отправьте его: ")

        self._RuCaptchaKey = RuCaptchaKey
        self._errorsLanguage = errorsLanguage.lower() if errorsLanguage and isinstance(errorsLanguage, str) and errorsLanguage.lower() in ["ru", "en"] else None

        import sys
        if sys.version_info < (3, 6):
            ruWarning = "Внимание: Работоспособость этой библиотеки гарантируется только при Python 3.6 или выше. Вы используете версию {}."
            enWarning = "Attention: The functionality of this library is guaranteed only for Python 3.6 or higher. You are using version {}."

            from warnings import warn
            warn(
                (ruWarning if self._errorsLanguage == "ru" else enWarning if self._errorsLanguage == "en" else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning).format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                UserWarning
            )

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

        self._clientSession = httpx.AsyncClient()
        self._client = WebClient(self._clientSession)

        self._defaultParams = {"access_token": VKToken, "v": VKAPIVersion}
        self._closed = False

        from .version import __version__
        from packaging import version
        latestVersion = self._client.sendReq("https://pypi.org/pypi/vkmusix/json").get("info").get("version")
        if version.parse(latestVersion) > version.parse(__version__):
            ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/vkmusix). Вы используете версию {__version__}."
            enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/vkmusix) is available. You are using version {__version__}."

            from warnings import warn
            warn(
                (ruWarning if self._errorsLanguage == "ru" else enWarning if self._errorsLanguage == "en" else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning).format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                UserWarning
            )


    def __enter__(self) -> "Client":
        return self


    def __aenter__(self) -> "Client":
        return self


    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


    def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


    @asyncFunction
    async def close(self) -> None:
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `Client`.
        """

        self._closed = True
        await self._clientSession.aclose()


    async def _VKReq(self, method: str, params: dict = None, HTTPMethod: str = "GET") -> Union[dict, None]:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = {}

        else:
            limit = params.get("count")

            if limit:
                if limit < 0:
                    params["count"] = 300

        if "." not in method:
            method = "audio." + method

        url = VKAPI + method
        fullParams = {**params, **self._defaultParams}

        req = await self._client.sendReq(url, fullParams, method=HTTPMethod)

        while isinstance(req, dict) and req.get("error"):
            error = req.get("error")
            errorCode = error.get("error_code")

            if errorCode == 3:
                return self._raiseError("VKInvalidMethod")

            elif errorCode == 5:
                self._raiseError("VKInvalidToken")

            elif errorCode in [6, 9]:
                return self._raiseError("tooHighRequestSendingRate")

            elif errorCode == 10 and method == "createChatPlaylist":
                return self._raiseError("chatNotFound")

            elif errorCode == 14:
                captchaImg = error.get("captcha_img")
                if self._RuCaptchaKey:
                    solve = await self._solveCaptcha(captchaImg)

                else:
                    solve = input(captchaImg + "\nВведите решение капчи: ")

                fullParams.update({"captcha_sid": error.get("captcha_sid"), "captcha_key": solve})

                req = await self._client.sendReq(url, fullParams)

            elif errorCode in [15, 201, 203]:
                if ": can not restore too late" in error.get("error_msg"):
                    return self._raiseError("trackRestorationTimeEnded")

                else:
                    return self._raiseError("accessDenied")

            elif errorCode == 18:
                return self._raiseError("userWasDeletedOrBanned")

            elif errorCode == 104:
                return self._raiseError("notFound")

            else:
                return error

        if isinstance(req, list) and len(req) == 1:
            req = req[0]

        return req


    async def _solveCaptcha(self, captchaImg: str) -> str:
        imageBytes = await self._client.sendReq(captchaImg, responseType="file")
        captchaImageInBase64 = base64.b64encode(imageBytes).decode("utf-8")

        RuCaptchaParams = {
            "clientKey": self._RuCaptchaKey,
            "task": {
                "type": "ImageToTextTask",
                "body": captchaImageInBase64
            },
            "languagePool": "rn"
        }

        taskId = (await self._client.sendReq(RuCaptchaAPI + "createTask", json=RuCaptchaParams, method="POST")).get("taskId")

        while True:
            await asyncio.sleep(5)
            taskResult = await self._client.sendReq(RuCaptchaAPI + "getTaskResult", json={"clientKey": self._RuCaptchaKey, "taskId": taskId}, method="POST")
            errorId = taskResult.get("errorId")

            if errorId == 0 and taskResult.get("status") == "ready":
                return taskResult.get("solution").get("text")

            elif errorId == 1:
                self._raiseError("RuCaptchaInvalidKey")

            elif errorId == 10:
                self._raiseError("RuCaptchaZeroBalance")

            elif errorId == 12:
                taskId = (await self._client.sendReq(RuCaptchaAPI + "createTask", json=RuCaptchaParams, method="POST")).get("taskId")

            elif errorId == 21:
                self._raiseError("RuCaptchaBannedIP")

            elif errorId == 55:
                self._raiseError("RuCaptchaBannedAccount")


    def _raiseError(self, errorType: Union[str, None]) -> Union[Error, None]:
        if not errorType:
            return

        if errorType not in errorsDict:
            errorType = "unknown"

        errorClass = createErrorClass(errorType)

        error = errorsDict.get(errorType)
        errorText = getattr(error, self._errorsLanguage) if self._errorsLanguage else "🇷🇺: " + error.ru + " 🇬🇧: " + error.en

        if error.critical:
            raise errorClass(errorText)

        return Error(error.code, errorClass.__name__, errorText)


    def _finalizeResponse(self, response: Union[List[dict], dict], objectType: Type[Union[Artist, Album, Track, Playlist]]) -> Union[List[Union[Artist, Album, Track, Playlist]], None]:
        if not (response or response is False):
            return

        if not isinstance(response, list):
            response = [response]

        for index, obj in enumerate(response):
            if objectType is Playlist:
                playlistType = obj.get("type")

                if playlistType in [0, 5]:
                    obj = objectType(obj, False if obj.get("original") else True, self)

                elif playlistType == 1:
                    obj = Album(obj, True, self)

            else:
                obj = objectType(obj, self)

            response[index] = obj

        return response if len(response) > 1 else response[0]