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

from .base import Base

class Section(Base):
    """
    Класс, представляющий раздел музыки owner'а (пользователь или группа).

    Атрибуты:
        title (str): название раздела.

        subsections (list[types.Section], optional): подразделы.

        tracks (list[types.Track], optional): треки раздела.

        playlists (list[types.Playlist], optional): плейлисты раздела.

        recommendedPlaylists (list[types.Playlist], optional): рекомендованные плейлисты.

        nextOffset (str, optional): значение оффсета для получения следующих результатов. Отсутствует, если результатов больше нету.

        id (str): идентификатор раздела.

        url (str): ссылка на раздел в web-версии ВКонтакте.

        raw (dict): необработанные данные, полученные от ВКонтакте.
    """

    from typing import Union, List

    from vkmusix.aio import async_
    from vkmusix.types import Track

    def __init__(self, section: dict, client: "Client" = None) -> None:
        from vkmusix.types import Track, Playlist

        super().__init__(client)

        sectionInfo = section.get("section", section)

        self.title = sectionInfo.get("title")

        subsections = sectionInfo.get("blocks")

        self.subsections = self._client._finalizeResponse(
            [subsection for subsection in subsections if subsection.get("data_type") not in ["none", "audio_stream_mixes"]],
            Section,
        ) if subsections else None

        tracks = section.get("audios")

        if not tracks:
            ids = section.get("audios_ids")

            if ids:
                tracks = [
                    {
                        "owner_id": ownerId,
                        "track_id": trackId,
                    }
                    for id in ids
                    for ownerId, trackId in [id.split("_")]
                ]

        self.tracks = self._client._finalizeResponse(
            tracks,
            Track,
        )

        playlists = section.get("playlists")

        if not playlists:
            ids = section.get("playlists_ids")

            if ids:
                playlists = [
                    {
                        "owner_id": ownerId,
                        "playlist_id": playlistId,
                    }
                    for id in ids
                    for ownerId, playlistId in [id.split("_")]
                ]

        self.playlists = self._client._finalizeResponse(
            playlists,
            Playlist,
        )

        self.recommendedPlaylists = self._client._finalizeResponse(
            section.get("recommended_playlists"),
            Playlist,
        )

        self.nextOffset = sectionInfo.get("next_from")

        self.id = sectionInfo.get("id")
        self.url = sectionInfo.get("url")

        if self.subsections:
            if len(self.subsections) == 1 and self.subsections[0].id == self.id:
                self.subsections = None

            else:
                self.subsections = [subsection for subsection in self.subsections if subsection.id != self.id]

        self.raw = section


    @async_
    async def get(self, offset: str = None) -> "Section":
        """
        Получает информацию о разделе музыки.

        `Пример использования`:

        section = section.get()

        print(section)

        :param offset: уникальное значение, содержащееся в атрибуте ``nextOffset`` объекта класса ``types.Section``. Необходимо для получения следующих результатов в разделе. (``str``, `optional`)
        :return: `При успехе`: информация о разделе музыки (``types.Section``). `Если раздел не найден`: ``None``.
        """

        return await self._client.getSection(
            self.id,
            offset,
        )


    @async_
    async def getTracks(self) -> Union[List[Track], None]:
        """
        Получает треки из раздела музыки.

        `Пример использования`:

        tracks = section.getTracks()

        print(tracks)

        :return: `При успехе`: треки (``list[types.Track]``). `Если раздел не найден или треки отсутствуют`: ``None``.
        """

        return await self._client.getTracks(
            self.id,
        )

    get_tracks = getTracks