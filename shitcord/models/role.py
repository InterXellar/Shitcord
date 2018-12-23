# -*- coding: utf-8 -*-

from .base import Model
from .colour import Colour
from .permissions import Permissions


class Role(Model):
    __slots__ = ('_json', 'name', 'color', 'hoist', 'position', 'permissions', 'managed', 'mentionable')

    def __init__(self, data, http):
        self._json = data
        super().__init__(data['id'], http=http)

        self.name = data['name']
        self.color = Colour(data['color'])
        self.hoist = data['hoist']
        self.position = data['position']
        self.permissions = Permissions(data['permissions'])
        self.managed = data['managed']
        self.mentionable = data['mentionable']
