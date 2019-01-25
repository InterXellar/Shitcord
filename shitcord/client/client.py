# -*- coding: utf-8 -*-

import inspect
import logging
import time
from typing import Union

import trio

from ..models import Activity, ActivityType, StatusType
from ..gateway import DiscordWebSocketClient, Opcodes, _resolve_alias
from ..http import API, ShitRequestFailed
from ..utils import EventEmitter

logger = logging.getLogger('shitcord')


class ClientConfig:
    """Represents the config for your Discord bot.

    You need to create a subclass of :class:`ClientConfig` and set the
    necessary attributes.

    Attributes
    ----------
    token : str
        The token to run your Discord bot.
    prefix : Callable, str, list
        The prefix(es) for your Discord bot. Can be a callable returning the prefix or a list containing the prefixes.
    description : str, optional
        An optional description about your Discord bot.
    ignore_case : bool, optional
        Whether the bot should ignore case for commands. Defaults to ``False``.
    owner_id : int, list, optional
        The ID of the bot owner. If there are multiple owners, pass a list containing all owner IDs.
    logging_level : string, int, optional
        The logging level Shitcord should use. Defaults to ``logging.INFO``.
    session : :class:`asks.Session`, optional
        The :class:`asks.Session` the bot should use. If no session provided, the bot will create a new one.
    do_reconnect : bool, optional
        Whether the gateway client should reconnect or not. Defaults to ``True``.
    max_reconnects : int, optional
        The total amount of allowed reconnects. Defaults to ``5``.
    encoding : str, optional
        The encoding that should be used for gateway payloads. Either ``json`` or ``etf``. Defaults to ``json``.
    zlib_compressed : bool, optional
        Whether gateway payloads should be zlib compressed or not. Defaults to ``True``.
    shard_id : int, optional
        The ID of the shard to use. Must be less than shard_count and at least 0. If you're unsure, don't change the default value.
    shard_count : int, optional
        The amount of shards to use. Defaults to ``1``. If you're unsure, don't change the default value.
    """

    # general client configuration
    token = ''
    prefix = ''
    description = ''
    ignore_case = False
    owner_id = None
    logging_level = 'info'

    # configuration for the http client
    session = None

    # configuration for the gateway client
    do_reconnect = True
    max_reconnects = 5
    encoding = 'json'
    zlib_compressed = True
    shard_id = 0
    shard_count = 1

    def to_dict(self):
        """Returns a representation of the config as a dictionary."""

        # This one is tricky. First, we need to gather all class variables.
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith('_')]

        # Next, we need to remove all attributes with None as their value.
        attrs = filter(lambda attr: attr is not None, attrs)

        # Now we can return a dict representation.
        return {attr: getattr(self, attr) for attr in attrs}


class Client:
    """A client that is used for communication with the Discord API.

    Parameters
    ----------
    config : :class:`ClientConfig`
        A :class:`ClientConfig` the client should use.

    Attributes
    ----------
    config : :class:`ClientConfig`
        The client configuration.
    emitter : :class:`EventEmitter`
        The main event emitter for gateway event dispatches.
    api : :class:`shitcord.http.API`
        The client that wraps around the Discord REST API.
    ws : :class:`shitcord.gateway.DiscordWebSocketClient`
        The client that is used for interacting with the Discord Gateway.
    """

    def __init__(self, config: ClientConfig):
        self.config = config
        self.emitter = EventEmitter()

        # these attributes will be set later
        self.api = None
        self.ws = None
        self.app_info = None

        logger.level = self._get_logging_level(self.config.logging_level)

    def _get_logging_level(self, level: Union[str, int]):
        if isinstance(level, int):
            # If level is already an integer, there's no need to do any more conversion.
            return level
        elif isinstance(level, str):
            return logging._nameToLevel[level.upper()]
        else:
            raise TypeError('Invalid type for logging level has been specified.')

    async def connect(self):
        """|coro|

        Establishes a connection to the Discord Gateway and initializes the API client.

        .. note:: :meth:`Client.connect` is a blocking call.
        """

        logger.debug('Establishing connection to the Discord API...')
        token = self.config.token
        if not token:
            raise RuntimeError('No token provided.')

        self.api = API(token)
        # test the passed token
        try:
            # TODO: Wrap this into an object
            self.app_info = await self.api.get_current_application_info()
        except ShitRequestFailed as error:
            if error.status_code.value == 0:
                raise RuntimeError('Unable to login. An improper token has been passed.')

        self.ws = await DiscordWebSocketClient.from_client(self)

        # Call to the private method _start, because we can't use trio.run a second time.
        await self.ws._start()

    async def close(self):
        """|coro|

        Closes the connection to Discord.
        """

        await self.ws.close()
        del self.api
        del self.ws

    def start(self):
        """Runs the client.

        .. note:: :meth:`Client.start` is a blocking call.
        """

        trio.run(self.connect)

    def add_listener(self, callback, name=None, *, recurring=True):
        """Registers a new event listener.

        Parameters
        ----------
        callback : Callable
            The event callback to register.
        name : str, optional
            The event to register the callback for. Defaults to ``callback.__name__``.
        recurring : bool
            Whether this event should be dispatched more than one time or not.
        """

        name = name or callback.__name__
        self.emitter.add_listener(_resolve_alias(name), callback, recurring=recurring)
        logger.debug('Callback %s for event %s was successfully added!', callback.__name__, name)

    def remove_listener(self, event, callback):
        """Removes an event listener by callback.

        Parameters
        ----------
        event : str
            The name of the event where a callback should be removed.
        callback : Callable
            The callback to remove.
        """

        self.emitter.remove_listener(event, callback)
        logger.debug('Callback %s for event %s was successfully removed!', callback.__name__, event)

    def remove_listeners(self, event):
        """Removes all registered listeners for a given event.

        Parameters
        ----------
        event : str
            The name of the event.
        """

        self.emitter.remove_all_listeners(event)
        logger.debug('Successfully removed all callbacks for event %s!', event)

    def on(self, event: str):
        """A decorator to register a new client event.

        .. note:: You can register multiple event callbacks for the same event.

        .. code-block:: python3

            import shitcord


            class MyConfig(shitcord.ClientConfig):
                token = 'My Token'
                description = 'My super cool bot'
                owner_id = 12345


            client = shitcord.Client(MyConfig())


            @client.on('message')
            async def on_message(message):
                if message.author.bot:  # we don't want the bot to respond to other bots.
                    return

                if str(message).startswith('ayy'):
                    await message.respond('lmao')

            client.start()

        Parameters
        ----------
        event : str
            The name of the event.
        """

        def decorator(callback):
            if not inspect.iscoroutinefunction(callback):
                raise RuntimeError('Only coroutines are allowed for client event registration.')

            self.add_listener(callback, event, recurring=True)
            return callback

        return decorator

    def once(self, event: str):
        """A decorator to register a new client event.

        You use this decorator similarly to :meth:`Client.on`

        .. warning:: Events that were registered using this decorator will only be dispatched once.

        Parameters
        ----------
        event : str
            The name of the event.
        """

        def decorator(callback):
            if not inspect.iscoroutinefunction(callback):
                raise RuntimeError('Only coroutines are allowed for client event registration.')

            self.add_listener(callback, event, recurring=False)
            return callback

        return decorator

    async def dispatch(self, event, callback, *args):
        """Dispatches a custom event once.

        This will add a custom event to the main emitter,
        then dispatch the event one time with the given args
        and remove it from the emitter afterwards.

        Parameters
        ----------
        event : str
            The name of the event.
        callback : Callable
            The callback that corresponds to the event.
        args
            The args the callback should be called with.
        """

        self.add_listener(callback, event, recurring=False)
        await self.emitter.emit(event, *args)

    async def change_presence(self, *, activity: Activity = None, status: StatusType = StatusType.ONLINE, afk=False, since=0.0):
        """Changes the bot's presence in the Discord chat client.

        This allows you to set a "Playing ..."/"Watching ..."/"Listening to ..." presence,
        but also allows to change the status type (online, idle, invsible, dnd, ...).

        Parameters
        ----------
        activity : Activity
            An :class:`Activity` object containing all necessary information for the bot's presence.
        status : StatusType
            A valid :class:`StatusType` denoting the bot's status. E.g. online, streaming, dnd, ...
        afk : bool
            Whether or not the bot should be displayed as afk.
        since : float
            The interval in seconds for how the bot has been afk.
        """

        if not isinstance(activity, Activity):
            raise TypeError('activity must be an Activity object')

        if status is StatusType.IDLE and not since:
            since = int(time.time() * 1000)

        payload = {
            'since': since,
            'game': None,
            'status': status.name.lower(),
            'afk': afk,
        }

        if activity:
            payload['game'] = activity.to_json()

        return await self.ws.send(Opcodes.STATUS_UPDATE, payload)
