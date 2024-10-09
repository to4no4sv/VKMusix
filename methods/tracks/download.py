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

class Download:
    from typing import Union

    from vkmusix.aio import asyncFunction
    from vkmusix.types import Track

    @asyncFunction
    async def download(self, ownerId: int = None, trackId: int = None, filename: str = None, directory: str = None, track: Track = None) -> Union[str, None]:
        """
        Загружает аудиотрек в формате MP3.

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int, необязательно)
        :param trackId: идентификатор аудиотрека, информацию о котором необходимо получить. (int, необязательно)
        :param filename: название файла с аудиотреком. (str, по умолчанию `{artist} -- {title}`)
        :param directory: путь к директории, в которую загрузить файл. (str, по умолчанию `os.getcwd()`)
        :param track: объект класса `Track`, представляющий аудиотрек. (Track, необязательно)
        :return: полный путь к загруженному файлу, если аудиотрек успешно загружен, иначе `None`.
        """

        from asyncio import create_task, gather

        import re

        import os
        import aiofiles
        import aiofiles.os

        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad

        import av

        from vkmusix.types import Track

        if not any((all((ownerId, trackId)), all((track, isinstance(track, Track))))):
            return

        if not track or not track.fileUrl:
            if track:
                ownerId, trackId = track.ownerId, track.trackId

            track = await self.get(ownerId, trackId)
            if not track.fileUrl:
                return

        async def downloadSegment(segmentUrlLocal: str, keyLocal: str, ivLocal: bytes) -> None:
            segmentData = await self._client.req(segmentUrlLocal, responseType="response")
            while segmentData.status_code in (301, 302):
                segmentData = await self._client.req(segmentData.headers.get("Location"), responseType="response")

            if segmentData.status_code != 200:
                return

            segmentData = segmentData.content

            if keyLocal:
                if len(segmentData) % AES.block_size != 0:
                    segmentData = pad(segmentData, AES.block_size)

                decryptor = AES.new(keyLocal, AES.MODE_CBC, ivLocal)
                decryptedData = decryptor.decrypt(segmentData)
                segmentData = decryptedData

            return segmentData

        if not directory:
            directory = os.getcwd()

        else:
            os.makedirs(directory, exist_ok=True)

        filename = (filename if not filename.endswith(".mp3") else filename[:-4]) if filename else f"{track.artist} -- {track.title}"
        filename = re.sub(r'[<>:"/\\|?*]', str(), filename)
        filename = os.path.join(directory, filename)

        key = None
        iv = bytes.fromhex("00000000000000000000000000000000")
        tasks = list()

        m3u8Content = await self._client.req(track.fileUrl, responseType="response")
        while m3u8Content.status_code in (301, 302):
            m3u8Content = await self._client.req(m3u8Content.headers.get("Location"), responseType="response")

        if m3u8Content.status_code != 200:
            return

        for line in m3u8Content.text.splitlines():
            if line.startswith("#EXT-X-KEY"):
                method = line.split("METHOD=")[1].split(",")[0]

                if method == "AES-128":
                    if not key:
                        keyUri = line.split('URI="')[1].split('"')[0]
                        response = await self._client.req(keyUri, responseType="response")
                        contentType = response.headers.get("content-type")
                        key = response.content if contentType and contentType == "application/octet-stream" else response.text.encode()

                    keyLocal = key

                elif method == "NONE":
                    keyLocal = None

            elif line.endswith((".ts", ".ts?siren=1")):
                segmentUrl = os.path.join(os.path.dirname(track.fileUrl), line)
                task = create_task(downloadSegment(str(segmentUrl), keyLocal, iv))
                tasks.append(task)

        segments = await gather(*tasks)

        async with aiofiles.open(f"{filename}.ts", "wb") as outfile:
            buffer = bytearray()
            for segment in segments:
                if not segment:
                    continue

                buffer.extend(segment)

                if len(buffer) > 10 * 1024 * 1024:
                    await outfile.write(buffer)
                    buffer.clear()

            if buffer:
                await outfile.write(buffer)

        try:
            inputContainer = av.open(f"{filename}.ts")
            outputContainer = av.open(f"{filename}.mp3", mode="w", format="mp3")

            inputStream = inputContainer.streams.audio[0]
            outputStream = outputContainer.add_stream("mp3", rate=inputStream.rate)
            outputStream.channels = inputStream.channels

            for packet in inputContainer.demux(inputStream):
                if packet.stream == inputStream and packet.stream_index == inputStream.index:
                    outputContainer.mux(packet)

            inputContainer.close()
            outputContainer.close()

        except av.InvalidDataError:
            return

        finally:
            await aiofiles.os.remove(f"{filename}.ts")

        return f"{filename}.mp3"