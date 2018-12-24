# -*- coding: utf-8 -*-

"""
shitcord.models
~~~~~~~~~~~~~~~

Represents the implementations of the models from the Discord API.
"""

from .base import Model
from .channel import *
from .colour import Color, Colour
from .emoji import Emoji, PartialEmoji
from .errors import *
from .permissions import Permissions, PermissionTypes
from .role import Role
from .snowflake import DISCORD_EPOCH, Snowflake
from .user import User

__all__ = ['Color', 'Colour', 'DISCORD_EPOCH', 'Emoji', 'PartialEmoji', 'Permissions',
           'PermissionTypes', 'TextChannel', 'DMChannel', 'Role', 'Snowflake', 'VoiceChannel',
           'GroupDMChannel', 'CategoryChannel', 'User']
