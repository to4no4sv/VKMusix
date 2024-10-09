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

from .error import Error
from .unknown import Unknown

from .sessionClosed import SessionClosed

from .vkInvalidToken import VKInvalidToken
from .vkCookieFileNotFound import VKCookieFileNotFound
from .vkInvalidCookie import VKInvalidCookie
from .vkUnsuccessfulLoginAttempt import VKUnsuccessfulLoginAttempt

from .ruCaptchaInvalidKey import RuCaptchaInvalidKey
from .ruCaptchaZeroBalance import RuCaptchaZeroBalance
from .ruCaptchaBannedIP import RuCaptchaBannedIP
from .ruCaptchaBannedAccount import RuCaptchaBannedAccount

from .invalidMethod import InvalidMethod
from .accessDenied import AccessDenied
from .accessDeniedWithoutCookie import AccessDeniedWithoutCookie

from .userWasDeletedOrBanned import UserWasDeletedOrBanned
from .trackRestorationTimeEnded import TrackRestorationTimeEnded

from .notFound import NotFound
from .chatNotFound import ChatNotFound
from .artistNotFound import ArtistNotFound
from .albumNotFound import AlbumNotFound
from .trackNotFound import TrackNotFound
from .playlistNotFound import PlaylistNotFound

from .noneQuery import NoneQuery

from .ownerIdsAndTrackIdsTypeDifferent import OwnerIdsAndTrackIdsTypeDifferent
from .ownerIdsAndTrackIdsLenDifferent import OwnerIdsAndTrackIdsLenDifferent

from .trackReorderNeedsBeforeOrAfterArgument import TrackReorderNeedsBeforeOrAfterArgument
from .trackReorderNeedsOnlyBeforeOrAfterNotBoth import TrackReorderNeedsOnlyBeforeOrAfterNotBoth

from .mp3FileNotFound import MP3FileNotFound
from .mp3FileTooBig import MP3FileTooBig

from .tooHighRequestSendingRate import TooHighRequestSendingRate

from .proxyShouldBeDict import ProxyShouldBeDict
from .invalidProxyDict import InvalidProxyDict