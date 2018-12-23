# -*- coding: utf-8 -*-

from collections import namedtuple

from ..utils import cdn
from .base import Model
from .user import User


class _BaseEmoji(Model):
    __slots__ = ('name', )

    def __init__(self, data, http):
        super().__init__(data.get('id', 0), http=http)

        self.name = data['name']

    def __repr__(self):
        raise NotImplementedError

    @property
    def url(self):
        format = 'gif' if self.animated else 'png'
        return cdn.format_url(cdn.Endpoints.CUSTOM_EMOJI, dict(emoji=self.id), image_format=format)


class PartialEmoji(_BaseEmoji, namedtuple('PartialEmoji', 'id name animated')):
    __slots__ = ()

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
