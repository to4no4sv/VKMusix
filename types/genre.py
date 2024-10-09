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

class Genre(Base):
    """
    Класс, представляющий жанр аудиотрека или альбома.

    Атрибуты:
        title (str): название жанра.\n
        id (str): идентификатор жанра.\n
    """

    def __init__(self, genre: dict = None, genreId: int = None, client: "Client" = None) -> None:
        super().__init__(client)

        if genreId:
            trackGenres = {
                1: "Рок",
                2: "Поп",
                3: "Рэп и Хип-хоп",
                4: "Расслабляющая",
                5: "House и Танцевальная",
                6: "Инструментальная",
                7: "Метал",
                8: "Дабстеп",
                10: "Drum & Bass",
                11: "Транс",
                12: "Шансон",
                13: "Этническая",
                14: "Акустическая",
                15: "Регги",
                16: "Классическая",
                17: "Инди-поп",
                18: "Другая",
                19: "Скит",
                21: "Альтернатива",
                22: "Электро-поп и Диско",
                1001: "Джаз и Блюз"
            }

            self.title = trackGenres.get(genreId, "Неизвестен")

            self.id = genreId

        else:
            self.title = genre.get("name")

            self.id = genre.get("id") or genre.get("genre_id")
