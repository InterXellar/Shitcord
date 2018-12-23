# -*- coding: utf-8 -*-

import datetime
import logging
from email.utils import parsedate_to_datetime

import trio

logger = logging.getLogger(__name__)


class APIResponse:
    def __init__(self, bucket, response, parsed):
        self._bucket = bucket
        self._response = response
        self._parsed = parsed
        self._headers = self._response.headers

        # Get all relevant headers for rate limit handling and parse them into a useful format.
        self.date = self._headers.get('Date')
        self.remaining = int(self._headers.get('X-RateLimit-Remaining', 0))
        self.reset = self._parse_reset(int(self._headers.get('X-RateLimit-Reset', 0)))
        self.is_global = self._headers.get('X-RateLimit-Global', False)

    def __repr__(self):
        return '<APIResponse for bucket {} with headers {}>'.format(self._bucket, self._headers)

    def _parse_reset(self, reset):
        now = parsedate_to_datetime(self.date)
        res = datetime.datetime.fromtimestamp(reset, datetime.timezone.utc)
        return (res - now).total_seconds() + .2

    @property
    def is_rate_limited(self):
        return self._response.status_code == 429

    @property
    def will_rate_limit(self):
        return self._response.status_code != 429 and self.remaining == 0

    @property
    def global_limit(self):
        return self.is_rate_limited and self.is_global

    @property
    def retry_after(self):
        return self._parsed['retry_after'] / 1000.0

    @staticmethod
    async def cooldown(duration):
        """Returns a cooldown for the current API response."""

        logger.debug('Sleeping for %s seconds due to an exhausted rate limit...', duration)
        try:
            return await trio.sleep(duration)
        except ValueError:
            # trio.sleep doesn't like negative values.
            # For the case of a stupid rate limit reset header that computes to a negative rate limit duration
            # we have to catch the ValueError.
            pass


class Limiter:
    def __init__(self):
        self.no_global_limit = trio.Event()
        self.no_global_limit.set()

    async def __call__(self, bucket, response, parsed):
        resp = APIResponse(bucket, response, parsed)
        await self._cooldown_task(resp)

    async def _cooldown_task(self, response):
        duration, global_limit = self.get_cooldown(response)

        # Ugly shit, but unfortunately no way to clean this up furthermore.
        async with trio.open_nursery() as nursery:
            nursery.start_soon(response.cooldown, duration)

            if global_limit:
                with trio.move_on_after(duration):
                    self.no_global_limit.clear()
                self.no_global_limit.set()

    @staticmethod
    def get_cooldown(resp):
        if resp.will_rate_limit:
            # In this case, the next request is going to cause a rate limit.
            duration = resp.reset
            logger.debug('Next request is going to cause a rate limit. We wait for a Rate Limit Reset in %s seconds.', duration)

        elif resp.is_rate_limited:
            # For this case, we are already rate-limited.
            duration = resp.retry_after
            logger.debug('You are being rate limited. We will retry it in %s seconds.', duration)

            if resp.global_limit:
                # Global rate limit. Not good.
                logger.debug('Global rate limit has been exhausted.')

        else:
            # We are neither rate-limited nor exhausted a rate limit bucket.
            duration = 0

        return duration, resp.global_limit
