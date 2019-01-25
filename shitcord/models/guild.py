# -*- coding: utf-8 -*-

from .emoji import Emoji
from .base import Model
from .member import Member
from .gateway import Presence
from .role import Role
from .voice import VoiceState
from .channel import _channel_from_payload
from ..utils import parse_time


class Guild(Model):
    """Represents a Guild Model from the Discord API

    Guilds in Discord represent an isolated collection of users and channels,
    and are often referred to as "servers" in the UI.

    Attributes
    ----------
    snowflake: :class:`Snowflake`
        A :class:`Snowflake` object that represents the guild's ID.
    id : int
        The ID of the guild.
    name : str
        The name of the guild.
    icon : str
        Icon hash.
    splash : str
        Splash hash.
    owner : bool, optional
        Whether or not the user is the owner of the guild.
    owner_id : int
        The ID of the guild owner.
    permissions : int, optional
        Total permissions for the user in the guild (does not include channel overrides).
    region : str
        Voice region ID for the guild.
    afk_channel_id : int
        The ID of the afk channel.
    afk_timeout : int
        The afk timeout in seconds.
    embed_enabled : bool, optional
        If this guild is embeddable (e.g. widget).
    embed_channel_id : int, optional
        If not null, the channel ID that the widget will generate an invite to.
    verification_level : int
        Verification level that is required for the guild.
    default_message_notifications : int
        Default message notification level.
    explicit_content_filter : int
        Explicit content filter level
    roles : List[:class:`Role`]
        Roles in the guild.
    emojis : List[:class:`Emoji`]
        Emojis in the guild.
    features : List[str]
        The enabled features of the guild.
    mfa_level : int
        The required mfa level for the guild.
    application_id : int
        Application ID of the guild creator if it is bot-created.
    widget_enabled : bool, optional
        Whether or not the guild widget is enabled.
    widget_channel_id : int, optional
        The channel ID for the guild widget.
    system_channel_id : int
        The channel ID of the channel where system messages are sent to.
    joined_at : :class:`datetime.datetime`, optional
        When this guild was joined at.
    large : bool, optional
        Whether this guild is considered large or not.
    unavailable : bool, optional
        Whether this guild is unavailable or not.
    member_count : int, optional
        Total number of members in that guild.
    voice_states : List[:class:`VoiceState`], optional
        List of voice states objects of the guild.
    members : List[:class:`Member`], optional
        Members of the guild.
    channels : List[:class:`Channel`], optional
        The channels of the guild.
    presences : List[:class:`Presence`], optional
        Presences of the users in the guild.
    """

    __slots__ = ('name', 'icon', 'splash', 'owner', 'owner_id', 'permissions', 'region', 'afk_channel_id', 'afk_timeout', 'embed_enabled',
                 'embed_channel_id', 'verification_level', 'default_message_notifications', 'explicit_content_filter', 'role', 'emojis', 'features',
                 'mfa_level', 'application_id', 'widget_enabled', 'widget_channel_id', 'system_channel_id', 'joined_at', 'large',
                 'unavailable', 'member_count', 'voice_states', 'members', 'channels', 'presences')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.name = data['name']
        self.icon = data['icon']
        self.splash = data['splash']
        self.owner = data.get('owner')
        self.owner_id = data['owner_id']
        self.permissions = data.get('permissions')
        self.region = data['region']
        self.afk_channel_id = data['afk_channel_id']
        self.afk_timeout = data['afk_timeout']
        self.embed_enabled = data.get('embed_enabled')
        self.embed_channel_id = data.get('embed_channel_id')
        self.verification_level = data['verification_level']
        self.default_message_notifications = data['default_message_notifications']
        self.explicit_content_filter = data['explicit_content_filter']
        self.roles = [Role(role, http) for role in data['roles']]
        self.emojis = [Emoji(self.id, emoji, http) for emoji in data['emojis']]
        self.features = data['features']
        self.mfa_level = data['mfa_level']
        self.application_id = data['application_id']
        self.widget_enabled = data.get('widget_enabled')
        self.widget_channel_id = data.get('widget_channel_id')
        self.system_channel_id = data['system_channel_id']
        self.joined_at = parse_time(data.get('joined_at'))
        self.large = data.get('large')
        self.unavailable = data.get('unavailable')
        self.member_count = data.get('member_count')
        self.members = [Member(member, http) for member in data.get('members', [])]
        self.channels = [_channel_from_payload(channel, http) for channel in data.get('channels', [])]
        self.voice_states = [VoiceState(voice_state, http) for voice_state in data.get('voice_states', [])]
        self.presences = [Presence(presence, http) for presence in data.get('presences', [])]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<shitcord.Guild id={0.id} name={0.name}>'.format(self)


class PartialGuild(Model):
    """Represents a Partial Guild Model from the Discord API

    Represents an Offline Guild,
    or a Guild whose information has not been provided through Guild Create events during the Gateway connect.

    Attributes
    ----------
    snowflake: :class:`Snowflake`
        A :class:`Snowflake` object that represents the guild's ID.
    id : int
        The ID of the guild.
    unavailable : bool
        Whether this guild is available or not.
    """

    __slots__ = ('unavailable',)

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.unavailable = data['unavailable']

    def __repr__(self):
        return '<shitcord.PartialGuild id={}>'.format(self.id)
