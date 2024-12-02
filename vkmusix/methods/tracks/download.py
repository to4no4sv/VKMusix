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

    from vkmusix.aio import async_
    from vkmusix.types import Track
    from vkmusix.enums import Extension

    @async_
    async def download(self, ownerId: int = None, trackId: int = None, filename: str = None, directory: str = None, extension: Extension = None, metadata: bool = False, track: Track = None) -> Union[str, None]:
        """
        Скачивает трек.

        `Пример использования`:

        from vkmusix.enums import Extension

        path = client.download(
            ownerId=-2001471901,
            trackId=123471901,
            extension=Extension.OPUS,
            metadata=True,
        )

        print(path)

        :param ownerId: идентификатор владельца трека. (``int``)
        :param trackId: идентификатор трека. (``int``)
        :param filename: имя файла с треком. По умолчанию ``{artist} — {fullTitle}``. Поддерживаемые переменные для динамического имени: ``artist``, ``title``, ``subtitle``, ``fullTitle``, ``album``. Пример динамического имени файла: ``{artist} - {title} ({album})``. (``str``, `optional`)
        :param directory: путь к директории, в которую загрузить трек. (``str``, `optional`)
        :param extension: расширение файла с треком. По умолчанию ``Extension.MP3``. (``enums.Extension``, `optional`)
        :param metadata: флаг, указывающий, необходимо ли добавить метаданные (артист, название, альбом, обложка) к файлу с треком. По умолчанию ``False``. Игнорируется, если параметр ``extension`` равен ``Extension.TS``. (``bool``, `optional`)
        :param track: трек. (``types.Track``, `optional`)
        :return: `При успехе`: полный путь к загруженному файлу (``str``). `Если трек не найден или недоступен для загрузки`: ``None``.
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
        from vkmusix.enums import Extension

        if not any((all((ownerId, trackId)), all((track, isinstance(track, Track))))):
            return

        if not track or not track.fileUrl:
            if track:
                ownerId, trackId = track.ownerId, track.trackId

            track = await self.get(ownerId, trackId)
            if not track.fileUrl:
                return

        async def downloadSegment(segmentUrlLocal: str, keyLocal: bytes, ivLocal: bytes) -> None:
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

        extension = extension.value if extension and isinstance(extension, Extension) else "mp3"

        if not filename:
            filename = f"{track.artist} — {track.fullTitle}"

        else:
            filename = filename if not filename.endswith(f".{extension}") else filename[:-(len(extension) + 1)]

            if "{subtitle}" in filename and not track.subtitle:
                filename = filename.replace("{subtitle}", str())
                filename = filename.strip()

            if "{album}" in filename and not track.album:
                filename = filename.replace("{album}", str())
                filename = filename.strip()

            filename = filename.format(
                artist=track.artist,
                title=track.title,
                subtitle=track.subtitle,
                fullTitle=track.fullTitle,
                album=track.album.title if track.album else None,
            )

        filename = re.sub(r'[<>:"/\\|?*]', str(), filename)
        filename = os.path.join(directory, filename)

        key = None
        iv = bytes.fromhex("00000000000000000000000000000000")
        tasks = list()

        while True:
            m3u8Content = await self._client.req(
                track.fileUrl,
                responseType="response",
            )

            if m3u8Content:
                break

        while m3u8Content.status_code in (301, 302):
            while True:
                m3u8Content = await self._client.req(
                    m3u8Content.headers.get("Location"),
                    responseType="response",
                )

                if m3u8Content:
                    break

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

        if extension != "ts":
            try:
                inputContainer = av.open(f"{filename}.ts")
                outputContainer = av.open(f"{filename}.{extension}", mode="w", format=extension)

                inputStream = inputContainer.streams.audio[0]
                outputStream = outputContainer.add_stream(extension, rate=inputStream.rate)

                if extension == "opus":
                    outputStream.codec_context.options = {
                        "strict": "experimental",
                    }

                for packet in inputContainer.demux(inputStream):
                    if packet.stream == inputStream and packet.stream_index == inputStream.index:
                        if extension == "opus":
                            if packet.size > 0:
                                try:
                                    for frame in packet.decode():
                                        newPacket = outputStream.encode(frame)

                                        if newPacket:
                                            outputContainer.mux(newPacket)

                                except av.error.InvalidDataError:
                                    pass
                        else:
                            outputContainer.mux(packet)

                inputContainer.close()
                outputContainer.close()

            except (av.InvalidDataError, av.ValueError, av.BlockingIOError):
                return

            finally:
                await aiofiles.os.remove(f"{filename}.ts")

            if metadata:
                album = track.album
                photo = album.photo if album else None

                coverData = await self._client.req(
                    photo.get(1200) or photo.get(600) or photo.get(300) or photo.get(270),
                    responseType="file",
                ) if photo else None

                if extension == "mp3":
                    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
                    from mutagen.mp3 import MP3

                    audio = MP3(f"{filename}.{extension}", ID3=ID3)
                    audio.update(
                        {
                            **{
                                "TIT2": TIT2(encoding=1, text=[track.fullTitle]),
                                "TPE1": TPE1(encoding=1, text=[track.artist]),
                            },
                            **({
                                "TALB": TALB(encoding=1, text=[album.title]),
                            } if album else dict()),
                        },
                    )

                    if coverData:
                        audio.tags.add(
                            APIC(
                                encoding=1,
                                mime="image/jpeg",
                                type=3,
                                data=coverData,
                            )
                        )

                elif extension == "opus":
                    from mutagen.oggopus import OggOpus

                    audio = OggOpus(f"{filename}.{extension}")
                    audio.update(
                        {
                            "title": track.fullTitle,
                            "artist": track.artist,
                            **({
                                "album": album.title,
                            } if album else dict()),
                        },
                    )

                    if coverData:
                        import base64
                        from mutagen.flac import Picture

                        picture = Picture()

                        picture.data = coverData

                        picture.type = 3
                        picture.mime = "image/jpeg"

                        resolution = next((x for x in [1200, 600, 300, 270] if photo.get(x)), 1200)
                        picture.width = resolution
                        picture.height = resolution

                        picture.depth = 24

                        encodedPicture = base64.b64encode(picture.write()).decode("ascii")
                        audio["metadata_block_picture"] = [encodedPicture]

                audio.save()

        return f"{filename}.{extension}"