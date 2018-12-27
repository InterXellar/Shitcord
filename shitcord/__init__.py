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

import logging
import sys
from collections import namedtuple

from .http import *
from .models import *
from .utils import *
from . import sync

__title__ = 'Shitcord'
__author__ = 'Valentin B.'
__version__ = '0.0.2b'
__license__ = 'GNU GPLv3'
__copyright__ = '(c) 2018 Valentin B.'
__url__ = 'https://github.com/itsVale/Shitcord'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=0, micro=2, releaselevel='beta', serial=0)

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())

if sys.version_info < (3, 5, 2):
    raise RuntimeError('Upgrade your Python, you shitter.')
