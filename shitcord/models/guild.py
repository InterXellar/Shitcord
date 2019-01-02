# -*- coding: utf-8 -*-

from .base import Model


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
    roles : list[:class:`Role`]
        Roles in the guild.
    emojis : list[:class:`Emoji`]
        Emojis in the guild.
    features : list[str]
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
    voice_states : list[], optional
        List of voice states objects of the guild.
    members : list[:class:`Member`], optional
        Members of the guild.
    channels : list[:class:`Channel`], optional
        The channels of the guild.
    presences : list[], optional
        Presences of the users in the guild.
    """

    __slots__ = ('name', 'icon', 'splash', 'owner', 'owner_id', 'permissions', 'region', 'afk_channel_id', 'afk_timeout', 'embed_enabled',
                 'embed_channel_id', 'verification_level', 'default_message_notifications', 'explicit_content_filter', 'role', 'emojis', 'features',
                 'mfa_level', 'application_id', 'widget_enabled', 'widget_channel_id', 'system_channel_id', 'joined_at', 'large'
                 'unavailable', 'member_count', 'voice_states', 'members', 'channels', 'presences')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.name = data['name']
        self.icon = data['icon']
        self.splash = data['splash']
        self.owner = data.get('owner')
        self.owner_id = data['owner.id']
        self.permissions = data.get('permissions')
