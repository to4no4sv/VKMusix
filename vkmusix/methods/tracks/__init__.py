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

from .get import Get
from .getLyrics import GetLyrics
from .getRecommendations import GetRecommendations

from .add import Add
from .remove import Remove

from .upload import Upload
from .edit import Edit
from .restore import Restore

from .download import Download

from .getTracksFromFeed import GetTracksFromFeed
from .getTracksFromChat import GetTracksFromChat

from ._parseAPITracks import _ParseAPITracks
from ._parseWebTracks import _ParseWebTracks

class Tracks(
    Get,
    GetLyrics,
    GetRecommendations,

    Add,
    Remove,

    Upload,
    Edit,
    Restore,

    Download,

    GetTracksFromFeed,
    GetTracksFromChat,

    _ParseAPITracks,
    _ParseWebTracks,
):
    pass