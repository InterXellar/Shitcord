# -*- coding: utf-8 -*-

from .base import Model
from .user import User


class Webhook(Model):
    """Represents a Webhook Model from the Discord API

    Webhooks are a low-effort way to post messages to channels in Discord.
    They do not require a bot user or authentication to use.

    Attributes
    ----------
    snowflake: :class:`Snowflake`
        A :class:`Snowflake` object that represents the webhooks's ID.
    id : int
        The webhook's ID.
    guild_id : int
        The guild ID this webhook is for.
    channel_id : int
        The channel ID this webhook is for.
    user : :class:`User`
        The user this webhook was created by (not returned when getting a webhook with its token).
    name : str
        The default name of the webhook.
    avatar : str
        The default avatar of the webhook.
    token : str
        The secure token of the webhook.
    """

    __slots__ = ('guild_id', 'channel_id', 'user', 'name', 'avatar', 'token')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.guild_id = data['guild_id']
        self.channel_id = data['channel_id']
        self.user = User(data['user'], self._http)
        self.name = data['name']
        self.avatar = data['avatar']
        self.token = data['token']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<shitcord.Webhook id={0.id} name={0.name}>'.format(self)
