# -*- coding: utf-8 -*-

from .api import API
from .errors import ShitRequestFailed
from .http import HTTP
from .rate_limit import CooldownBucket, Limiter
from .rest_shit import *
from .routes import Endpoints

__all__ = ['RESTShit', 'rest_shit']
