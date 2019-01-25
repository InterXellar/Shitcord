# -*- coding: utf-8 -*-

import datetime
import logging
import time
from collections import OrderedDict
from email.utils import parsedate_to_datetime

import trio

logger = logging.getLogger(__name__)


class CooldownBucket:
    """This class wraps around a bucket to handle rate limits.

    Instances of this class are stored by the rate limiter and constantly updated.
    It provides all necessary helper properties and methods to effectively detect
    and handle rate limits for the corresponding bucket.

    Parameters
    ----------
    bucket : tuple
        The bucket this :class:`shitcord.http.CooldownBucket` should handle.

    Attributes
    ----------
    bucket : tuple
        The bucket this :class:`shitcord.http.CooldownBucket` should handle.
    date : datetime.datetime
        A datetime object representing the time the current headers were received.
    remaining : int
        The amount of requests that can be still made to the bucket before exhausting
        a rate limit.
    reset : float
        The interval in seconds after which the rate limits for this bucket will reset.
    cooled_down : :class:`trio.Event`
        An event used for indicating the current cooldown state of the bucket.
    """

    __slots__ = ('bucket', 'date', 'remaining', 'reset', 'cooled_down')

    def __init__(self, bucket, response):
        self.bucket = bucket

        # these will be set later
        self.date = None
        self.remaining = 0
        self.reset = None

        self.cooled_down = trio.Event()
        self.cooled_down.set()

        self.update(response)

    def __repr__(self):
        if isinstance(self.bucket, str):
            bucket = (self.bucket,)
        else:
            bucket = self.bucket

        return '<shitcord.http.APIResponse {}>'.format(' '.join(bucket))

    @property
    def get_current_time(self):
        """Returns a datetime object denoting the current time in UTC.
        This is especially necessary for determining the actual rate limit reset time.
        """

        return datetime.datetime.now(datetime.timezone.utc)

    @property
    def cooling_down(self):
        """Whether this bucket is currently being cooled down or not."""

        return not self.cooled_down.is_set()

    @property
    def will_rate_limit(self):
        """Whether the next request will cause a rate limit or not."""

        return self.get_current_time <= self.reset and self.remaining == 0

    def update(self, response):
        """Updates the current APIResponse object with response headers
        and body from a new request to the corresponding bucket.
        """

        headers = response.headers

        # Rate limit headers is basically all or nothing.
        # If one of the rate limit headers is missing, any
        # other rate limit headers also won't be included.
        # It basically doesn't really matter what header to check here.
        if 'X-RateLimit-Remaining' not in headers:
            return

        self.date = parsedate_to_datetime(headers.get('Date'))
        self.remaining = int(headers.get('X-RateLimit-Remaining'))
        self.reset = datetime.datetime.fromtimestamp(int(headers.get('X-RateLimit-Reset')), datetime.timezone.utc)

    async def wait(self):
        """|coro|

        Waits until the bucket has been cooled down.

        Returns
        -------
        float
            The duration we waited for.
        """

        start = time.time()
        await self.cooled_down.wait()
        return time.time() - start

    async def cooldown(self):
        """|coro|

        Cools down a bucket.
        """

        if self.reset < self.get_current_time:
            raise ValueError('Cannot cooldown for a negative time period.')

        self.cooled_down.clear()
        delay = (self.reset - self.date).total_seconds() + .5
        logger.debug('Cooling down bucket %s for %s seconds.', self, delay)
        await trio.sleep(delay)
        self.cooled_down.set()

        return delay


class Limiter:
    """Represents a Limiter for handling per-bucket rate limits.

    By storing buckets with corresponding :class:`shitcord.http.CooldownBucket` objects,
    the limiter keeps track of all received API responses and updates the CooldownBuckets
    with the corresponding headers. Once a CooldownBucket indicates a rate limit has been
    exhausted, the limiter blocks until the limit resets before making another request to
    the same bucket. This also handles global rate limits and returns the total cooldown duration.

    Attributes
    ----------
    buckets : :class:`collections.OrderedDict`
        An OrderedDict to keep track of the buckets.
    """

    def __init__(self):
        self.buckets = OrderedDict()

    async def chill(self, bucket):
        """|coro|

        Checks if it's safe to make a request to the given bucket.

        For this case, this method will return immediately.
        Otherwise it will block until the bucket has been cooled down.

        This also handles global rate limits.

        Parameters
        ----------
        bucket : tuple
            The bucket to check.
        """

        return await self._get_limit_duration('global_rate_limit') + await self._get_limit_duration(bucket)

    async def _get_limit_duration(self, bucket):
        if bucket in self.buckets:
            if self.buckets[bucket].cooling_down:
                return await self.buckets[bucket].wait()

            if self.buckets[bucket].will_rate_limit:
                return await self.buckets[bucket].cooldown()

        return 0

    def update_bucket(self, bucket, response):
        """Updates a :class:`shitcord.http.CooldownBucket` for a given bucket.

        Parameters
        ----------
        bucket : tuple
            The bucket to initialize :class:`shitcord.http.CooldownBucket` with.
        response : :class:`asks.Response`
            A response object to retrieve rate limit headers from.
        """

        if 'X-RateLimit-Global' in response.headers:
            bucket = 'global_rate_limit'

        if bucket in self.buckets:
            self.buckets[bucket].update(response)
        else:
            self.buckets[bucket] = CooldownBucket(bucket, response)
