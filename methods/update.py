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
import aiofiles

import os

import pytz
from datetime import datetime

from typing import Union, List, Tuple

from ..aio import asyncFunction
from ..errors import Error
from ..models import Track, Playlist
from ..config import moscowTz
from ..utils import checkFile


class Update:
    @asyncFunction
    async def upload(self, filename: str, title: str = None, artist: str = None, lyrics: str = None, genreId: int = None, removeFromSearchResults: bool = None, groupId: int = None) -> Union[Track, Error]:
        """
        Загружает новый аудиотрек во ВКонтакте.

        Пример загрузки файла с названием «prombl — zapreti.mp3»:\n
        result = client.upload(filename="prombl — zapreti", title="zapreti", artist="prombl", lyrics="yourLyrics", removeFromSearchResults=True, groupId="yourGroupId")\n
        print(result)

        :param filename: имя MP3-файла, содержащего аудиотрек, который необходимо загрузить (без расширения). (str)
        :param title: название аудиотрека. (str, необязательно)
        :param artist: артист(ы) аудиотрека. (str, необязательно)
        :param lyrics: текст аудиотрека. (str, необязательно)
        :param genreId: жанр аудиотрека (в виде идентификатора). (int, необязательно)
        :param removeFromSearchResults: флаг, указывающий, будет ли аудиотрек скрыт из поисковой выдачи. (bool, необязательно)
        :param groupId: идентификатор группы, в музыку которой необходимо загрузить аудиотрек (int, необязательно)
        :return: загруженный аудиотрек в виде объекта модели `Track`.
        """

        if filename.endswith(".mp3"):
            filename = filename[:-4]

        filename = checkFile(filename + ".mp3")
        if not filename:
            self._raiseError("MP3FileNotFound")

        fileSizeInBytes = os.path.getsize(filename)
        fileSizeInMB = fileSizeInBytes / (1024 * 1024)

        if fileSizeInMB > 200:
            self._raiseError("MP3FileTooBig")

        uploadUrl = (await self._VKReq("getUploadServer")).get("upload_url")

        async with aiofiles.open(filename, "rb") as file:
            fileContent = await file.read()

        uploadingFileResponse = await self._client.sendReq(uploadUrl, files={"file": (filename, fileContent, "audio/mpeg")}, method="POST")

        server = uploadingFileResponse.get("server")
        audio = uploadingFileResponse.get("audio")
        hash = uploadingFileResponse.get("hash")

        track = await self._VKReq("save", {"server": server, "audio": audio, "hash": hash, "title": title, "artist": artist})
        if isinstance(track, Error):
            return track

        track = Track(track)

        if any((lyrics, genreId, removeFromSearchResults)):
            await self.edit(track.ownerId, track.trackId, lyrics=lyrics, genreId=genreId, removeFromSearchResults=removeFromSearchResults)
            track = await self.get(track.ownerId, track.trackId, True)

        if groupId:
            await self.add(track.ownerId, track.trackId, groupId=groupId)
            await self.remove(track.ownerId, track.trackId)

        return track


    @asyncFunction
    async def add(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], playlistId: int = None, groupId: int = None) -> Union[Tuple[Union[bool, Error]], Error]:
        """
        Добавляет аудиотрек в музыку или плейлист пользователя или группы.

        Пример использования:\n
        result = client.add(ownerIds=474499244, trackIds=456638035, playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо добавить. (int или list)
        :param playlistId: идентификатор плейлиста, в который необходимо добавить аудиотрек. (int, необязательно)
        :param groupId: идентификатор группы, в музыку или плейлист которой необходимо добавить аудиотрек. (int, необязательно)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно добавлен(ы), `False` в противном случае.
        """

        if type(ownerIds) != type(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        if isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        if not (isinstance(ownerIds, list) and isinstance(trackIds, list)):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        if playlistId:
            method = "addToPlaylist"

        else:
            method = "add"

        results = []
        for ownerId, trackId in zip(ownerIds, trackIds):
            response = await self._VKReq(method, {**({"owner_id": ownerId, "audio_id": trackId, "group_id": groupId} if not playlistId else {"owner_id": groupId, "audio_ids": f"{ownerId}_{trackId}"}), "playlist_id": playlistId})
            results.append(bool(response) if not isinstance(response, Error) else self._raiseError("playlistNotFound"))

        return tuple(results)


    @asyncFunction
    async def remove(self, ownerIds: Union[int, List[int]], trackIds: Union[int, List[int]], playlistId: int = None, groupId: int = None, reValidateIds: bool = True) -> Union[Tuple[Union[bool, Error]], Error]:
        """
        Удаляет аудиотрек из музыки или плейлиста пользователя или группы.

        Пример использования:\n
        result = client.remove(ownerIds=474499244, trackIds=456638035, playlistId="yourPlaylistId", groupId="yourGroupId", reValidateIds=False)\n
        print(result)

        :param ownerIds: идентификатор(ы) владельца аудиотрека(ов) (пользователь или группа). (int или list)
        :param trackIds: идентификатор(ы) аудиотрека(ов), который(е) необходимо удалить. (int или list)
        :param playlistId: идентификатор плейлиста, из которого необходимо удалить аудиотрек(и). (int, необязательно, метод временно не работает для плейлистов, привязанных к чату)
        :param groupId: идентификатор группы, из музыки или плейлиста которой необходимо удалить аудиотрек(и). (int, необязательно)
        :param reValidateIds: флаг, указывающий, необходимо ли перепроверить идентификатор(ы) аудитрека(ов) по находящимся в плейлисте. (bool, по умолчанию `True`)
        :return: кортеж, состоящий из `True`, если аудиотрек(и) успешно удалён(ы), `False` в противном случае.
        """

        if type(ownerIds) != type(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsTypeDifferent")

        if isinstance(ownerIds, list) and isinstance(trackIds, list) and len(ownerIds) != len(trackIds):
            return self._raiseError("ownerIdsAndTrackIdsLenDifferent")

        if not (isinstance(ownerIds, list) and isinstance(trackIds, list)):
            ownerIds = [ownerIds]
            trackIds = [trackIds]

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        if reValidateIds:
            if playlistId:
                playlist = await self.getPlaylist(playlistId, groupId, includeTracks=True)
                if isinstance(playlist, Error):
                    return playlist

                existTracks = playlist.tracks

            else:
                existTracks = await self.getTracks(groupId)

            if not existTracks and playlistId:
                return (False,)

            for index, (ownerId, trackId) in enumerate(zip(ownerIds, trackIds)):
                if not playlistId:
                    continue

                track = await self.get(ownerId, trackId)

                if isinstance(track, Error):
                    continue

                trackTitle = track.title
                trackArtists = track.artists
                if not trackArtists:
                    trackArtists = track.artist

                for existTrack in existTracks:
                    if isinstance(existTrack, Error):
                        continue

                    existTrackTitle = existTrack.title
                    existTrackArtists = existTrack.artists
                    if not existTrackArtists:
                        existTrackArtists = existTrack.artist

                    existTrackOwnerId = existTrack.ownerId
                    existTrackId = existTrack.trackId

                    if existTrackTitle == trackTitle and existTrackArtists == trackArtists:
                        ownerIds[index] = existTrackOwnerId
                        trackIds[index] = existTrackId
                        break

        deleteSemaphore = asyncio.Semaphore(2)
        if playlistId:
            if groupId > 0:
                groupId = -groupId

            async def removeTrackFromPlaylist(id: str, semaphore: asyncio.Semaphore) -> bool:
                async with semaphore:
                    response = await self._VKReq("removeFromPlaylist", {"audio_ids": id, "owner_id": groupId, "playlist_id": playlistId})
                    return bool(response) if not isinstance(response, Error) else response

            tasks = [removeTrackFromPlaylist(f"{ownerId}_{trackId}", deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        else:
            async def removeTrack(ownerId: int, trackId: int, semaphore: asyncio.Semaphore) -> bool:
                async with semaphore:
                    response = await self._VKReq("delete", {"owner_id": ownerId, "audio_id": trackId, "group_id": groupId})
                    return bool(response) if not isinstance(response, Error) else response

            tasks = [removeTrack(ownerId, trackId, deleteSemaphore) for ownerId, trackId in zip(ownerIds, trackIds)]

        return tuple(await asyncio.gather(*tasks))


    @asyncFunction
    async def edit(self, ownerId: int, trackId: int, title: Union[str, int] = None, artist: Union[str, int] = None, lyrics: Union[str, int] = None, genreId: int = None, removeFromSearchResults: bool = None) -> Union[bool, Error]:
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

        response = await self._VKReq("edit", {"owner_id": ownerId, "audio_id": trackId,
            **({"title": title} if title else {}),
            **({"artist": artist} if artist else {}),
            **({"lyrics": lyrics} if lyrics is not None else {}),
            **({"genre_id": genreId} if genreId is not None else {}),
            **({"no_search": removeFromSearchResults} if removeFromSearchResults is not None else {})
        })

        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def restore(self, ownerId: int, trackId: int) -> Union[bool, Error]:
        """
        Восстанавливает удалённый аудиотрек.

        Пример использования:\n
        result = client.restore(ownerId="yourOwnerId", trackId="yourTrackId")\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int)
        :param trackId: идентификатор аудиотрека, который необходимо восстановить. (int)
        :return: `True`, если аудиотрек успешно восстановлен, `False` в противном случае.
        """

        response = await self._VKReq("restore", {"owner_id": ownerId, "audio_id": trackId})

        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def createPlaylist(self, title: Union[str, int], description: Union[str, int] = None, photo: str = None, groupId: int = None, chatId: int = None) -> Union[int, Error, None]:
        """
        Создаёт плейлист в музыке пользователя или группы.

        Пример использования:\n
        result = client.createPlaylist(title="prombl — npc", description="Release Date: December 24, 2021", "photo"="yourPhotoUrl", "groupId"="yourGroupId", chatId="yourChatId")\n
        print(result)

        :param title: название плейлиста. (str)
        :param description: описание плейлиста. (str, необязательно)
        :param photo: фото плейлиста. (str, необязательно, временно не работает)
        :param groupId: идентификатор группы, в которой необходимо создать плейлист. (int, необязательно)
        :param chatId: идентификатор чата, к которому привязать плейлист. (int, формат: `2000000000 + идентификатор чата`)
        :return: идентификатор плейлиста или словарь с ключами `ownerId` и `playlistId` (если создаётся плейлист, привязанный к чату), если плейлист успешно создан, `None` в противном случае.
        """

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        if chatId:
            method = "createChatPlaylist"

        else:
            method = "createPlaylist"

        playlist = await self._VKReq(method, {"title": title, "description": description, "owner_id": groupId})
        playlistId = playlist.get("id")

        if playlistId:
            if chatId:
                playlistOwnerId = playlist.get("owner_id")
                return {"ownerId": playlistOwnerId, "playlistId": playlistId}

            return playlistId

            """if photo:
                await self._editPlaylistPhoto(playlistId, photo, groupId)"""

        return playlist


    @asyncFunction
    async def addPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None) -> Union[int, None, Error]:
        """
        Добавляет плейлист в музыку пользователя или группы.

        Пример использования:\n
        result = client.addPlaylist(playlistId=1, ownerId=-215973356, groupId="yourGroupId")\n
        print(result)

        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param playlistId: идентификатор плейлиста, который необходимо добавить. (int)
        :param groupId: идентификатор группы, в которую необходимо добавить плейлист. (int, необязательно)
        :return: идентификатор плейлиста, если плейлист успешно добавлен, `None` в противном случае.
        """

        if not ownerId:
            if not groupId:
                return None

            ownerId = (await self.getSelf()).get("id")

        response = await self._VKReq("followPlaylist", {"owner_id": ownerId, "playlist_id": playlistId, **({"group_id": groupId} if groupId else {})})
        return response.get("id") if not isinstance(response, Error) else response


    @asyncFunction
    async def removePlaylist(self, playlistId: int, groupId: int = None) -> Union[bool, Error]:
        """
        Удаляет плейлист из музыки пользователя или группы.

        Пример использования:\n
        result = client.removePlaylist(playlistId="yourPlaylistId", groupId="yourGroupId")\n
        print(result)

        :param playlistId: идентификатор плейлиста, который необходимо удалить. (int)
        :param groupId: идентификатор группы, из которой необходимо удалить плейлист. (int, необязательно)
        :return: `True`, если плейлист успешно удалён, `False` в противном случае.
        """

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        response = await self._VKReq("deletePlaylist", {"owner_id": groupId, "playlist_id": playlistId})
        return bool(response) if not isinstance(response, Error) else (response if response._code != 17 else self._raiseError("playlistNotFound"))


    async def _editPlaylistPhoto(self, playlistId: int, photo: str = None, groupId: int = None) -> Union[bool, Error]:
        if photo is None:
            return False

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        params = {"playlist_id": playlistId, "owner_id": groupId}
        if photo:
            method = "setPlaylistCoverPhoto"
            params = {**params, **{"photo": photo}}

        else:
            method = "deletePlaylistCoverPhoto"

        response = await self._VKReq(method, params)
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def editPlaylist(self, playlistId: int, title: Union[str, int] = None, description: Union[str, int] = None, photo: str = None, groupId: int = None) -> Union[bool, Error]:
        """
        Изменяет информацию плейлиста, принадлежащего пользователю или группе.

        Пример использования:\n
        result = client.editPlaylist(playlistId="yourPlaylistId", title="prombl — npc", description="Release Date: December 24, 2021", photo="yourPhotoUrl", groupId="yourGroupId")\n
        print(result)

        :param playlistId: идентификатор плейлиста, информацию которого необходимо изменить.
        :param title: новое название плейлиста. (Необязательно)
        :param description: новое описание плейлиста. (Необязательно)
        :param photo: новое фото плейлиста. (Необязательно)
        :param groupId: идентификатор группы, в которой находится плейлист. (Необязательно)
        :return: `True`, если информация плейлиста успешно обновлена, `False` в противном случае.
        """

        if not any((title, description is not None, photo is not None)):
            return False

        if not groupId:
            groupId = (await self.getSelf()).get("id")

        params = {
            "playlist_id": playlistId,
            "owner_id": groupId,
            **({"title": title} if title else {}),
            **({"description": description} if description is not None else {})
        }

        if not any(("title" in params, "description" in params, photo is not None)):
            return False

        else:
            if any(("title" in params, "description" in params)):
                response = await self._VKReq("editPlaylist", params)
                editInfoStatus = bool(response) if not isinstance(response, Error) else response

            else:
                editInfoStatus = None

        if any((editInfoStatus is True, editInfoStatus is None)) and photo is not None:
            editPhotoStatus = await self._editPlaylistPhoto(playlistId, photo, groupId)
            if editInfoStatus is None:
                editInfoStatus = editPhotoStatus

        return editInfoStatus


    @asyncFunction
    async def copyPlaylist(self, playlistId: int, ownerId: int = None, groupId: int = None, newTitle: Union[str, None] = str(), newDescription: Union[str, None] = str(), newPhoto: Union[str, None] = str()) -> Union[Playlist, None, Error]:
        """
        Копирует плейлист, принадлежий пользователю или группе в музыку пользователя или группы.

        Пример использования:\n
        result = client.copyPlaylist(playlistId=1, ownerId=-215973356, groupId="yourGroupId", newTitle=None, newDescription=None, newPhoto=None)\n
        print(result)

        :param playlistId: идентификатор плейлиста, который необходимо скопировать. (int)
        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param groupId: идентификатор группы, в которую необходимо скопировать плейлист. (int, необязательно)
        :param newTitle: новое название плейлиста, `None` для использования текущих даты и времени. (str или None, по умолчанию оригинальное название)
        :param newDescription: новое описание плейлиста, `None` для удаления описания. (str или None, по умолчанию оригинальное описание)
        :param newPhoto: новая обложка плейлиста, `None` для удаления обложки. (str или None, по умолчанию оригинальная обложка)
        :return: плейлист в виде объекта модели `Playlist` с атрибутами `ownerId`, `playlistId`, `id` и `url`, если плейлист успешно скопирован, `None` в противном случае.
        """

        if not ownerId:
            ownerId = (await self.getSelf()).get("id")

        playlist = await self.getPlaylist(playlistId, ownerId, True)
        if isinstance(playlist, Error):
            return playlist

        title = playlist.title
        description = playlist.description
        photo = playlist.photo

        if newTitle != str():
            title = newTitle if newTitle is not None else datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(moscowTz).strftime("%d.%m.%Y / %H:%M:%S")

        if newDescription != str():
            description = newDescription

        if newPhoto != str():
            photo = None

        elif photo:
            _, photo = photo.popitem()

        newPlaylistId = await self.createPlaylist(title, description, photo, groupId)
        if isinstance(newPlaylistId, Error):
            return newPlaylistId

        tracks = playlist.tracks
        if tracks:
            ownerIds, trackIds = zip(*[(track.ownerId, track.trackId) for track in tracks[::-1]])
            await self.add(list(ownerIds), list(trackIds), newPlaylistId, groupId)

        return Playlist({"owner_id": groupId or (await self.getSelf()).get("id"), "id": newPlaylistId})


    @asyncFunction
    async def reorder(self, trackId: int, beforeTrackId: int = None, afterTrackId: int = None) -> Union[bool, Error]:
        """
        Изменяет порядок аудиотрека в музыке пользователя. Должен быть заполнен один из типов аргументов на выбор: `beforeTrackId` или `afterTrackId`.

        Пример использования для перемещения на место перед определённым треком:\n
        result = client.reorder(trackId="yourTrackId", beforeTrackId="yourBeforeTrackId")\n
        print(result)

        Пример использования для перемещения на место после определённого трека:\n
        result = client.reorder(trackId="yourTrackId", afterTrackId="yourAfterTrackId")\n
        print(result)

        :param trackId: идентификатор аудиотрека, порядок которого необходимо изменить. (int)
        :param beforeTrackId: идентификатор аудиотрека перед которым необходимо поместить аудиотрек. (int, необязательно)
        :param afterTrackId: идентификатор аудиотрека после которого необходимо поместить аудиотрек. (int, необязательно)
        :return: `True`, если порядок трека успешно изменён, `False` в противном случае.
        """

        if not any((beforeTrackId, afterTrackId)):
            return self._raiseError("trackReorderNeedsBeforeOrAfterArgument")

        if all((beforeTrackId, afterTrackId)):
            return self._raiseError("trackReorderNeedsOnlyBeforOrAfterNotBoth")

        response = await self._VKReq("reorder", {"audio_id": trackId, **({"before": beforeTrackId} if beforeTrackId else {"after": afterTrackId})})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def followArtist(self, artistId: int = None) -> Union[bool, Error]:
        """
        Подписывается на обновления музыки артиста.

        Пример использования:\n
        result = client.followArtist(artistId=5696274288194638935)\n
        print(result)

        :param artistId: идентификатор артиста, на обновления которого необходимо подписаться. (int)
        :return: `True`, если Вы успешно подписались на обновления музыки артиста, `False` в противном случае.
        """

        response = await self._VKReq("followArtist", {"artist_id": artistId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def unfollowArtist(self, artistId: int = None) -> Union[bool, Error]:
        """
        Отписывается от обновлений музыки артиста.

        Пример использования:\n
        result = client.unfollowArtist(artistId=5696274288194638935)\n
        print(result)

        :param artistId: идентификатор артиста, от обновлений которого необходимо отписаться. (int)
        :return: `True`, если Вы успешно отписались от обновлений музыки артиста, `False` в противном случае.
        """

        response = await self._VKReq("unfollowArtist", {"artist_id": artistId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def followCurator(self, curatorId: int = None) -> Union[bool, Error]:
        """
        Подписывается на обновления музыки куратора.

        Пример использования:\n
        result = client.followCurator(curatorId=28905875)\n
        print(result)

        :param curatorId: идентификатор куратора, на обновления которого необходимо подписаться. (int)
        :return: `True`, если Вы успешно подписались на обновления музыки куратора, `False` в противном случае.
        """

        response = await self._VKReq("followCurator", {"curator_id": curatorId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def unfollowCurator(self, curatorId: int = None) -> Union[bool, Error]:
        """
        Отписывается от обновлений музыки куратора.

        Пример использования:\n
        result = client.unfollowCurator(curatorId=28905875)\n
        print(result)

        :param curatorId: идентификатор куратора, от обновлений которого необходимо отписаться. (int)
        :return: `True`, если Вы успешно отписались от обновлений музыки куратора, `False` в противном случае.
        """

        response = await self._VKReq("unfollowCurator", {"curator_id": curatorId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def followOwner(self, ownerId: int = None) -> Union[bool, Error]:
        """
        Подписывается на обновления музыки пользователя или группы.

        Пример использования:\n
        result = client.followOwner(ownerId=-215973356)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, на обновления которого(ой) необходимо подписаться. (int)
        :return: `True`, если Вы успешно подписались на обновления музыки пользователя или группы, `False` в противном случае.
        """

        response = await self._VKReq("followOwner", {"owner_id": ownerId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def unfollowOwner(self, ownerId: int = None) -> Union[bool, Error]:
        """
        Отписывается от обновлений музыки пользователя или группы.

        Пример использования:\n
        result = client.unfollowOwner(ownerId=-215973356)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, от обновлений которого(ой) необходимо отписаться. (int)
        :return: `True`, если Вы успешно отписались на обновлений музыки пользователя или группы, `False` в противном случае.
        """

        response = await self._VKReq("followOwner", {"owner_id": ownerId})
        return bool(response) if not isinstance(response, Error) else response


    @asyncFunction
    async def setBroadcast(self, ownerId: int = None, trackId: int = None, groupIds: Union[List[str], str] = None) -> Union[bool, Error]:
        """
        Устанавливает (удаляет) аудиотрек в (из) статус(а) пользователя или группы.

        Пример использования для установки аудиотрека в статус пользователя:\n
        result = client.setBroadcast(ownerId=474499156, trackId=456637846)\n
        print(result)

        Пример использования для установки аудиотрека в статус группы:\n
        result = client.setBroadcast(ownerId=474499156, trackId=456637846, groupdIds="yourGroupId")\n
        print(result)

        Пример использования для удаления аудиотрека из статуса пользователя:\n
        result = client.setBroadcast()\n
        print(result)

        Пример использования для удаления аудиотрека из статуса группы:\n
        result = client.setBroadcast(groupdIds="yourGroupId")\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int, необязательно)
        :param trackId: идентификатор аудиотрека, который необходимо установить в статус. (int, необязательно)
        :param groupIds: идентификатор(ы) групп(ы), в (из) статус(а) которой необходимо установить (удалить) аудиотрек. (int, по умолчанию текущий пользователь)
        :return: `True`, если аудиотрек успешно установлен (удалён) в (из) статус(а), `False` в противном случае.
        """

        response = await self._VKReq("setBroadcast", {**({"audio": f"{ownerId}_{trackId}"} if ownerId and trackId else {}), **({"target_ids": groupIds} if groupIds else {})})
        return True if not isinstance(response, Error) else response