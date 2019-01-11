import queue
import signal
import threading
from functools import partial

import multio
import trio


class SyncExecution(threading.Thread):
    def __init__(self):
        super().__init__()

        self.running = False
        self.daemon = True

        self.in_queue = queue.Queue(1)
        self.out_queue = queue.Queue(1)

    def execute_coro(self, coro, *args, **kwargs):
        if self.running:
            return coro(*args, **kwargs)

        self.running = True
        self.in_queue.put((coro, args, kwargs))

        while self.running:
            if self.out_queue.full():
                self.running = False
                value = self.out_queue.get()
                if isinstance(value, BaseException):
                    raise value
                return value

    def run(self):
        multio.init(trio)

        while True:
            coro, args, kwargs = self.in_queue.get()
            try:
                result = trio.run(partial(coro, *args, **kwargs))
            except BaseException as error:
                result = error

            self.out_queue.put(result)


_thread = SyncExecution()
_thread.start()

from .cls_wrapper import (  # noqa
    DiscordWebSocketClient,
    Colour,
    Color,
    Emoji,
    Invite,
    Member,
    PartialChannel,
    PartialEmoji,
    Permissions,
    TextChannel,
    DMChannel,
    Role,
    VoiceChannel,
    GroupDMChannel,
    CategoryChannel,
    User,
    Webhook,
    HTTP,
    Limiter,
    API,
    EventEmitter,
    GatewayLimiter,
    Cache
)

signal.signal(signal.SIGINT, signal.SIG_DFL)
