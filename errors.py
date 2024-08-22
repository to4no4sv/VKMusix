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


from .encoder import _BaseModel


errorsDict = {
    "unknown": ("Неизвестная ошибка.", "Unknown error.", True),

    "outdated1": ("Устаревшая ошибка.", "Outdated error."),
    "outdated2": ("Устаревшая ошибка.", "Outdated error."),

    "sessionClosed": ("Текущая сессия закрыта. Для отправки новых запросов потребуется создать новый объект класса `Client`", "The current session is closed. To send new requests, you need to create a new instance of the `Client` class.", True),

    "VKInvalidToken": ("Недействительный токен ВКонтакте.", "Invalid VKontakte token.", True),
    "VKCookieFileNotFound": ("Файл с расширением .VKCookie не найден. Если он ещё не создан, введите логин и пароль от аккаунта.", "The file with the .VKCookie extension was not found. If it hasn't been created yet, please enter the login and password for the account.", True),
    "VKInvalidCookie": ("В файле с расширением .VKCookie были недействительные cookie. Пожалуйста, перезапустите Ваш код.", "The file with the .VKCookie extension contained invalid cookies. Please restart your code.", True),
    "VKUnsuccessfulLoginAttempt": ("Неудачная попытка входа в ВКонтакте. Проверьте введённые `login` и (или) `password`.", "Unsuccessful login attempt on VKontakte. Please check the entered `login` and/or `password`.", True),

    "RuCaptchaInvalidKey": ("Недействительный ключ RuCaptcha.", "Invalid RuCaptcha key.", True),
    "RuCaptchaZeroBalance": ("Отсутствие средств на балансе RuCaptcha.", "Insufficient funds on RuCaptcha balance.", True),
    "RuCaptchaBannedIP": ("IP заблокирован на RuCaptcha.", "IP blocked on RuCaptcha.", True),
    "RuCaptchaBannedAccount": ("Аккаунт заблокирован на RuCaptcha.", "Account blocked on RuCaptcha.", True),

    "VKInvalidMethod": ("Некорректный метод.", "Invalid method specified."),
    "userWasDeletedOrBanned": ("Пользователь удалён или заблокирован.", "User was deleted or banned."),
    "trackRestorationTimeEnded": ("Время, в течение которого восстановление аудиотрека было возможно, закончилось.", "The time during which track restoration was possible has ended."),
    "accessDenied": ("Недостаточно прав доступа для совершения этого действия.", "Insufficient permissions to perform this action."),
    "accessDeniedWithoutCookie": ("Для совершения этого действия необходимо войти в аккаунт (Указать cookie при создании `Client`).", "To perform this action, you need to log in (Specify cookies when creating `Client`)."),

    "notFound": ("Объект не найден. Проверьте введённые данные.", "Object not found. Please check the entered data"),
    "chatNotFound": ("Чат не найден. Проверьте введённый `chatId`.", "Chat not found. Please check the entered `chatId`."),
    "artistNotFound": ("Артист не найден. Проверьте введённый `artistId`.", "Artist not found. Please check the entered `artistId`."),
    "albumNotFound": ("Альбом не найден. Проверьте введённые `ownerId` и (или) `albumId`.", "Album not found. Please check the entered `ownerId` and/or `albumId`."),
    "trackNotFound": ("Аудиотрек не найден. Проверьте введённые `ownerId` и (или) `trackId`", "Track not found. Please check the entered `ownerId` and/or `trackId`."),
    "playlistNotFound": ("Плейлист не найден. Проверьте введённые `ownerId` (`groupId`) и (или) `playlistId`", "Playlist not found. Please check the entered `ownerId` and/or `playlistId`."),

    "ownerIdsAndTrackIdsTypeDifferent": ("Типы `ownerIds` и `trackIds` не могут отличаться.", "The types of `ownerIds` and `trackIds` must be the same."),
    "ownerIdsAndTrackIdsLenDifferent": ("Длины `ownerIds` и `trackIds` не могут отличаться.", "The lengths of `ownerIds` and `trackIds` must be the same."),

    "noneQuery": ("Не указана строка для поиска.", "Search string not specified."),

    "trackReorderNeedsBeforeOrAfterArgument": ("Для изменения порядка аудиотрека необходимо указать `beforeTrackId` или и `afterTrackId`.", "To change the order of the track, you need to specify either `beforeTrackId` or `afterTrackId`."),
    "trackReorderNeedsOnlyBeforOrAfterNotBoth": ("Для изменения порядка аудиотрека необоходимо указать `beforeTrackId` или `afterTrackId`, но не оба типа.", "To change the order of a track, you need to specify either `beforeTrackId`, or `afterTrackId`, but not both types."),

    "MP3FileNotFound": ("MP3-файл с аудиотреком не найден. Убедитесь, что вы указали правильное название файла.", "The MP3 file with the track was not found. Please make sure you have specified the correct filename.", True),
    "MP3FileTooBig": ("MP3-файл слишком большой. Максимальный размер 200 МБ", "MP3 file too big. Max size is 200 MB.", True),

    "tooHighRequestSendingRate": ("Слишком высокая частота отправки запросов.", "Too high request sending rate."),
}


class PreError:
    def __init__(self, code: int, critical: bool, ruText: str, enText: str) -> None:
        self.code = code
        self.critical = critical
        self.ru = ruText
        self.en = enText


for errorCode, (errorName, errorText) in enumerate(errorsDict.items()):
    errorsDict[errorName] = PreError(
        errorCode,
        errorText[2] if len(errorText) > 2 else False,
        errorText[0],
        errorText[1]
    )


class Error(_BaseModel):
    def __init__(self, code: int, title: str, message: str) -> None:
        super().__init__()
        self._code = code
        self._title = title
        self._message = message


def createErrorClass(errorType: str) -> any:
    return type(
        errorType,
        (Exception,),
        {"__init__": lambda self_, message: super(type(self_), self_).__init__(message)}
    )