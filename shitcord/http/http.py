# -*- coding: utf-8 -*-

import shitcord

import logging
import sys
from random import randint
from urllib.parse import quote

import trio
import asks

from .errors import ShitRequestFailed
from .rate_limit import Limiter

logger = logging.getLogger(__name__)
asks.init(trio)


class HTTP:
    """Represents an HTTP client that wraps around the asks library and performs requests to the Discord API."""

    BASE_URL = 'https://discordapp.com/api/v7'
    MAX_RETRIES = 5

    LOG_SUCCESS = 'Gratz! {bucket} ({url}) has received {text}!'
    LOG_FAILED = 'Request to {bucket} failed with status code {code}: {error}. Retrying after {seconds} seconds.'

    def __init__(self, token, **kwargs):
        self._token = token
        self._session = kwargs.get('session', asks.Session())
        self.limiter = Limiter()

        self.headers = {
            'User-Agent': self.create_user_agent(),
            'Authorization': kwargs.get('application_type', 'Bot').strip() + ' ' + self._token,
        }

    async def make_request(self, route, fmt=None, **kwargs):
        """Makes a request to a given endpoint with a set of arguments.

        This makes the request for you, handles the rate limits as well as
        non-success status codes and attempts up to 5 requests on failure.

        Parameters
        ----------
        route : tuple
            A tuple containing the HTTP method to use as well as the route to make the request to.
        fmt : dict
            The necessary keys and values to dynamically format the route.
        headers : dict, optional
            The headers to use for the request.
        retries : int, optional
            The amount of retries that have been made yet.

        Returns
        -------
        dict
            The API's JSON response.

        Raises
        ------
        ShitRequestFailed
            Will be raised on request failure or when the total amount of possible retries was exceeded.
        """

        fmt = fmt or {}
        retries = kwargs.pop('retries', 0)
        bucket_fmt = {key: value if key in ('guild', 'channel') else '' for key, value in fmt.items()}

        # Prepare the headers
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers

        if kwargs.get('reason'):
            kwargs['headers']['X-Audit-Log-Reason'] = quote(kwargs['reason'], '/ ')

        method = route[0].value
        bucket_endpoint = route[1].format(**bucket_fmt)
        bucket = (method, bucket_endpoint)
        url = self.BASE_URL + route[1].format(**fmt)

        logger.debug('Performing request to bucket %s with headers %s', bucket, kwargs['headers'])

        duration = await self.limiter.chill(bucket)
        if duration > 0:
            logger.debug('Bucket %s has been cooled down!', bucket)

        response = await self._session.request(method, url, **kwargs)
        data = response._actual_response = self.parse_response(response)
        status = response.status_code

        self.limiter.update_bucket(bucket, response)

        if 200 <= status < 300:
            # These status codes indicate successful requests. So just return the JSON response.
            logger.debug(self.LOG_SUCCESS.format(bucket=bucket, url=url, text=data))
            return data

        elif status != 429 and 400 <= status < 500:
            # These status codes are only caused by the dumb user and won't disappear with another request.
            # It'd be just a waste of performance to attempt sending another request.
            raise ShitRequestFailed(response, data, bucket)

        else:
            # Some retarded shit happened here. Let's try that again.
            retries += 1
            if retries > self.MAX_RETRIES:
                raise ShitRequestFailed(response, data, bucket, retries=self.MAX_RETRIES)

            backoff = randint(100, 50000) / 1000.0
            logger.debug(self.LOG_FAILED.format(bucket=bucket, code=status, error=response.content, seconds=backoff))
            await trio.sleep(backoff)

            return await self.make_request(route, fmt, retries=retries, **kwargs)

    @staticmethod
    def parse_response(response):
        if response.headers['Content-Type'] == 'application/json':
            return response.json()
        return response.text.encode('utf-8')

    @staticmethod
    def create_user_agent():
        fmt = 'DiscordBot ({0.__url__}, v{0.__version__}) / Python {1[0]}.{1[1]}.{1[2]}'
        return fmt.format(shitcord, sys.version_info)
