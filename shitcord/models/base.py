# -*- coding: utf-8 -*-

import abc

from .snowflake import Snowflake


class Model(abc.ABC):
    """Represents an Abstract Base Class for most models in this library.

    Most of this library's implementations of the Discord API models implement
    this ABC which mainly provides some core functionality.

    Attributes
    ----------
    snowflake: Snowflake
        A :class:`Snowflake` object that represents the model's ID.
    id : int
        The ID of the model. This should always be retrieved from the Discord API.
        For the case a model doesn't have an ID, defaults to 0.
    """

    def __init__(self, model_id, *, http):
        self._json = None  # The raw dictionary from the Discord API.
        self.snowflake = Snowflake(int(model_id))
        self.id = self.snowflake.snowflake
        self._http = http

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not isinstance(other, self.__class__) or self.id != other.id

    def __repr__(self):
        return '<shitcord.Model id={}>'.format(self.id)

    def __hash__(self):
        return self.id >> 22

    @property
    def created_at(self):
        return self.snowflake.timestamp

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
