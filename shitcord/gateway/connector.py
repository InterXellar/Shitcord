# -*- coding: utf-8 -*-

import functools
import logging
import ssl
import typing
import zlib

import trio
import trio_websocket
from wsproto.frame_protocol import Opcode as WSOpcodes

from .encoding import ENCODERS
from .errors import NoMoreReconnects
from .opcodes import Opcodes
from .serialization import identify, resume
from ..utils import gateway, event_emitter

logger = logging.getLogger(__name__)
none_func = lambda *a, **kw: None


class DiscordWebSocketClient:
    VERSION = 6
    ZLIB_SUFFIX = b'\x00\x00\xff\xff'
    TEN_MEGABYTES = 10490000

    def __init__(self, *args, **kwargs):
        self.max_reconnects = kwargs.get('max_reconnects', 5)
        self.encoder = ENCODERS[kwargs.get('encoder', 'json')]
        self.zlib_compressed = kwargs.get('zlib_compressed', True)
        self._con = None

        # Necessary Gateway data
        url, shard, self.session_start_limit = args
        self._gateway_url = self.format_url(url)
        self.shard_id, self.shard_count = 0, shard  # Currently only support for one shard.

        # For connection state
        self.session_id = None
        self._trace = None
        self.sequence = None
        self.reconnects = 0
        self.shutting_down = trio.Event()
        self.do_reconnect = True

        # Heartbeating stuff
        self.interval = 0
        self._heartbeat_ack = True
        self._send_heartbeat, self._receive_heartbeat = trio.open_memory_channel(1)

        # Rate Limit handling. We are actually allowed to send 2 payloads per second, but let's give us a buffer.
        self.limiter = gateway.Limiter(1, 1)

        # Necessary for detecting zlib-compressed payloads
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()

        # For emitting received opcodes
        self.emitter = event_emitter.EventEmitter()

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

        cls.token = client.api.token

        return cls(*gateway_data, **client.config)

    def format_url(self, url):
        url += '?version={version}&encoding={encoding}'
        if self.zlib_compressed:
            url += '&compress=zlib-stream'

        return url.format(version=self.VERSION, encoding=self.encoder.TYPE)

    async def _send(self, opcode, payload):
        logger.debug('Sending %s', payload)
        await self._con.send_message(self.encoder.encode({
            'op': opcode.value if isinstance(opcode, Opcodes) else opcode,
            'd': payload,
        }))

    async def send(self, opcode: typing.Union[Opcodes, int], payload: typing.Union[dict, int, None]):
        await self.limiter.check()
        await self._send(opcode, payload)

    async def __heartbeat_task(self):
        await self._receive_heartbeat.receive()

        while not self.shutting_down.is_set() or self._con.closed:
            if not self._heartbeat_ack:
                logger.error('No HEARTBEAT_ACK received from that crap. Forcing a reconnect.')
                self._heartbeat_ack = True
                await self._close(4000, 'Zombied connection, you shitters!')
                break

            logger.debug('Sending Heartbeat with Sequence: %s.', self.sequence)
            await self._send(Opcodes.HEARTBEAT, self.sequence)
            self._heartbeat_ack = False
            await trio.sleep(self.interval / 1000)

    async def _handle_dispatch(self, event, payload):
        if event == 'ready':
            self.session_id = payload['session_id']

        # TODO: Caching & Updating already cached objects.

    async def _handle_heartbeat(self, _):
        logger.debug('Heartbeat requested by the Discord Gateway.')
        await self._send(Opcodes.HEARTBEAT, self.sequence)

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
        logger.debug('Received HEARTBEAT_ACK.')
        self._heartbeat_ack = True

    async def _message_task(self):
        while not self.shutting_down.is_set() or self._con.closed:
            try:
                message = await self._con.get_message()
            except trio_websocket.ConnectionClosed:
                break

            await self.on_message(message)

    def decompress(self, message):
        """Decompression algorithm for Gateway payloads."""

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
        """Identifying/Resuming"""

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
        logger.debug('Received message: %s', message)

        message = self.decompress(message)
        if not message:
            return

        try:
            payload = self.encoder.decode(message)
        except Exception:
            logger.debug('Failed to parse Gateway message: %s', message)
            return

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
        logger.debug('Connection was closed with code %s: %s', code, reason)

        # Clean up any old data
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()
        self.shutting_down.clear()

        if not self.do_reconnect:
            await self._con.aclose(1000)
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

        await self.on_close(con.closed.code, con.closed.reason)

    async def _start(self):
        async with trio.open_nursery() as nursery:
            logger.debug('Starting Nursery!')
            self.emitter.emit = functools.partial(self.emitter.emit, nursery=nursery)

            nursery.start_soon(self.connect, nursery)
            nursery.start_soon(self.__heartbeat_task)

    async def close(self):
        logger.debug('Shutting down the Gateway client.')
        self.do_reconnect = False
        await self._close(1000)

    async def _close(self, code, reason=None):
        await self._con.aclose(code, reason)
        self.shutting_down.set()

    def start(self):
        trio.run(self._start)
