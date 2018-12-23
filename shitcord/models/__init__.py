# -*- coding: utf-8 -*-

"""
shitcord.models
~~~~~~~~~~~~~~~

Represents the implementations of the models from the Discord API.
"""

from .base import Model
from .channel import *
from .colour import Color, Colour
from .errors import ModelError, NoFlags
from .snowflake import DISCORD_EPOCH, Snowflake
from .user import User

__all__ = ['Color', 'Colour', 'DISCORD_EPOCH', 'TextChannel','DMChannel', 'Snowflake',
           'VoiceChannel', 'GroupDMChannel', 'CategoryChannel', 'User']
