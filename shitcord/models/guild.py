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

    """

    __slots__ = ()

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)
