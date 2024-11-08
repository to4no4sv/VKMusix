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

class GetTracksFromChat:
    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Message

    @async_
    async def getTracksFromChat(self, chatId: int = None, groupId: int = None) -> Union[List[Message], None]:
        """
        Получает сообщения с треками из чата.

        `Пример использования`:

        messages = client.getTracksFromChat()

        print(messages)

        :param chatId: идентификатор чата. По умолчанию «Избранное». (``int``, `optional`)
        :param groupId: идентификатор группы, в которой находится чат. Только для личных сообщений группы. (``int``, `optional`)
        :return: `При успехе`: сообщения с треками (``list[types.Message]``). `Если чат не найден или сообщения с треками отсутствуют`: ``None``.
        """

        from vkmusix.types import Track, Message

        if not chatId:
            chatId = await self._getMyId()

        messages = (await self._req(
            "messages.getHistoryAttachments",
            {
                "media_type": "audio",
                "count": 200,
                "peer_id": chatId,
                **({
                       "group_id": groupId,
                } if groupId else dict()),
            },
            version=5.241,
        )).get("items")

        if not messages:
            return

        messages = messages[::-1]

        newMessages = dict()

        for idx, message in enumerate(messages):
            messageId = message.get("message_id")
            messageInfo = newMessages.get(messageId)

            track = self._finalizeResponse(
                message.get("attachment").get("audio"),
                Track,
            )

            if messageInfo:
                messageInfo.get("tracks").append(track)

            else:
                newMessages[messageId] = {
                    "tracks": [track],
                    "date": message.get("date"),
                    "from_id": message.get("from_id"),
                    "chat_id": chatId,
                    "message_id": messageId,
                }

        return [
            Message(message)
            for message in newMessages.values()
        ]

    get_tracks_from_chat = getTracksFromChat