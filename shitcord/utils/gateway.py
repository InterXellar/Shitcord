# -*- coding: utf-8 -*-

import trio


class Limiter:
    """Represents a simple rate limiter mainly used for the Discord Gateway.

    A client is allowed to send up to 2 payloads per second, which counts up to a total of 30 payloads per 60 seconds.
    This class will simply be used to produce a delay before actually sending a payload.

    Parameters
    ----------
    total : int
        The total amount of allowed payloads...
    per : int
        ...per the provided time interval in seconds.
    """

    def __init__(self, total, per):
        self.total = total
        self.per = per
        self._lock = trio.Semaphore(self.total)

    async def check(self):
        await self._lock.acquire()

        async def _release_lock():
            await trio.sleep(self.per)
            self._lock.release()

        async with trio.open_nursery() as nursery:
            nursery.start_soon(_release_lock)
