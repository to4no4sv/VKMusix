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

from .base import Base

class Message(Base):
    """
    Класс, представляющий сообщение с треками.

    Атрибуты:
        tracks (list[types.Track]): треки из сообщения.

        date (datetime): дата и время отправки сообщения.

        fromId (int): идентификатор автора сообщения.

        chatId (int): идентификатор чата, в котором отправлено сообщение.

        id (int): идентификатор сообщения.

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    def __init__(self, message: dict) -> None:
        from vkmusix.utils import unixToDatetime

        self.tracks = message.get("tracks")

        self.date = unixToDatetime(message.get("date"))

        self.fromId = message.get("from_id")

        self.chatId = message.get("chat_id")

        self.id = message.get("message_id")

        self.raw = message