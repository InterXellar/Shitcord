# -*- coding: utf-8 -*-

import collections
import functools
import inspect
import typing

import trio

# A basic event object definition.
Event = collections.namedtuple('Event', 'func recurring')


class EventError(Exception):
    """Base exception for event emitting."""


class EventEmitter:
    """Implements event emitter functionality inspired by NodeJS.

    Every callback is executed by creating a background task.
    """

    __callbacks = collections.defaultdict(list)
    __lock = trio.Lock()

    def add_listener(self, event, callback: typing.Callable = None, *, recurring=True):
        """Registers a callback for the specified event.

        Can be used as decorator if only the `event` parameter is specified.
        To listen for any event, use :class:`None` as event identifier.

        Parameters
        ----------
        event : str
            The name of the event that will be used for dispatching the event.
        callback : typing.Callable, optional
            The callback that should be executed when the event was dispatched.
        recurring : bool, optional
            Whether or not the event should only be executed more than once. Defaults to True.
        """

        # When called as function
        if callback:
            if not inspect.iscoroutinefunction(callback):
                raise EventError('Only coroutines are allowed for registration of callbacks.')

            with self.__lock:
                self.__callbacks[event].append(Event(func=callback, recurring=recurring))
            return

        # When used for decorating an event
        def decorator(callback):
            if not inspect.iscoroutinefunction(callback):
                raise EventError('Only coroutines are allowed for registration of callbacks.')

            with self.__lock:
                self.__callbacks[event].append(Event(func=callback, recurring=recurring))
            return callback

        return decorator

    # A shorter alias for registration of events.
    on = add_listener

    once = functools.partial(add_listener, recurring=False)

    def remove_listener(self, event, callback: typing.Callable):
        """Removes a callback for a given event.

        You need to pass the event's name and the corresponding callback
        to ensure that the correct callback will be removed.

        If you are looking for something to remove all callbacks for a given event,
        see :meth:`remove_all_listeners`.

        Parameters
        ----------
        event : str
            The name of the event where a callback should be removed.
        callback : typing.Callable
            The callback reference.
        """

        if event in self.__callbacks:
            with self.__lock:
                self.__callbacks[event] = [event for event in self.__callbacks[event] if event.func != callback]

    def remove_all_listeners(self, event=None):
        """Removes all registered callbacks.

        Depending on whether or not you specified the event, this will
        either remove any registered callbacks or just the callbacks
        for the specified event.

        Parameters
        ----------
        event : str, optional
            An optional event reference if only the callbacks for a specific event should be removed.
        """

        if not event:
            self.__callbacks.clear()
        elif event in self.__callbacks:
            with self.__lock:
                self.__callbacks.pop(event, None)

    async def emit(self, event, *args):
        """Emits an event with some arguments.

        You can specify args that should be passed to the function.
        This calls any registered callback for an event with the given arguments.

        Parameters
        ----------
        event : str
            The event that should be emitted.
        args
            Some arguments that should be passed to the event callback.

        Raises
        ------
        EventError
            Will be raised when an unregistered event was emitted.
        """

        with self.__lock:
            new_events = []
            for event in self.__callbacks.pop(event, []):
                if not inspect.iscoroutinefunction(event.func):
                    raise EventError('Only coroutines are allowed for event emitting.')

                if event.recurring:
                    new_events.append(event)

                async with trio.open_nursery() as nursery:
                    nursery.start_soon(event.func, *args)

            if new_events:
                self.__callbacks[event] = new_events

    async def emit_after(self, delay, event, *args):
        """Emits an event with some arguments after a given amount of time.

        You can specify args that should be passed to the function.
        This calls any registered callback for an event with the given arguments.

        Parameters
        ----------
        delay : int, float
            The delay after which the event should be emitted.
        event : str
            The event that should be emitted.
        args
            Some arguments that should be passed to the event callback.

        Raises
        ------
        EventError
            Will be raised when an unregistered event was emitted.
        """

        await trio.sleep(delay)
        return await self.emit(event, *args)

    async def wait(self, name, *, timeout=30.0):
        """Waits until an event was dispatched and returns its parameters.

        This blocks until an event was dispatched or it times out.

        Parameters
        ----------
        name : str
            The event that should be waited for.
        timeout : int, float, optional
            The timeout after which the function should error.

        Raises
        ------
        trio.TooSlowError
            Will be raised when the timeout was exceeded without any results.
        """

        data = None
        event = trio.Event()

        async def callback(*args):
            nonlocal data, event
            data = args[0] if len(args) == 1 else args
            event.set()

        self.add_listener(name, callback, recurring=False)
        with trio.fail_after(timeout):
            await event.wait()
        return data
