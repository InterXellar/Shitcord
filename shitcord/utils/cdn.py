# -*- coding: utf-8 -*-

import base64
import enum

BASE_URL = 'https://cdn.discordapp.com/'


class Endpoints(enum.Enum):
    CUSTOM_EMOJI = ({'png', 'gif'}, 'emojis/{emoji}.{type}')
    GUILD_ICON = ({'png', 'jpeg', 'webp'}, 'icons/{guild}/{hash}.{type}')
    GUILD_SPLASH = ({'png', 'jpeg', 'webp'}, 'splashes/{guild}/{hash}.{type}')
    DEFAULT_USER_AVATAR = ({'png'}, 'embed/avatars/{discriminator}.{type}')
    USER_AVATAR = ({'png', 'jpeg', 'webp', 'gif'}, 'avatars/{user}/{hash}.{type}')
    APPLICATION_ICON = ({'png', 'jpeg', 'webp'}, 'app-icons/{application}/{hash}.{type}')
    APPLICATION_ASSET = ({'png', 'jpeg', 'webp'}, 'app-assets/{application}/{asset}.{type}')

    def verify_file_type(self, file_type: str):
        if file_type == 'jpg':
            file_type = 'jpeg'

        if file_type not in self.value[0]:
            return False
        return True


class PlebAvatar(enum.IntEnum):
    # The Discord standard avatars for people without real profile pictures.
    BLURPLE = 0
    GREY    = 1
    GRAY    = 1
    GREEN   = 2
    ORANGE  = 3
    RED     = 4

    def __str__(self):
        return self.name.lower()


def _get_image_mime_type(image_data: bytes):
    """Determines the header type for an image given its byte representation."""

    if image_data.startswith(b'\xFF\xD8') and image_data.rstrip(b'\0').endswith(b'\xFF\xD9'):
        return 'image/jpeg'
    elif image_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif image_data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif image_data.startswith(b'RIFF') and image_data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise TypeError('Unsupported image type provided.')


def _create_avatar_uri_scheme(image_data: bytes):
    """Creates the Data URI Scheme for an avatar given its byte representation."""

    mime = _get_image_mime_type(image_data)
    b64 = base64.b64encode(image_data).decode('ascii')

    fmt = 'data:{mime};base64,{data}'
    return fmt.format(mime=mime, data=b64)


def _valid_icon_size(size: int):
    """Validates whether the icon is in a range between 16 and 2048."""

    return not size & (size - 1) and size in range(16, 2049)


def format_url(endpoint, fmt, *, image_format='webp', size=512, animated=False):
    """Formats a CDN url for a Discord icon."""

    _, uri = endpoint.value
    if not endpoint.verify_file_type(image_format):
        raise TypeError('Unsupported file ending for image provided.')

    if image_format == 'gif' and not animated:
        raise TypeError('Avatars that aren\'t animated do not support gif format.')

    if size:
        if not _valid_icon_size(size):
            raise ValueError('The size must be in a range between 16 and 2048.')

        uri += '?size={}'.format(size)

    return BASE_URL + uri.format(**fmt, type=image_format)
