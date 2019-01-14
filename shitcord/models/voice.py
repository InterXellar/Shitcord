# -*- coding: utf-8 -*-

from .base import Model
from .member import Member


class VoiceState:
    """Represents a Voice State Model from the Discord API

    Used to represent a user's voice connection status.

    Attributes
    ----------
    guild_id : int, optional
        The guild ID this voice state is for.
    channel_id : int
        The channel ID this user is connected to.
    user_id : int
        The user ID this voice state is for
    member : :class:`Member`, optional
        The guild member this voice state is for.
    session_id : str
        The session ID for this voice state.
    deaf : bool
        Whether this user is deafened by the server.
    mute : bool
        Whether this user is muted by the server.
    self_deaf : bool
        Whether this user is locally deafened.
    self_mute : bool
        Whether this user is locally muted
    suppress : bool
        Whether this user is muted by the current user
    """

    __slots__ = ('guild_id', 'channel_id', 'user_id', 'member', 'session_id', 'deaf', 'mute', 'self_deaf', 'self_mute', 'suppress')

    def __init__(self, data, http):
        self.guild_id = data.get('guild_id')
        self.channel_id = data['channel_id']
        self.user_id = data['user_id']
        self.session_id = data['session_id']
        self.deaf = data['deaf']
        self.mute = data['mute']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.suppress = data['suppress']

        self.member = data.get('member')
        if self.member:
            self.member = Member(self.member, http)

    def __repr__(self):
        return '<shitcord.VoiceState id={}>'.format(self.gui)


class VoiceRegion(Model):
    """Represents a Voice Region Model from the Discord API

    Used to represent a Voice Region from the Discord API.

    Attributes
    ----------
    id : str
        The voice region's ID.
    name : str
        Name of the region.
    vip : bool
        True if this is a vip-only server.
    optimal : bool
        True for a single server that is closest to the current user's client.
    deprecated : bool
        Whether this is a deprecated voice region.
    custom : bool
        Whether this is a custom voice region.
    """

    __slots__ = ('id', 'name', 'vip', 'optimal', 'deprecated', 'custom')

    def __init__(self, data, http):
        super().__init__(data, http=http)

        self.id = data['id']
        self.name = data['name']
        self.vip = data['vip']
        self.optimal = data['optimal']
        self.deprecated = data['deprecated']
        self.custom = data['custom']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<shitcord.VoiceRegion id={0.id} name={0.name}>'.format(self)
