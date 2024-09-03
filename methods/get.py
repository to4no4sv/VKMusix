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

import asyncio
import os

import re

from typing import Type, Union, List

from ..aio import asyncFunction
from ..errors import Error
from ..models import Artist, Album, Track, Playlist
from ..config import VK, headers, playlistsPerReq, playlistsOwnerId


class Get:
    @asyncFunction
    async def get(self, ownerId: int, trackId: int, includeLyrics: bool = False) -> Union[Track, Error]:
        """
        Получает информацию об аудиотреке по его идентификатору.

        Пример использования:\n
        result = client.get(ownerId=474499244, trackId=456638035, includeLyrics=True)\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int)
        :param trackId: идентификатор аудиотрека, информацию о котором необходимо получить. (int)
        :param includeLyrics: флаг, указывающий, необходимо ли включать текст трека в ответ. (bool, по умолчанию `False`)
        :return: информация об аудиотреке в виде объекта модели `Track`.
        """

        id = f"{ownerId}_{trackId}"

        tasks = [self._VKReq("getById", {"audios": id})]

        if includeLyrics:
            tasks.append(self._VKReq("getLyrics", {"audio_id": id}))

        responses = await asyncio.gather(*tasks)

        track = responses[0]
        if not track:
            return self._raiseError("trackNotFound")

        if isinstance(track, Error):
            return track

        if includeLyrics:
            lyrics = responses[1]
            if not isinstance(lyrics, Error):
                lyrics = lyrics.get("lyrics")
                timestamps = lyrics.get("timestamps")

                track["lyrics"] = "\n".join([line.get("line") for line in timestamps if line.get("line") is not None] if timestamps else lyrics.get("text"))

            elif lyrics._code != 17:
                track["lyrics"] = lyrics

        return self._finalizeResponse(track, Track)


    @asyncFunction
    async def download(self, ownerId: int = None, trackId: int = None, filename: str = None, directory: str = os.getcwd(), track: "Track" = None) -> Union[bool, Error]:
        """
        Загружает аудиотрек в формате MP3.

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int, необязательно)
        :param trackId: идентификатор аудиотрека, информацию о котором необходимо получить. (int, необязательно)
        :param filename: название файла с аудиотреком. (str, по умолчанию `{artist} -- {title}`)
        :param directory: путь к директории, в которой сохранить файл. (str, по умолчанию `os.getcwd()`)
        :param track: объект класса `Track`, представляющий аудиотрек. (Track, необязательно)
        :return: `True`, если аудиотрек успешно загружен, иначе `False`.
        """

        import os
        import aiofiles
        import aiofiles.os
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        import av

        if not any((all((ownerId, trackId)), all((track, isinstance(track, Track))))):
            return False

        if not track or not track.fileUrl:
            track = await self.get(ownerId, trackId)
            if isinstance(track, Error):
                return track

            if not track.fileUrl:
                return False

        filename = (filename if not filename.endswith(".mp3") else filename[:-4]) or f"{track.artist} -- {track.title}.mp3"
        filename = os.path.join(directory, filename)

        m3u8Content = await self._client.sendReq(track.fileUrl, responseType="code")

        async def downloadSegment(segmentUrlLocal: str, keyLocal: str, ivLocal: bytes) -> None:
            segmentData = await self._client.sendReq(segmentUrlLocal, responseType="file")

            if keyLocal:
                if len(segmentData) % AES.block_size != 0:
                    segmentData = pad(segmentData, AES.block_size)

                decryptor = AES.new(keyLocal.encode("utf-8"), AES.MODE_CBC, ivLocal)
                decryptedData = decryptor.decrypt(segmentData)
                segmentData = decryptedData

            return segmentData

        key = None
        iv = bytes.fromhex("00000000000000000000000000000000")
        tasks = list()

        for line in m3u8Content.splitlines():
            if line.startswith("#EXT-X-KEY"):
                method = line.split("METHOD=")[1].split(",")[0]

                if method == "AES-128":
                    if not key:
                        keyUri = line.split('URI="')[1].split('"')[0]
                        key = keyLocal = await self._client.sendReq(keyUri, responseType="code")

                    else:
                        keyLocal = key

                elif method == "NONE":
                    keyLocal = None

            elif line.endswith(".ts"):
                segmentUrl = os.path.join(os.path.dirname(track.fileUrl), line)
                task = asyncio.create_task(downloadSegment(str(segmentUrl), keyLocal, iv))
                tasks.append(task)

        segments = await asyncio.gather(*tasks)

        async with aiofiles.open(f"{filename}.ts", "wb") as outfile:
            for segment in segments:
                await outfile.write(segment)

        inputContainer = av.open(f"{filename}.ts")
        outputContainer = av.open(f"{filename}.mp3", mode="w", format="mp3")

        inputStream = inputContainer.streams.audio[0]
        outputContainer.add_stream("mp3", rate=inputStream.rate)

        for packet in inputContainer.demux(inputStream):
            outputContainer.mux(packet)

        outputContainer.close()

        await aiofiles.os.remove(f"{filename}.ts")

        return True


    @asyncFunction
    async def getTracks(self, groupId: int = None) -> Union[List[Track], Track, None, Error]:
        """
        Получает треки пользователя или группы по его (её) идентификатору. (Временно не работает)

        Пример использования:\n
        result = client.getTracks(groupId=-215973356)\n
        print(result)

        :param groupId: идентификатор пользователя или группы. (int, по умолчанию текущий пользователь)
        :return: список аудиотреков в виде объектов класса `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если треки отсутствуют).
        """

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        tracks = await self._client.sendReq(VK + "audios" + str(groupId), cookies=self._cookies if hasattr(self, "_cookies") else None, headers=headers, responseType="code")
        tracks = await self._getTracks(tracks)

        return tracks


    @asyncFunction
    async def getArtist(self, artistId: int, includeAlbums: bool = False, includeTracks: bool = False) -> Union[Artist, Error, None]:
        """
        Получает информацию об артисте по его идентификатору.

        Пример использования:\n
        result = client.getArtist(artistId=5696274288194638935, includeAlbums=True, includeTracks=True)\n
        print(result)

        :param artistId: идентификатор артиста, информацию о котором необходимо получить. (int)
        :param includeAlbums: флаг, указывающий, необходимо ли включать альбомы артиста в ответ. (bool, по умолчанию `False`)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки артиста в ответ. (bool, умолчанию `False`)
        :return: информация об артисте в виде объекта модели `Artist`, или None (если артист не найден).
        """

        if not artistId:
            return

        params = {"artist_id": artistId}

        tasks = [self._VKReq("getArtistById", params)]

        if includeAlbums:
            tasks.append(self._VKReq("getAlbumsByArtist", params))

        if includeTracks:
            tasks.append(self._VKReq("getAudiosByArtist", params))

        responses = await asyncio.gather(*tasks)

        artist = responses[0]
        if not artist.get("name"):
            return self._raiseError("artistNotFound")

        if isinstance(artist, Error):
            return artist

        if includeAlbums:
            albums = responses[1]

            artist["albums"] = albums.get("items") if not isinstance(albums, Error) else albums

        if includeTracks:
            tracks = responses[2 if includeAlbums else 1]

            artist["tracks"] = tracks.get("items") if not isinstance(tracks, Error) else tracks

        return self._finalizeResponse(artist, Artist)


    @asyncFunction
    async def getRelatedArtists(self, artistId: int, limit: int = 10) -> Union[List[Artist], Artist, None, Error]:
        """
        Получает похожих артистов.

        Пример использования:\n
        result = client.getRelatedArtists(artistId=5696274288194638935, limit=5)\n
        print(result)

        :param artistId: идентификатор артиста, похожих на которого необходимо получить. (int)
        :param limit: максимальное количество артистов, которое необходимо вернуть. (bool, по умолчанию 10)
        :return: список артистов в виде объектов модели `Artist`, артист в виде объекта модели `Artist` (если он единственственный), или None (если `artistId` неверный или похожие артисты отсутствуют).
        """

        return self._finalizeResponse((await self._VKReq("getRelatedArtistsById", {"artist_id": artistId, "count": limit})).get("artists"), Artist)


    async def _getTracks(self, tracks: str, objectType: Union[Type[Union[Album, Playlist]], None] = None) -> Union[List[Track], Error]:
        tracks = re.sub(r"\\/", "/", re.sub(r"false", "False", re.sub(r"true", "True", re.sub(r"null", "None", tracks))))
        
        try:
            tracks = eval(tracks[tracks.rfind("[["): tracks.rfind("]]") + 2]) if objectType else list()

        except SyntaxError:
            tracks = self._raiseError("accessDenied" + ("WithoutCookie" if not hasattr(self, "_cookies") else ""))

        if isinstance(tracks, list):
            for index, track in enumerate(tracks):
                if len(track) < 20:
                    tracks[index] = None
                    continue

                album = track[19]
                if album:
                    album.append(dict(zip(["photo_160", "photo_300"], track[14].split(",")[::-1])))

                tracks[index] = Track({"owner_id": track[1], "track_id": track[0], "title": track[3], "artist": track[4], "subtitle": track[16], "main_artists": track[17], "featured_artists": track[18], "duration": track[5], "album": {"owner_id": album[0], "album_id": album[1], **({"photo": album[3]} if len(album) == 4 else dict())} if album else dict(), "release_audio_id": track[-2]}, self)

            tracks = [track for track in tracks if track]

            if not tracks or all(track is None for track in tracks):
                tracks = None

        return tracks


    @asyncFunction
    async def getAlbum(self, ownerId: int, albumId: int, includeTracks: bool = False) -> Union[Album, Error]:
        """
        Получает информацию об альбоме по его идентификатору.

        Пример использования:\n
        result = client.getAlbum(ownerId=-2000837600, albumId=16837600, includeTracks=True)\n
        print(result)

        :param ownerId: идентификатор владельца альбома (пользователь или группа). (int)
        :param albumId: идентификатор альбома, информацию о котором необходимо получить. (int)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки альбома в ответ. (bool, по умолчанию `False`)
        :return: информация об альбоме в виде объекта модели `Album`.
        """

        tasks = [self._VKReq("getPlaylistById", {"owner_id": ownerId, "playlist_id": albumId})]

        if includeTracks:
            tasks.append(self._client.sendReq(VK + "music/album/" + f"{ownerId}_{albumId}", headers=headers, responseType="code"))

        responses = await asyncio.gather(*tasks)

        album = responses[0]
        if not album:
            return self._raiseError("albumNotFound")

        if isinstance(album, Error):
            return album

        if includeTracks:
            album["tracks"] = await self._getTracks(responses[1], Album)

        return self._finalizeResponse(album, Album)


    @asyncFunction
    async def getPlaylist(self, playlistId: int, ownerId: int = None, includeTracks: bool = False) -> Union[Playlist, Error]:
        """
        Получает информацию о плейлисте по его ID.

        Пример использования:\n
        result = client.getPlaylist(playlistId=1, ownerId=-215973356, includeTracks=True)\n
        print(result)

        :param playlistId: идентификатор плейлиста, информацию о котором необходимо получить. (int)
        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки плейлиста в ответ. (bool, по умолчанию `False`)
        :return: информация о плейлисте в виде объекта модели `Playlist`.
        """

        if not ownerId:
            ownerId = (await self.getSelf()).get("id")

        tasks = [self._VKReq("getPlaylistById", {"owner_id": ownerId, "playlist_id": playlistId})]

        if includeTracks:
            tasks.append(self._client.sendReq(VK + "music/playlist/" + f"{ownerId}_{playlistId}", cookies=self._cookies if hasattr(self, "_cookies") else None, headers=headers, responseType="code"))

        responses = await asyncio.gather(*tasks)

        playlist = responses[0]
        if not playlist:
            return self._raiseError("playlistNotFound")

        if isinstance(playlist, Error):
            return playlist

        if includeTracks:
            playlist["tracks"] = await self._getTracks(responses[1], Playlist)

        return self._finalizeResponse(playlist, Playlist)


    @asyncFunction
    async def getPlaylists(self, ownerId: int = None, playlistTypes: Union[str, List[str]] = ["own", "foreign", "album"]) -> Union[List[Union[Playlist, Album]], Playlist, Album, None, Error]:
        """
        Получает плейлисты пользователя или группы.

        Пример использования:\n
        result = client.getPlaylists(ownerId=-215973356, playlistTypes="own")\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, плейлисты которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :param playlistTypes: типы плейлистов, которые необходимо получить: `own` — принадлежащий пользователю или группе, `foreign` — не принадлежащий пользователю или группе, `album` — альбом. (str или list, по умолчанию ["own", "foreign", "album"])
        :return: список плейлистов в виде объектов модели `Playlist` или `Album`, плейлист в виде объекта модели `Playlist` или `Album` (если он единственственный), или `None` (если плейлисты отсутствуют).
        """

        if not ownerId:
            ownerId = (await self.getSelf()).get("id")

        if not isinstance(playlistTypes, list):
            playlistTypes = [playlistTypes]

        for index, playlistType in enumerate(playlistTypes):
            playlistTypes[index] = playlistType.lower()

        method, params = "getPlaylists", {"owner_id": ownerId, "count": playlistsPerReq}
        playlists_ = await self._VKReq(method, params)
        if isinstance(playlists_, Error):
            return playlists_

        playlists = [playlist for playlist in playlists_.get("items")]
        count = playlists_.get("count")
        offset = count if count < playlistsPerReq else playlistsPerReq

        if offset < count:
            tasks = []
            while offset < count:
                tasks.append(self._VKReq(method, {**params, **{"offset": offset}}))
                offset += playlistsPerReq

            playlists_ = await asyncio.gather(*tasks)
            for playlistGroup in playlists_:
                if isinstance(playlistGroup, Error):
                    continue

                for playlist in playlistGroup.get("items"):
                    playlists.append(playlist)

        playlists = self._finalizeResponse(playlists, Playlist)

        if not isinstance(playlists, list):
            playlists = [playlists]

        playlists = [playlist for playlist in playlists if (isinstance(playlist, Playlist) and ("own" if playlist.own else "foreign") in playlistTypes) or (isinstance(playlist, Album) and "album" in playlistTypes)]

        return (playlists if len(playlists) > 1 else playlists[0]) if playlists else None


    @asyncFunction
    async def getCuratorTracks(self, curatorId: int, limit: int = 10, offset: int = 0) -> Union[List[Track], Track, None, Error]:
        """
        Получает аудиотреки, принадлежащие куратору.

        Пример использования:\n
        result = client.getCuratorTracks(curatorId=28905875, limit=5)\n
        print(result)

        :param curatorId: идентификатор куратора (пользователь или группа). (int)
        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если неверный `curatorId` или аудиотреки отсутствуют).
        """

        return self._finalizeResponse((await self._VKReq("getAudiosByCurator", {"curator_id": curatorId, "count": limit, "offset": offset})).get("items"), Track)


    @asyncFunction
    async def getTracksFromFeed(self) -> Union[List[Track], Error]:
        """
        Получает все треки из новостной ленты.

        Пример использования:\n
        result = client.getTracksFromFeed()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track` с атрибутами `ownerId`, `trackId`, `id` и `url`.
        """

        tracks = (await self._VKReq("getAudioIdsBySource", {"source": "feed"})).get("audios")
        for index, track in enumerate(tracks):
            ownerId, trackId = track.get("audio_id").split("_")[:2]
            tracks[index] = {"owner_id": int(ownerId), "id": int(trackId)}

        return self._finalizeResponse(tracks, Track)


    @asyncFunction
    async def getRecommendations(self, limit: int = 10, offset: int = 0, ownerId: int = None, trackId: int = None) -> Union[List[Track], Track, None, Error]:
        """
        Получает рекомендации аудиотреков для пользователя или похожие на аудиотрек.

        Пример использования для рекомендаций пользователя:\n
        result = client.getRecommendations(limit=20)\n
        print(result)

        Пример использования для рекомендаций по аудиотреку:\n
        result = client.getRecommendations(limit=5, ownerId=474499156, trackId=456637846)\n
        print(result)

        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10, минимально для пользовательских рекомендаций 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа).
        :param trackId: идентификатор аудиотрека, похожие на который необходимо получить.
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если рекомендации или похожие треки отсутствуют).
        """

        if not all((ownerId, trackId)) and limit < 10:
            limit = 10

        return self._finalizeResponse((await self._VKReq("getRecommendations", {"count": limit, "offset": offset, **({"target_audio": f"{ownerId}_{trackId}"} if all((ownerId, trackId)) else {})})).get("items"), Track)


    @asyncFunction
    async def getNew(self) -> Union[List[Track], Error]:
        """
        Получает аудиотреки, вышедшие недавно.

        Пример использования:\n
        result = client.getNew()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track`.
        """

        playlist = await self.getPlaylist(2, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    @asyncFunction
    async def getPopular(self) -> Union[List[Track], Error]:
        """
        Получает популярные аудиотреки.

        Пример использования:\n
        result = client.getPopular()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track`.
        """

        playlist = await self.getPlaylist(1, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    @asyncFunction
    async def getEditorsPicks(self) -> Union[List[Track], Error]:
        """
        Получает аудиотреки, выбранные редакторами ВКонтакте.

        Пример использования:\n
        result = client.getEditorsPicks()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track`.
        """

        playlist = await self.getPlaylist(3, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    @asyncFunction
    async def getTrackCount(self, ownerId: int) -> Union[int, Error]:
        """
        Получает количество аудиотреков, принадлежащих этому пользователю или группе.

        Пример использования:\n
        result = client.getTrackCount(ownerId=-215973356)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы. (int)
        :return: количество аудиотреков, принадлежащих пользователю или группе, в виде целого числа.
        """

        return await self._VKReq("getCount", {"owner_id": ownerId})


    @asyncFunction
    async def getSearchTrends(self, limit: int = 10, offset: int = 0) -> Union[List[str], str, None, Error]:
        """
        Получает самые частые поисковые запросы в музыке.

        Пример использования:\n
        result = client.getSearchTrends(limit=5)\n
        print(result)

        :param limit: максимальное количество запросов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список самых частых поисковых запросов в музыке в виде строк, самый частый поисковой запрос в музыке в виде строки (если он единственный) или `None` (если поисковые запросы отсутствуют).
        """

        return [item.get("name") for item in (await self._VKReq("getSearchTrends", {"count": limit, "offset": offset})).get("items")]


    @asyncFunction
    async def getBroadcast(self, id: int = None) -> Union[Track, None, bool, Error]:
        """
        Получает аудиотрек, транслируемый в статус.

        Пример использования для текущего пользователя:\n
        result = client.getBroadcast()\n
        print(result)

        Пример использования для любого пользователя:\n
        result = client.getBroadcast(id=1)\n
        print(result)

        :param id: идентификатор пользователя или группы, аудиотрек из статуса которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :return: аудиотрек в виде объекта модели `Track`, `None` (если ничего не проигрывается), или `False` (если музыка не транслируется в статус, работает только для текущего пользователя).
        """

        broadcast = await self._VKReq("status.get", ({"user_id": id} if id > 0 else {"group_id": -id}) if id else None)
        if isinstance(broadcast, Error):
            return broadcast

        audio = broadcast.get("audio")
        if audio:
            return Track(audio, self)

        if not id or id == (await self.getSelf()).get("id"):
            isBroadcastEnabled = (await self._VKReq("getBroadcast")).get("enabled")
            if not bool(isBroadcastEnabled):
                return False

        return
