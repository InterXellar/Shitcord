# -*- coding: utf-8 -*-

from .role import Role
from .user import _BaseUser


class Member(_BaseUser):

    """Represents a Member model from the Discord API.

    A member basically is a user inside a guild.
    Because of that, they have more attributes than normal users, e.g. their attached roles.

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
    nick: str, optional
        Represents the member's nickname. None if no nickname is set.
    roles: List[:class:`Role`]
        A list of role objects the member has attached.
    joined_at : :class:`datetime.datetime`
        Representing when the member joined the guild..
    deaf : bool
        Whether the user is deafened or not.
    mute : bool
        Whether the user is muted or not.
    """

    __slots__ = ('nick', 'roles', 'joined_at', 'deaf', 'mute')

    def __init__(self, data, http):
        super().__init__(data['user'], http=http)
        self.nick = data.get('nick')
        self.roles = [Role(role, http) for role in data['roles']]
        self.joined_at = data['joined_at']
        self.deaf = data['deaf']
        self.mute = data['mute']

    def __repr__(self):
        return '<shitcord.Member id={0.id} name={0.name}>'.format(self)

    @property
    def mention(self):
        return '<@{0.id}>'.format(self)
