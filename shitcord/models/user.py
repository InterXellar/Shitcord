# -*- coding: utf-8 -*-

import enum

from . import abc
from .base import Model
from .errors import MissingProfile
from ..utils import cdn

__all__ = ['Connection', 'User']


class RelationshipType(enum.IntEnum):
    FRIEND           = 1  # noqa
    BLOCKED          = 2  # noqa
    INCOMING_REQUEST = 3  # noqa
    OUTGOING_REQUEST = 4  # noqa


class HypeSquadHouse(enum.IntEnum):
    BRAVERY    = 1  # noqa
    BRILLIANCE = 2  # noqa
    BALANCE    = 3  # noqa


class Flags(enum.IntEnum):
    DISCORD_EMPLOYEE     = 1  # noqa
    DISCORD_PARTNER      = 2  # noqa
    DISCORD_HYPESQUAD    = 4  # noqa
    DISCORD_BUG_HUNTER   = 8  # noqa
    HYPESQUAD_BRAVERY    = 64  # noqa
    HYPESQUAD_BRILLIANCE = 128  # noqa
    HYPESQUAD_BALANCE    = 256  # noqa
    EARLY_SUPPORTER      = 512  # noqa


class _BaseUser(Model, abc.DiscordUser):
    """Represents a base class for Users on Discord.

    It implements some core functionality Users as well as Members have.

    Attributes
    ----------
    snowflake : :class:`Snowflake`
        A :class:`Snowflake` object that represents the user's ID.
    id : int
        The user's ID.
    name : str
        The user's name.
    avatar_hash : str
        The hash of the user's avatar.
    """

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.name = data.get('username')
        self.discriminator = int(data['discriminator']) if data.get('discriminator') else None
        self.avatar_hash = data.get('avatar')

    def __str__(self):
        return '{0.name}#{0.discriminator}'.format(self)

    @property
    def mention(self):
        raise NotImplementedError

    @property
    def default_avatar(self):
        """Returns an enum member that represents the user's default avatar."""

        return cdn.PlebAvatar(self.discriminator % 5)

    @property
    def avatar(self):
        """Returns a CDN url for the user's avatar."""

        return self.avatar_url()

    @property
    def animated_avatar(self):
        """Returns a boolean indicating whether the user's avatar is animated or not."""

        avatar_hash = self.avatar_hash
        return avatar_hash and avatar_hash.startswith('a_')

    @property
    def default_avatar_url(self):
        """Returns a CDN url for the user's default avatar."""

        return cdn.format_url(cdn.Endpoints.DEFAULT_USER_AVATAR, dict(discriminator=self.default_avatar.value), image_format='png')

    def avatar_url(self, image_format=None, size=1024):
        """Returns a CDN url for the user's avatar.

        Parameters
        ----------
        image_format : str
            The file format for the user's avatar. Defaults to 'webp'.
        size : int, optional
            The size of the image from the CDN url. Defaults to '1024'. Must be in a range between 16 and 2048.
        """

        if not self.avatar_hash:
            return self.get_default_avatar()

        if image_format is None:
            image_format = 'webp'
            if self.animated_avatar:
                image_format = 'gif'

        animated = image_format == 'gif'

        return cdn.format_url(cdn.Endpoints.USER_AVATAR,
                              dict(user=self.id, hash=self.avatar_hash), image_format=image_format, size=size, animated=animated)


class User(_BaseUser):
    """Represents a User on Discord.

    Users on Discord don't belong to guilds.
    They are only in DM conversations.

    Attributes
    ----------
    snowflake : :class:`Snowflake`
        A :class:`Snowflake` object that represents the user's ID.
    id : int
        The user's ID.
    name : str
        The user's name.
    avatar_hash : str
        The hash of the user's avatar.
    bot : bool, optional
        A boolean indicating whether the user is a bot or not.
    mfa_enabled : bool, optional
        A boolean indicating whether the user has mfa enabled or not.
    verified : bool, optional
        A boolean indicating whether the user has verified his email address or not.
    email : str, optional
        The user's email address.
    flags : int, optional
        The user's account flags. None when permissions for accessing flags aren't granted.
    permium_type : int, optional
        The user's premium type as an integer. None when permissions for accessing the premium type aren't granted.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.bot = data.get('bot', False)
        self.mfa_enabled = data.get('mfa_enabled', False)
        self.language = data.get('locale')
        self.verified = data.get('verified')
        self.email = data.get('email', '')
        self.flags = data.get('flags')
        self.premium_type = data.get('premium_type')

    @property
    def mention(self):
        """Returns a string that mentions the user."""

        return '<@{}>'.format(self.id)

    def _has_flag(self, flag):
        if self.flags is None:
            raise MissingProfile('User object has no flags attached.')

        value = flag.value
        return (self.flags & value) == value

    @property
    def nitro_classic(self):
        """Indicates whether the user has Nitro Classic or not."""

        if self.premium_type is None:
            raise MissingProfile('No information about Nitro status are accessible.')

        return self.premium_type == 1

    @property
    def nitro(self):
        """Indicates whether the user has Nitro or not."""

        if self.premium_type is None:
            raise MissingProfile('No information about Nitro status are accessible.')

        return self.premium_type == 2

    @property
    def employee(self):
        """Indicates whether the user is a Discord Employee or not."""

        return self._has_flag(Flags.DISCORD_EMPLOYEE)

    @property
    def partner(self):
        """Indicates whether the user is a Discord Partner or not."""

        return self._has_flag(Flags.DISCORD_PARTNER)

    @property
    def hypesquad(self):
        """Indicates whether the user is inside HypeSquad Events or not."""

        return self._has_flag(Flags.DISCORD_HYPESQUAD)

    @property
    def bug_hunter(self):
        """Indicates whether the user is a Bug Hunter or not."""

        return self._has_flag(Flags.DISCORD_BUG_HUNTER)

    @property
    def hypesquad_house(self):
        """Returns a list of HypeSquad houses this user is in."""

        houses = [
            house for house, flag in zip(HypeSquadHouse, (Flags.HYPESQUAD_BRAVERY, Flags.HYPESQUAD_BRILLIANCE, Flags.HYPESQUAD_BALANCE))
            if self._has_flag(flag)
        ]

        if len(houses) == 1:
            return houses[0]
        return houses


class Connection:
    """Represents a connection object every user has attached.

    Attributes
    ----------
    id : str
        The ID of the connection account.
    name : str
        The username of the connection account.
    type : str
        The service of the connection.
    revoked : bool
        Whether the connection is revoked or not.
    integrations : list
        A list of :class:`Integration` objects
    """

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.revoked = data['revoked']
        self.integrations = data['integrations']
