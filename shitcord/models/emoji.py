# -*- coding: utf-8 -*-

from ..utils import cdn
from .base import Model
from .user import User


class _BaseEmoji(Model):
    """Represents a base class for Emoji implementations.

    Attributes
    ----------
    snowflake : :class:`Snowflake`
        A :class:`Snowflake` object representing the emoji's ID.
    name : str
        Either the custom emoji's name or a unicode representation of the emoji.
    """

    __slots__ = ('name', )

    def __init__(self, data, http):
        super().__init__(data.get('id', 0), http=http)

        self.name = data['name']

    def __repr__(self):
        raise NotImplementedError

    @property
    def url(self):
        image_format = 'gif' if self.animated else 'png'
        return cdn.format_url(cdn.Endpoints.CUSTOM_EMOJI, dict(emoji=self.id), image_format=image_format)


class PartialEmoji(_BaseEmoji):
    """Represents a PartialEmoji model from the Discord API.

    This is a special form of Emoji where only a few parameters are given.
    In this case, the name can either be a unicode emoji or a custom emoji's name.
    In such a case, a bool may be included that tells whether the emoji is animated.

    Attributes
    ----------
    snowflake : :class:`Snowflake`, optional
        A :class:`Snowflake` object that represents the emoji's ID.
    name : str
        Either the custom emoji's name or a unicode representation of the emoji.
    animated : bool, optional
        A boolean indicating whether the emoji is animated or not.
    """

    __slots__ = ('animated', )

    def __init__(self, data, http):
        super().__init__(data, http)

        self.animated = data.get('animated', False)

    def __str__(self):
        if not self.id:
            return self.name

        if self.animated:
            return '<a:{0.name}:{0.id}>'.format(self)
        return '<:{0.name}:{0.id}>'.format(self)

    def __repr__(self):
        return '<shitcord.PartialEmoji id={0.id} name={0.name}>'.format(self)

    @property
    def is_custom_emoji(self):
        return self.id is not None

    def to_reaction(self):
        if not self.is_custom_emoji:
            return self.name
        return ':{0.name}:{0.id}'.format(self)


class Emoji(_BaseEmoji):
    """Represents an Emoji model from the Discord API.

    Attributes
    ----------
    snowflake : :class:`Snowflake`, optional
        A :class:`Snowflake` object that represents the emoji's ID.
    name : str
        Either the custom emoji's name or a unicode representation of the emoji.
    guild_id : int
        The ID of the Guild this emoji belongs to.
    roles : list
        A list of role IDs which are whitelisted for this emoji.
    user : :class:`User`
        A :class`User` object representing the creator of the emoji.
    require_colons : bool, optional
        A boolean indicating whether this emoji requires colons or not.
    managed : bool, optional
        A boolean indicating whether this emoji is managed or not.
    animated : bool, optional
        A boolean indicating whether the emoji is animated or not.
    """

    __slots__ = ('guild_id', 'roles', 'user', 'required_colons', 'managed', 'animated')

    def __init__(self, guild_id, data, http):
        super().__init__(data, http)

        self.guild_id = guild_id
        self.roles = list(map(int, data.get('roles', [])))
        self.user = User(data['user'], self._http)
        self.require_colons = data.get('require_colons', False)
        self.managed = data.get('managed', False)
        self.animated = data.get('animated', False)

    def __str__(self):
        if self.animated:
            return '<a:{0.name}:{0.id}>'.format(self)
        return '<:{0.name}:{0.id}>'.format(self)

    def __repr__(self):
        return '<shitcord.Emoji id={0.id} name={0.name!r}>'.format(self)
