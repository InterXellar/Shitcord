# -*- coding: utf-8 -*-

import colorsys
from random import random


class Colour:
    __slots__ = ('value', )

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Colour) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '#{:0>6x}'.format(self.value)

    def __repr__(self):
        return '<shitcord.Colour value={}>'.format(self.value)

    def __hash__(self):
        return hash(self.value)

    def __get_byte(self, value):
        return (self.value >> (8 * value)) & 0xff

    @property
    def red(self):
        return self.__get_byte(2)

    @property
    def green(self):
        return self.__get_byte(1)

    @property
    def blue(self):
        return self.__get_byte(0)

    @classmethod
    def from_rgb(cls, r, g, b):
        colour = (r << 16) + (g << 8) + b

        return cls(colour)

    @classmethod
    def from_hsv(cls, h, s, v):
        rgb_colour = colorsys.hsv_to_rgb(h, s, v)

        return cls.from_rgb(*(int(component * 255) for component in rgb_colour))

    # TODO: Implement more classmethods for creating Colour objects with default color values.

    @classmethod
    def default(cls):
        return cls(0)

    @classmethod
    def random(cls):
        rgb_colour = colorsys.hsv_to_rgb(random(), 1, 1)
        values = [int(component * 255) for component in rgb_colour]

        return cls.from_rgb(*values)


# Alias
Color = Colour
