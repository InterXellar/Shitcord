# -*- coding: utf-8 -*-

import abc

import trio
import trio_websocket


class WebSocketClient(abc.ABC):
    """Defines a basic wrapper around the ``trio-websocket`` library.

    This ABC is some sort of template for any WebSocket client that should be implemented
    for Shitcord.

    .. note::
        Any subclass should have an attribute called `_con` that represents an instance of
        `WebSocketConnection <https://trio-websocket.readthedocs.io/en/latest/api.html#trio_websocket.WebSocketConnection>`_.

    Make sure to override all abstractmethods when subclassing from :class:`WebSocketClient`.
    """

    VERSION = None

    @classmethod
    @abc.abstractmethod
    async def from_client(cls, client):
        """|coro|

        Initializes a WebSocket client from a given client.

        Subclasses must override this and they might handle different client types
        for this method.
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, opcode, payload=None):
        """|coro|

        Sends a message to the opened WebSocketConnection via ``await self._con.send_message(...)``.

        You must ensure that his method correctly formats the payloads that should be sent and correctly
        handles rate limits.
        """

        raise NotImplementedError

    async def __heartbeat_task(self):
        """|coro|

        Defines a recursive method that is used for heartbeating.

        All WebSocket connections to the Discord gateway require some sort of heartbeating
        to keep them alive. Depending on the gateway type, the way of how these heartbeats should
        be performed may vary.
        """

        raise NotImplementedError

    async def _message_task(self):
        try:
            message = await self._con.get_message()
        except trio_websocket.ConnectionClosed:
            return

        await self.on_message(message)
        await self._message_task()

    @abc.abstractmethod
    async def on_open(self):
        """|coro|

        This coroutine should implement some sort of task that should be performed
        after a WebSocket connection was established.
        This could for example handle identifying/resuming or just some debug logs.
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def on_message(self, message):
        """|coro|

        Will be called when a WebSocket message was received.
        This method should implement the logic about how these messages should be handled
        and store necessary information from them.
        """

        raise NotImplementedError

    async def on_close(self, code, reason=None):
        """|coro|

        Should be called once a WebSocket connection was closed.
        This could handle some sort of reconnecting or clear any old data.
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def connect(self, nursery):
        """|coro|

        Handles the creation of an actual WebSocket connection.
        Once a connection was created, set the _con attribute from here.

        Further, this method should implement the call to :meth:`on_close`.
        It should always be called with a nursery argument that is used to spawn child tasks
        e.g. :meth:`_message_task`.
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def _start(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.connect, nursery)

    @abc.abstractmethod
    async def close(self):
        """|coro|

        This method should be used for closing the WebSocket connection
        in a natural way (which means close code 1000).

        It should only be called for expected connection terminations.
        """

        raise NotImplementedError

    def start(self):
        """Starts the client."""

        trio.run(self._start)
