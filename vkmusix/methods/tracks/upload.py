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
from distutils.command.upload import upload


class Upload:
    from typing import Union

    from vkmusix.aio import async_
    from vkmusix.types import Track

    @async_
    async def upload(self, filename: str, title: str = None, artist: str = None, lyrics: str = None, genreId: int = None, removeFromSearchResults: bool = None, playlistId: int = None, groupId: int = None) -> Union[Track, None]:
        """
        Загружает новый трек во ВКонтакте.

        `Пример использования`:

        track = client.upload(
            filename="Маленький ярче — LARILARI",
            title="LARILARI",
            artist="Маленький ярче",
            genreId=21,
            removeFromSearchResults=True,
        )

        print(track)

        :param filename: путь к .MP3 (обязательно) файлу. (``str``)
        :param title: название трека. По умолчанию берётся из метаданных файла. (``str``, `optional`)
        :param artist: артисты трека. По умолчанию берётся из метаданных файла. (``str``, `optional`)
        :param lyrics: текст трека. (``str``, `optional`)
        :param genreId: идентификатор жанра трека. (``int``, `optional`)
        :param removeFromSearchResults: флаг, указывающий, необходимо ли исключить трек из поиска. По умолчанию ``False``. (``bool``, `optional`)
        :param playlistId: идентификатор плейлиста, в который необходимо добавить трек после загрузки. (``int``, `optional`)
        :param groupId: идентификатор группы, в плейлист или музыку которой необходимо добавить трек после загрузки. (``int``, `optional`)
        :return: `При успехе`: информация о загруженном треке (``types.Track``). `Если трек не удалось загрузить`: ``None``.
        """

        import os.path
        import aiofiles

        from vkmusix.types import Track
        from vkmusix.utils import checkFile

        if filename.endswith(".mp3"):
            filename = filename[:-4]

        filename = checkFile(f"{filename}.mp3")
        if not filename:
            self._raiseError("MP3FileNotFound")

        fileSizeInBytes = os.path.getsize(filename)
        fileSizeInMB = fileSizeInBytes / (1024 * 1024)

        if fileSizeInMB > 200:
            self._raiseError("MP3FileTooBig")

        uploadUrl = (await self._req("getUploadServer")).get("upload_url")

        async with aiofiles.open(filename, "rb") as file:
            fileContent = await file.read()

        uploadingFileResponse = await self._client.req(
            uploadUrl,
            files={
                "file": (
                    filename,
                    fileContent,
                    "audio/mpeg",
                ),
            },
            method="POST",
        )

        server = uploadingFileResponse.get("server")
        audio = uploadingFileResponse.get("audio")
        hash = uploadingFileResponse.get("hash")

        track = await self._req(
            "save",
            {
                "server": server,
                "audio": audio,
                "hash": hash,
                "title": title,
                "artist": artist,
            },
        )

        if not track or (isinstance(track, dict) and track.get("error_code")):
            return track

        track = self._finalizeResponse(
            track,
            Track,
        )

        if any((lyrics, genreId, removeFromSearchResults)):
            await track.edit(lyrics=lyrics, genreId=genreId, removeFromSearchResults=removeFromSearchResults)
            track = await track.get(True)

        if any((playlistId, groupId)):
            await track.add(playlistId, groupId)
            await track.remove()

        return track