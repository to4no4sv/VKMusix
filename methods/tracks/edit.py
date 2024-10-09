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

class Edit:
    from typing import Union

    from vkmusix.aio import asyncFunction

    @asyncFunction
    async def edit(self, ownerId: int, trackId: int, title: Union[str, int] = None, artist: Union[str, int] = None, lyrics: Union[str, int] = None, genreId: int = None, removeFromSearchResults: bool = None) -> bool:
        """
        Изменяет информацию об аудиотреке.

        Пример использования:\n
        result = client.edit(ownerId="yourOwnerId", trackId="yourTrackId", title="zapreti", artist="prombl", "lyrics"=str(), "genreId"=3, removeFromSearchResults=True)\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int)
        :param trackId: идентификатор аудиотрека, информацию которого необходимо изменить. (int)
        :param title: новое название аудиотрека. (str, необязательно)
        :param artist: новый(е) артист(ы) аудиотрека. (str, необязательно)
        :param lyrics: новый текст аудиотрека. (str, необязательно)
        :param genreId: новый жанр аудиотрека (в виде идентификатора). (int, необязательно)
        :param removeFromSearchResults: флаг, указывающий, будет ли аудиотрек скрыт из поисковой выдачи. (bool, необязательно)
        :return: `True`, если информация аудиотрека успешно обновлена, `False` в противном случае.
        """

        if not any((title, artist, lyrics is not None, genreId is not None, removeFromSearchResults is not None)):
            return False

        response = await self._req(
            "edit",
            {
                "owner_id": ownerId,
                "audio_id": trackId,
                **({"title": title} if title else dict()),
                **({"artist": artist} if artist else dict()),
                **({"lyrics": lyrics} if lyrics is not None else dict()),
                **({"genre_id": genreId} if genreId is not None else dict()),
                **({"no_search": removeFromSearchResults} if removeFromSearchResults is not None else dict())
            }
        )

        return bool(response)