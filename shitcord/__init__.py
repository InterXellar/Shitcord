# -*- coding: utf-8 -*-

"""
Shitcord
~~~~~~~~

A shitty, fucked up wrapper of the Discord API.
Don't expect too much because this was intended to be a joke at the beginning. :^)
Though I think this lib could actually be pretty cool...

:copyright: (c) 2018 Valentin B.
:license: GNU GPLv3, see LICENSE for more information
"""

__title__ = 'Shitcord'
__author__ = 'Valentin B.'
__version__ = '0.0.3b'
__license__ = 'GNU GPLv3'
__copyright__ = '(c) 2018 Valentin B.'
__url__ = 'https://github.com/itsVale/Shitcord'

import logging
from collections import namedtuple

from .client import *
from .http import *
from .gateway import *
from .models import *
from .utils import *
import shitcord.sync  # We don't want our classes from shitcord.models overridden

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=0, micro=3, releaselevel='beta', serial=0)

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())
