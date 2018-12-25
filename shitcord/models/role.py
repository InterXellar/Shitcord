# -*- coding: utf-8 -*-

from .base import Model
from .colour import Colour
from .permissions import Permissions


class Role(Model):
    """Represents a Role model from the Discord API.

    A Role belongs to a Guild and is basically a set of permissions
    attached to a group of users. They are unique per Guild.

    Attributes
    ----------
    snowflake: :class:`Snowflake`
        A :class:`Snowflake` object that represents the role's ID.
    id : int
        The role's ID.
    name : str
        The role's name.
    hoist: bool
        A boolean indicating whether the role is hoisted or not.
    position : int
        The role's position in the hierarchy.
    permissions : :class:`Permissions`
        A :class:`Permissions` object representing the permissions attached to the role.
    managed : bool
        Whether the role is managed or not.
    mentionable : bool
        Whether the role is mentionable by everyone or not.
    """

    __slots__ = ('name', 'color', 'hoist', 'position', 'permissions', 'managed', 'mentionable')

    def __init__(self, data, http):
        super().__init__(data['id'], http=http)

        self.name = data['name']
        self.color = Colour(data['color'])
        self.hoist = data['hoist']
        self.position = data['position']
        self.permissions = Permissions(data['permissions'])
        self.managed = data['managed']
        self.mentionable = data['mentionable']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<shitcord.Role id={0.id} name={0.name}>'.format(self)

    @property
    def mention(self):
        """Returns a string that mentions the role."""

        return '<@&{}>'.format(self.id)
