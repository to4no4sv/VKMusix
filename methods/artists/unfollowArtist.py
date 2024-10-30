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

class UnfollowArtist:
    from vkmusix.aio import async_

    @async_
    async def unfollowArtist(self, artistId: int = None) -> bool:
        """
        Отписывается от обновлений музыки артиста.

        `Пример использования`:

        result = client.unfollowArtist(
            artistId=5696274288194638935,
        )

        print(result)

        :param artistId: идентификатор артиста. (``int``)
        :return: `При успехе`: ``True``. `Если артист не найден`: ``False``.
        """

        response = await self._req(
            "unfollowArtist",
            {
                "artist_id": artistId,
            },
        )

        return bool(response)

    unfollow_artist = unfollowArtist