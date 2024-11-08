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

class GetMusicFromPost:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import MusicFromPost

    @async_
    async def getMusicFromPost(self, postId: int, ownerId: int = None) -> Union[MusicFromPost, None]:
        """
        Получает музыку из поста.

        `Пример использования`:

        music = client.getMusicFromPost(
            postId=34450119,
            ownerId=-28905875,
        )

        print(music)

        :param postId: идентификатор поста. (``int``)
        :param ownerId: идентификатор owner'а (пользователь или группа). По умолчанию залогиненный пользователь. (``int``, `optional`)
        :return: `При успехе`: музыка из поста (``types.MusicFromPost``). `Если пост не найден или музыка отсутствует`: ``None``.
        """

        import asyncio

        import re

        from vkmusix.types import Album, Track, Playlist, MusicFromPost

        if not ownerId:
            ownerId = await self._getMyId()

        post = (await self._req(
            "wall.getById",
            {
                "posts": f"{ownerId}_{postId}",

            },
        )).get("items")

        if not post:
            return

        post = post[0]
        attachments = post.get("attachments")

        if not attachments:
            return

        tracks = list()
        playlists = list()
        playlistTasks = list()

        for attachment in attachments:
            type = attachment.get("type")

            if type == "audio":
                tracks.append(attachment.get("audio"))

            elif type == "link":
                link = attachment.get("link")
                url = link.get("url")

                if url.startswith("https://m.vk.com/audio?act=audio_playlist"):
                    match = re.search(r"audio_playlist(-?\d+)_(\d+)", url)
                    if not match:
                        continue

                    ownerId, playlistId = match.groups()

                    playlistTask = self.getPlaylist(
                        playlistId,
                        ownerId,
                    )

                    playlistTasks.append(playlistTask)

        if playlistTasks:
            playlists = await asyncio.gather(*playlistTasks)

            if playlists:
                playlists = [playlist for playlist in playlists if playlist]

        albums = [album for album in playlists if isinstance(album, Album)] if playlists else None
        playlists = [playlist for playlist in playlists if isinstance(playlist, Playlist)] if playlists else None

        return MusicFromPost(
            albums if albums else None,
            self._finalizeResponse(tracks, Track) if tracks else None,
            playlists if playlists else None,
        ) if any((albums, tracks, playlists)) else None

    get_music_from_post = getMusicFromPost