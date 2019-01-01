# -*- coding: utf-8 -*-

from .user import _BaseUser
from .role import Role


class Member(_BaseUser):

    """Represents a Member model from the Discord API

    A Member is a User based Guild member.

    Attributes
    ----------
    user: :class:`User`
        A :class:`User` that represent the Member User.
    nick: str
        Represents the member's nick, if no nick exists None.
    roles: :class:`Roles`
        An Array of member's roles.
    joined_at: ISO8601 timestamp
        Represents the joining date and time.
    deaf: bool
        Whether the user is deafened or not.
    mute: bool
        Whether the user is muted or not.
    """

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
