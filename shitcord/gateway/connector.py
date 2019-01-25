# -*- coding: utf-8 -*-

import functools
import logging
import ssl
import time
import typing
import zlib
from contextlib import contextmanager

import contextvars  # trio includes a backport for lower Python versions than 3.7
import trio
import trio_websocket
from wsproto.frame_protocol import Opcode as WSOpcodes

from .encoding import ENCODERS
from .errors import GatewayException, NoMoreReconnects
from .events import parse_event
from .gateway import WebSocketClient
from .opcodes import Opcodes
from .serialization import identify, resume
from ..utils import gateway

logger = logging.getLogger(__name__)
none_func = lambda *a, **kw: None


class DiscordWebSocketClient(WebSocketClient):
    """Implements a WebSocket client for the Discord Gateway v6.

    WebSockets will be used to establish a connection to the Discord Gateway.
    It is a way of real-time communication between Discord and your bot, so mostly the connection
    will be used for receiving events e.g. indicating when somebody sent a message.

    The Gateway lifecycle is quite complex and demanding. For more details, see: https://s.gus.host/flowchart.svg

    .. note:: This class should always be initialized via :meth:`from_client`.

    .. warning:: As a library user you should never create an instance of this class manually.

    Parameters
    ----------
    url : str
        The WebSocket URL received from the `Get Gateway Bot` endpoint.
    shard : int
        The amount of recommended shards, received from the `Get Gateway Bot` endpoint.
    session_start_limit : dict
        The session start limit for this bot, received from the `Get Gateway Bot` endpoint.
    max_reconnects : int
        A keyword argument, describing how often a bot is allowed to reconnect. Defaults to 5.
    encoding : str
        A keyword argument denoting the encoding of the Gateway payloads. Either `'json'` or `'etf'`.
    zlib_compressed : bool
        A keyword argument to indicate whether Gateway payloads should be compressed or not. Defaults to `True`.

    Attributes
    ----------
    VERSION : int
        A constant defining the Gateway version. This should always be 6.
    ZLIB_SUFFIX : bytes
        A constant defining the zlib suffix that will be used for detecting zlib-compressed payloads.
    TEN_MEGABYTES : int
        A constant defining the initial size of the output buffer for zlib decompression should always be 10 mb.

    max_reconnects : int
        The total amount of allowed reconnects after the connection was closed.
    encoder : :class:`BaseEncoder`
        Represents an encoder and decoder for Gateway payloads. Either :class:`ETFEncoder` or :class:`JSONEncoder`.
    zlib_compressed : bool
        Whether payloads from the Discord Gateway should be compressed or not.
    session_start_limit : dict
        The session start limit sent by the Discord Gateway.
    session_id : str
        The ID for the current session.
    sequence : int
        The sequence that will be used for heartbeating and resuming connections.
    reconnects : int
        Indicates how many reconnects were already made.
    shutting_down : :class:`trio.Event`
        An event that will be used to close the Gateway connection.
    do_reconnect : bool
        A boolean indicating whether the client should reconnect.
    latency : float
        The WebSocket latency between sent Heartbeats and received HEARTBEAT_ACKs in microseconds.
    interval : int
        The interval after which the client should send heartbeats.
    limiter : :class:`shitcord.utils.Limiter`
        A rate limiter for the Discord Gateway.
    emitter : :class:`EventEmitter`
        An event emitter for emitting received gateway events.
    token : str
        The bot token.
    """

    VERSION = 6
    ZLIB_SUFFIX = b'\x00\x00\xff\xff'
    TEN_MEGABYTES = 10490000

    def __init__(self, *args, **kwargs):
        self.max_reconnects = kwargs.get('max_reconnects', 5)
        self.encoder = ENCODERS[kwargs.get('encoding', 'json')]
        self.zlib_compressed = kwargs.get('zlib_compressed', True)
        self._con = None

        # Necessary Gateway data
        url, shard, self.session_start_limit = args
        self._gateway_url = self.format_url(url)
        self.shard_id, self.shard_count = kwargs.get('shard_id', 0), kwargs.get('shard_count', shard)  # Currently only support for one shard.

        # For connection state
        self.session_id = None
        self._trace = None
        self.sequence = None
        self.reconnects = 0
        self.shutting_down = trio.Event()
        self.do_reconnect = True
        self._last_sent = time.perf_counter()
        self._last_ack = time.perf_counter()
        self.latency = float('inf')

        # For caching all sent and received WebSocket messages.
        self._received_messages = contextvars.ContextVar('_received_messages', default=[])
        self._sent_messages = contextvars.ContextVar('_sent_messages', default=[])

        # Heartbeating stuff
        self.interval = 0
        self._heartbeat_ack = True
        self._send_heartbeat, self._receive_heartbeat = trio.open_memory_channel(1)

        # Rate Limit handling. We are actually allowed to send 2 payloads per second, but let's give us a buffer.
        self.limiter = gateway.Limiter(1, 1)

        # Necessary for detecting zlib-compressed payloads
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()

        # Bind corresponding callbacks for opcodes sent by the Discord API
        self.emitter.on('DISPATCH', self._handle_dispatch)
        self.emitter.on('HEARTBEAT', self._handle_heartbeat)
        self.emitter.on('RECONNECT', self._handle_reconnect)
        self.emitter.on('INVALID_SESSION', self._handle_invalid_session)
        self.emitter.on('HELLO', self._handle_hello)
        self.emitter.on('HEARTBEAT_ACK', self._handle_heartbeat_ack)

    @classmethod
    async def from_client(cls, client):
        gateway_data = await client.api.get_gateway_bot()

        cls.api = client.api
        cls.emitter = client.emitter
        cls.token = client.api.token

        return cls(*gateway_data, **client.config.to_dict())

    def format_url(self, url: str):
        url += '?version={version}&encoding={encoding}'
        if self.zlib_compressed:
            url += '&compress=zlib-stream'

        return url.format(version=self.VERSION, encoding=self.encoder.TYPE)

    @contextmanager
    def received_messages(self):
        """A contextmanager that yields all messages that were received from the Discord Gateway.

        PLEASE DO ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING!
        """

        messages = self._received_messages.get()

        try:
            yield messages
        finally:
            self._received_messages.set([])

    @contextmanager
    def sent_messages(self):
        """A contextmanager that yields all messages that were sent to the Discord Gateway.

        PLEASE DO ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING!
        """

        messages = self._sent_messages.get()

        try:
            yield messages
        finally:
            self._sent_messages.set([])

    async def _send(self, opcode, payload):
        logger.debug('Sending %s', payload)
        message = {
            'op': opcode.value if isinstance(opcode, Opcodes) else opcode,
            'd': payload,
        }

        self._sent_messages.get().append(message)
        await self._con.send_message(self.encoder.encode(message))

    async def send(self, opcode: typing.Union[Opcodes, int], payload: typing.Union[dict, int] = None):
        """|coro|

        Sends a message to the Discord gateway and handles the rate limit.

        Parameters
        ----------
        opcode : :class:`shitcord.gateway.Opcodes`, int
            The opcode that should be sent.
        payload : dict, int, optional
            The payload that should be sent.
        """

        await self.limiter.check()
        await self._send(opcode, payload)

    async def __heartbeat_task(self):
        if not self.interval:
            await self._receive_heartbeat.receive()

        if not self._heartbeat_ack:
            logger.error('No HEARTBEAT_ACK received from that crap. Forcing a reconnect.')
            self._heartbeat_ack = True
            await self._close(4000, 'Zombied connection, you shitters!')
            return

        logger.debug('Sending Heartbeat with Sequence: %s.', self.sequence)
        await self._send(Opcodes.HEARTBEAT, self.sequence)
        self._last_sent = time.perf_counter()
        self._heartbeat_ack = False

        await trio.sleep(self.interval / 1000)

        if not self.shutting_down.is_set() or self._con.closed:
            await self.__heartbeat_task()

    async def _handle_dispatch(self, event, payload):
        if event == 'ready':
            self.session_id = payload['session_id']

        # TODO: Caching & Updating already cached models.

        name, handler = parse_event(event, payload, self.api.get_api())

        await self.emitter.emit(name, handler)

    async def _handle_heartbeat(self, _):
        logger.debug('Heartbeat requested by the Discord Gateway.')
        await self._send(Opcodes.HEARTBEAT, self.sequence)
        self._last_sent = time.perf_counter()

    async def _handle_reconnect(self, _):
        logger.debug('Received Opcode 7: RECONNECT. Forcing a reconnect.')
        self.session_id = None
        self.shutting_down.set()

    async def _handle_invalid_session(self, _):
        logger.debug('Received Opcode 9: INVALID_SESSION. Forcing a reconnect.')
        self.session_id = None
        self.shutting_down.set()

    async def _handle_hello(self, payload):
        logger.debug('Received Opcode 10: HELLO. Starting to perform the heartbeat task.')
        self.interval = payload['heartbeat_interval']
        self._trace = payload['_trace']
        await self._send_heartbeat.send('Heartbeat!')

    async def _handle_heartbeat_ack(self, _):
        ack_time = time.perf_counter()
        self._last_ack = ack_time
        self.latency = ack_time - self._last_sent
        logger.debug('Received HEARTBEAT_ACK.')
        self._heartbeat_ack = True

    def _decompress(self, message):
        if self.zlib_compressed:
            self._buffer.extend(message)

            if len(message) < 4 or message[-4:] != self.ZLIB_SUFFIX:
                return

            message = self._inflator.decompress(self._buffer)
            if self.encoder.OPCODE is WSOpcodes.TEXT:
                message = message.decode('utf-8')

            self._buffer = bytearray()
        else:
            # As there are special cases where zlib-compressed payloads also occur, even
            # if zlib-stream wasn't specified in the Gateway url, also try to detect them.
            is_json = message[0] == '{'
            is_etf = message[0] == 131
            if not is_json and not is_etf:
                message = zlib.decompress(message, 15, self.TEN_MEGABYTES).decode('utf-8')

        return message

    async def on_open(self):
        """|coro|

        Will be called once the WebSocket connection was established.

        .. warning:: This should only be called internally by the client.

        From here, an identify/resume payload will be sent to establish a real "connection" to the Discord Gateway.
        """

        session_id, sequence = self.session_id, self.sequence
        if session_id and sequence:
            # As of these attributes being set, we try to resume the connection.
            logger.debug('WebSocket connection established: Trying to resume with Session ID: %s and Sequence: %s.', session_id, sequence)
            await self._send(Opcodes.RESUME, resume(self.token, session_id, sequence))

        else:
            logger.debug('WebSocket connection established: Sending Identify payload.')
            shard = [self.shard_id, self.shard_count]
            await self._send(Opcodes.IDENTIFY, identify(self.token, shard=shard))

    async def on_message(self, message):
        """|coro|

        Will be called when a received gateway message was successfully polled from the queue.
        This decompresses and decodes a payload and emits the corresponding opcode event.

        .. warning:: This should only be called internally by the client.
        """

        logger.debug('Received message: %s', message)

        message = self._decompress(message)
        if not message:
            return

        try:
            payload = self.encoder.decode(message)
        except Exception:
            raise GatewayException('Failed to parse Gateway message: {}'.format(message))

        # Cache the received message in JSON format.
        self._received_messages.get().append(payload)

        # Update the sequence if given because it is necessary for keeping the connection alive.
        if payload['s']:
            self.sequence = payload['s']

        opcode = Opcodes(payload['op'])
        data = payload['d']

        if opcode is Opcodes.DISPATCH:
            event = payload['t']
            logger.debug('Received event dispatch: %s', event)

            await self.emitter.emit(opcode.name, event.lower(), data)
            return

        await self.emitter.emit(opcode.name, data)

    async def on_close(self, code, reason=None):
        """|coro|

        Will be called once the WebSocket connection was closed.
        Cleans up any old data and handles reconnecting.

        .. warning:: This should only be called internally by the client.
        """

        logger.debug('Connection was closed with code %s: %s', code, reason)

        # Clean up any old data
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()
        self.shutting_down.clear()
        self._con = None

        if not self.do_reconnect:
            return

        self.reconnects += 1
        if self.reconnects > self.max_reconnects:
            raise NoMoreReconnects('Total amount of allowed reconnects was exceeded.')

        if code and 4000 <= code <= 4011:
            self.session_id = None
            self.interval = None

        action = 'resume' if self.session_id else 'reconnect'
        delay = self.reconnects + 10
        logger.debug('Connection was closed. Attempting to %s after %s.', action, delay)
        await trio.sleep(delay)

        await self._start()

    async def connect(self, nursery):
        """Opens a WebSocket connection to the Discord Gateway."""

        # Handling the session start limit from the Gateway.
        if self.session_start_limit['remaining'] <= 0:
            duration = self.session_start_limit['reset_after'] / 1000
            logger.debug('Total amount of allowed session starts was exceeded. Sleeping for %s until the limit resets.', duration)
            await trio.sleep(duration)

        logger.debug('Opening a WebSocket connection to the Discord Gateway with url `%s`', self._gateway_url)
        async with trio_websocket.open_websocket_url(self._gateway_url, ssl.SSLContext(ssl.PROTOCOL_SSLv23)) as con:
            self._con = con
            nursery.start_soon(self._message_task)
            await self.on_open()

            await self.shutting_down.wait()

        await self.on_close(con.closed.code.value, con.closed.reason)

    async def _start(self):
        async with trio.open_nursery() as nursery:
            logger.debug('Starting Nursery!')
            self.emitter.emit = functools.partial(self.emitter.emit, nursery=nursery)

            nursery.start_soon(self.connect, nursery)
            nursery.start_soon(self.__heartbeat_task)

    async def close(self):
        """Closes the Gateway connection."""

        logger.debug('Shutting down the Gateway client.')
        self.do_reconnect = False
        await self._close(1000)

    async def _close(self, code, reason=None):
        await self._con.aclose(code, reason)
        self.shutting_down.set()
