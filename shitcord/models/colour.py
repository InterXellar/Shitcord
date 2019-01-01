# -*- coding: utf-8 -*-

import colorsys
from random import random


class Colour:
    """Represents a Colour class that basically wraps around a color like an RGB tuple.

    This class is used for displaying the colors of models from the Discord API, e.g. Role or Embed.
    There is an alias for this under :class:`Color`.

    Parameters
    ----------
    value : int
        The color code integer.
    """

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
    def r(self):
        """Returns the red component of a colour."""

        return self.__get_byte(2)

    @property
    def g(self):
        """Returns the green component of a colour."""

        return self.__get_byte(1)

    @property
    def b(self):
        """Returns the blue component of a colour."""

        return self.__get_byte(0)

    def to_rgb(self):
        """Returns a tuple containing the rgb values for the colour."""

        return self.r, self.g, self.b

    @classmethod
    def from_rgb(cls, r, g, b):
        """Returns a new instance of :class:`Colour` from given rgb values."""

        colour = (r << 16) + (g << 8) + b

        return cls(colour)

    @classmethod
    def from_hsv(cls, h, s, v):
        """Returns a new instance of :class:`Colour` from given hsv values."""

        rgb_colour = colorsys.hsv_to_rgb(h, s, v)

        return cls.from_rgb(*(int(component * 255) for component in rgb_colour))

    @classmethod
    def default(cls):
        """A factory method that returns a new instance of :class:`Colour` without any colour value."""

        return cls(0)

    @classmethod
    def red(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xff0000' as the colour value."""

        return cls(0xff0000)

    @classmethod
    def green(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x6eff00' as the colour value."""

        return cls(0x6eff00)

    @classmethod
    def blue(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x0000ff' as the colour value."""

        return cls(0x0000ff)

    @classmethod
    def yellow(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xffff00' as the colour value."""

        return cls(0xffff00)

    @classmethod
    def orange(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xffa500' as the colour value."""

        return cls(0xffa500)

    @classmethod
    def purple(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xd600ff' as the colour value."""

        return cls(0xd600ff)

    @classmethod
    def gold(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xffd700' as the colour value."""

        return cls(0xffd700)

    @classmethod
    def silver(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xc0c0c0' as the colour value."""

        return cls(0xc0c0c0)

    @classmethod
    def clear(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x36393e' as the colour value."""

        return cls(0x36393e)

    @classmethod
    def pink(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xffc0cb' as the colour value."""

        return cls(0xffc0cb)

    @classmethod
    def blurple(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x7289da' as the colour value."""

        return cls(0x7289da)

    @classmethod
    def greyple(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x99aab5' as the colour value."""

        return cls(0x99aab5)

    @classmethod
    def brown(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0xa0522d' as the colour value."""

        return cls(0xa0522d)

    shit = brown

    @classmethod
    def grey(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x808080' as the colour value."""

        return cls(0x808080)

    @classmethod
    def light_blue(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x00fff9' as the colour value."""

        return cls(0x00fff9)

    @classmethod
    def light_green(cls):
        """A factory method that returns a new instance of :class:`Colour` with '0x3cff00' as the colour value."""

        return cls(0x3cff00)

    @classmethod
    def random(cls):
        """A factory method that returns a new instance of :class:`Colour` with a random colour value."""

        rgb_colour = colorsys.hsv_to_rgb(random(), 1, 1)
        values = [int(component * 255) for component in rgb_colour]

        return cls.from_rgb(*values)


# Alias
Color = Colour
