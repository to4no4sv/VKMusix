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

class Upload:
    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def upload(self, filename: str, title: str = None, artist: str = None, lyrics: str = None, genreId: int = None, removeFromSearchResults: bool = None, playlistId: int = None, groupId: int = None) -> Track:
        """
        Загружает новый аудиотрек во ВКонтакте.

        Пример загрузки файла с названием «prombl — zapreti.mp3»:\n
        result = client.upload(filename="prombl — zapreti", title="zapreti", artist="prombl", lyrics="yourLyrics", removeFromSearchResults=True, playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param filename: имя MP3-файла, содержащего аудиотрек, который необходимо загрузить (без расширения). (str)
        :param title: название аудиотрека. (str, необязательно)
        :param artist: артист(ы) аудиотрека. (str, необязательно)
        :param lyrics: текст аудиотрека. (str, необязательно)
        :param genreId: жанр аудиотрека (в виде идентификатора). (int, необязательно)
        :param removeFromSearchResults: флаг, указывающий, будет ли аудиотрек скрыт из поисковой выдачи. (bool, необязательно)
        :param playlistId: идентификатор плейлиста, в который необходимо загрузить аудиотрек. (int, необязательно)
        :param groupId: идентификатор группы, в музыку которой необходимо загрузить аудиотрек. (int, необязательно)
        :return: загруженный аудиотрек в виде объекта модели `Track`.
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
                "artist": artist
            }
        )

        track = self._finalizeResponse(track, Track)

        if any((lyrics, genreId, removeFromSearchResults)):
            await track.edit(lyrics=lyrics, genreId=genreId, removeFromSearchResults=removeFromSearchResults)
            track = await track.get(True)

        if any((playlistId, groupId)):
            await track.add(playlistId, groupId)
            await track.remove()

        return track