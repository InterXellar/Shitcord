# -*- coding: utf-8 -*-

import enum
from datetime import datetime

from . import abc
from .base import Model

__all__ = ['_channel_from_payload', 'TextChannel', 'DMChannel', 'VoiceChannel', 'GroupDMChannel', 'CategoryChannel']


def _channel_from_payload(payload, http):
    channel_type = IntChannelTypes(payload['type']).name
    channel_cls = _ChannelTypes[channel_type].value

    return channel_cls(payload, http)


def _get_as_datetime(payload, key):
    item = payload.get(key)
    if not item:
        return None

    return datetime.utcfromtimestamp(item)


class _BaseChannel(Model):
    """Represents a BaseChannel class all different channel types will implement.

    This is literally just a base class to define some basic behavior of all different
    channel types and to implement some methods all of these channels share.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel type.
    """

    __slots__ = ('snowflake', 'id', '_json', 'type')

    def __init__(self, data, http):
        self._json = data
        super().__init__(data['id'], http=http)

        self.type = data['type']

    def __repr__(self):
        raise NotImplementedError


class PartialChannel(_BaseChannel, abc.Sendable):
    """Represents a PartialChannel model from the Discord API.

    PartialChannels are very incomplete and thin Channel representations
    with only few attributes. They occur very rarely and only in special cases.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int, optional
        The channel's ID.
    type : int
        An integer representing the channel type. Most likely, this will be 0.
    name : str
        The channel's name.
    """

    def __init__(self, data, http):
        # Make sure an ID is given at any time.
        if not data.get('id'):
            data['id'] = 0

        super().__init__(data, http)

        self.name = data['name']

    def __repr__(self):
        return '<shitcord.PartialChannel id={} name={}>'.format(self.id, self.name)


class TextChannel(_BaseChannel, abc.GuildChannel, abc.Sendable):
    """Represents a TextChannel model from the Discord API.

    TextChannel is a very common channel type. As the name says,
    they always belong to a Guild and are just pure text channels.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel's type. Should be 0.
    guild_id : int
        The Guild ID for the corresponding Guild this channel belongs to.
    position: int
        The channel's position.
    permission_overwrites : typing.List[PermissionOverwrite]
        A list containing `PermissionOverwrite` objects for the channel.
    name : str
        The channel's name.
    topic : str, optional
        The channel's topic.
    nsfw : bool
        Indicates whether the channel is NSFW or not.
    last_message_id : int, optional
        The ID of the last message that was sent into this channel.
    rate_limit : int, optional
        Amount of seconds that must be waited before a message can be sent to this channel.
    parent_id : int, optional
        The channel's parent ID if a parent exists.
    last_pinned: datetime.datetime, optional
        A datetime representing when the last message in this channel was pinned.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.topic = data.get('topic', '')
        self.nsfw = data['nsfw']
        self.last_message_id = data.get('last_message_id')
        self.rate_limit = data.get('rate_limit_per_user', 0)
        self.parent_id = data.get('parent_id')
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.TextChannel id={} name={} guild_id={} nsfw={}>'.format(self.id, self.name, self.guild_id, self.nsfw)


class DMChannel(_BaseChannel, abc.PrivateChannel, abc.Sendable):
    """Represents a DMChannel model from the Discord API.

    This channel type represents a private channel between 2 `User`s.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel's type. Should be 1.
    last_message_id : int, optional
        The ID of the last message that was sent into this channel.
    recipients : typing.List[User]
        A list of `User` objects that are permitted to interact with this channel.
    last_pinned : datetime.datetime, optional
        A datetime representing when the last message in this channel was pinned.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.last_message_id = data.get('last_message_id')
        self.recipients = data['recipients']
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.DMChannel id={}>'.format(self.id)


class VoiceChannel(_BaseChannel, abc.Connectable, abc.GuildChannel):
    """Represents a VoiceChannel model from the Discord API.

    VoiceChannels are channels, Users can connect to and transmit audio.
    Audio usually must be encoded with the opus codec.
    Like `TextChannel`, this channel type also always has a Guild it belongs to.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel's type. Should be 2.
    guild_id : int
        The Guild ID for the corresponding Guild this channel belongs to.
    position: int
        The channel's position.
    permission_overwrites : typing.List[PermissionOverwrite]
        A list containing `PermissionOverwrite` objects for the channel.
    name : str
        The channel's name.
    bitrate : int
        The channel's bitrate.
    user_limit : int
        The total amount of `User`s that can be connected to the channel at the same time.
    parent_id : int, optional
        The channel's parent ID if a parent exists.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        self.parent_id = data.get('parent_id')

    def __repr__(self):
        return '<shitcord.VoiceChannel id={} name={} bitrate={} user_limit={}>'.format(self.id, self.name, self.bitrate, self.user_limit)


class GroupDMChannel(_BaseChannel, abc.PrivateChannel, abc.Sendable):
    """Represents a GroupDMChannel model from the Discord API.

    This is actually quite similar to `DMChannel` except that `User`s can
    be invited to these groups and they show up some parallels to `Guild`.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel's type. Should be 3.
    name : str
        The channel's name.
    last_message_id : int, optional
        The ID of the last message that was sent into this channel.
    recipients : typing.List[User]
        A list of `User` objects that are permitted to interact with this channel.
    icon : str, optional
        The icon hash of the group.
    owner_id : int
        The ID of the `User` that owns the group.
    application_id : int, optional
        The Application ID of the group's creator if it was created by a bot.
    last_pinned : datetime.datetime, optional
        A datetime representing when the last message in this channel was pinned.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['name']
        self.last_message_id = data.get('last_message_id')
        self.recipients = data['recipients']
        self.icon = data.get('icon')
        self.owner_id = data['owner_id']
        self.application_id = data.get('application_id')
        self.last_pinned = _get_as_datetime(data, 'last_pin_timestamp')

    def __repr__(self):
        return '<shitcord.GroupDMChannel id={} name={} owner_id={}>'.format(self.id, self.name, self.owner_id)


class CategoryChannel(_BaseChannel, abc.GuildChannel):
    """Represents a CategoryChannel model from the Discord API.

    Categories always belong to a `Guild`.
    Categories are usually parents to `TextChannel` objects but
    actually have a similar behavior to actual channels.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The channel's ID.
    type : int
        An integer representing the channel's type. Should be 0.
    guild_id : int
        The Guild ID for the corresponding Guild this channel belongs to.
    position: int
        The channel's position.
    permission_overwrites : typing.List[PermissionOverwrite]
        A list containing `PermissionOverwrite` objects for the channel.
    name : str
        The channel's name.
    nsfw : bool
        Indicates whether the channel is NSFW or not.
    parent_id : int, optional
        The channel's parent ID if a parent exists.
    """

    def __init__(self, data, http):
        super().__init__(data, http)

        self.guild_id = data['guild_id']
        self.position = data['position']
        self.permission_overwrites = data['permission_overwrites']
        self.name = data['name']
        self.nsfw = data['nsfw']
        self.parent_id = data.get('parent_id')

    def __repr__(self):
        return '<shitcord.CategoryChannel id={} name={} guild_id={} nsfw={}>'.format(self.id, self.name, self.guild_id, self.nsfw)


class IntChannelTypes(enum.IntEnum):
    GUILD_TEXT     = 0
    DM             = 1
    GUILD_VOICE    = 2
    GROUP_DM       = 3
    GUILD_CATEGORY = 4


class _ChannelTypes(enum.Enum):
    GUILD_TEXT     = TextChannel
    DM             = DMChannel
    GUILD_VOICE    = VoiceChannel
    GROUP_DM       = GroupDMChannel
    GUILD_CATEGORY = CategoryChannel
