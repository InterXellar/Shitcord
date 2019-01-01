# -*- coding: utf-8 -*-

import logging
from contextlib import contextmanager

import contextvars

from .http import HTTP

logger = logging.getLogger(__name__)


def optional(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


class API:
    def __init__(self, token):
        self.http = HTTP(token)
        self._storage = contextvars.ContextVar('_storage', default=[])

    @property
    def token(self):
        return self.http._token

    async def make_request(self, route, fmt=None, **kwargs):
        response = await self.http.make_request(route, fmt, **kwargs)
        self._capture_response(response)

        return response

    def _capture_response(self, response):
        self._storage.get().append(response)  # Quite ugly, but does its job.
        logger.debug('Added response "%s" to the cache.', response)

    @contextmanager
    def raw_responses(self):
        """A contextmanager that yields all the captured raw responses from the requests we made.

        PLEASE DO ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING!
        """

        responses = self._storage.get()

        try:
            yield responses
        finally:
            self._storage.set([])

    # Start actual wrapping
