import functools
import inspect
import typing

import trio

__all__ = ['RESTShit', 'rest_shit']


async def maybe_awaitable(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


class RESTShit:
    """Implements Shitcord's high-level interface for requests to the REST API.

    RESTShits are used to change the specific behavior of requests to extend the
    customizability of making requests to the Discord REST API.
    Here's an example:

    .. code-block:: python

        await channel.send('Hey there!')  # A regular, asynchronous RESTShit.
        await channel.send('Hey there!').wait()  # This kind of RESTShit blocks until the message was sent.
        await channel.send('Hey there!').after(30)  # Schedules the message to be sent after 30 seconds.

    .. note:: This is inspired from JDA's RestActions_.

    .. _RestActions: https://github.com/DV8FromTheWorld/JDA/wiki/7%29-Using-RestAction
    """

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        self._lock = trio.Semaphore(1)
        self._result = None

    def __repr__(self):
        return '<shitcord.RESTShit callback={0.callback} args={0.args} kwargs={0.kwargs}>'.format(self)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def __await__(self):
        return maybe_awaitable(self.callback, *self.args, **self.kwargs).__await__()

    async def wait(self, timeout=None):
        """|coro|

        This blocks until the request finished and returns the result.
        You can specify an optional timeout if you want to limit how long
        a request can take.

        Parameters
        ----------
        timeout : int, float, optional
            An optional timeout after which the RESTShit should fail.

        Returns
        -------
        The regular return value of the performed request.

        Raises
        ------
        trio.TooSlowError
            For the case you provided a timeout and the RESTShit timed out, this exception will be raised.
        """

        await self._lock.acquire()

        async def _release_lock():
            result = await self.callback(*self.args, **self.kwargs)
            self._lock.release()
            self.result = result

        async with trio.open_nursery() as nursery:
            if timeout is not None:
                async with trio.fail_after(timeout):
                    nursery.start_soon(_release_lock)
            else:
                nursery.start_soon(_release_lock)

        return self.result

    async def nursery(self):
        """|coro|

        Returns the nursery that executes the RESTShit, e.g. if you want to cancel a request.

        Returns
        -------
        trio._core._run.Nursery
            The nursery for this RESTShit.
        """

        async with trio.open_nursery() as nursery:
            nursery.start_soon(functools.partial(self.callback, *self.args, **self.kwargs))
            return nursery

    async def memory_channel(self, nursery):
        """|coro|

        This basically schedules the RESTShit to run after :class:`trio.abc.ReceiveChannel`
        receives a message from the :class:`trio.abc.SendChannel` that was returned.

        Note that this method must always take a parameter representing a nursery, otherwise
        there would be blocking problems for your code.

        Parameters
        ----------
        nursery
            The nursery that should be used to run the callback task.

        Returns
        -------
        trio.abc.SendChannel
            A channel you should send a message to in order to complete the RESTShit.
        """

        _send_channel, _receive_channel = trio.open_memory_channel(1)

        async def _call_after_receive():
            await _receive_channel.receive()
            return await self.callback(*self.args, **self.kwargs)

        nursery.start_soon(_call_after_receive)
        return _send_channel

    async def after(self, interval, *, action: typing.Optional[typing.Callable] = None, timeout=None):
        """|coro|

        Performs a task after a given interval. This one might be a bit more tricky than the other.
        Example:
            .. code-block:: python

                await channel.send('Hi').after(30)  # 'Hi' will be sent to the channel after 30 seconds.

        Then you've got a couple more actions you can perform with this method.
        For example by using the `action` parameter:

        .. code-block:: python

            # This example demonstrates how to use the `action` parameter.
            # The lambda expression will be called with the result from `channel.send`
            # which is the created message object. This way, the final return value of
            # this statement is the message content. Of course, this will run after 30 seconds.
            content = await channel.send('Hi').after(30, action=lambda message: message.content)

        Parameters
        ----------
        interval : int, float
            The interval after which the RESTShit should be executed.
        action : Optional[Callable]
            The action that should be performed after the interval has passed.
            If you just want to schedule the execution of your RESTShit, leave this to `None`.
        timeout : int, float, optional
            An optional timeout after which the RESTShit should fail.

        Returns
        -------
        Either the result of the request itself or the result of the invoked `action`.

        Raises
        ------
        ValueError
            Will be raised when an invalid string literal was provided for `action`.
        trio.TooSlowError
            Will be raised when the optional timeout was set and the RESTShit timed out.
        """

        await trio.sleep(interval)

        if callable(action):
            result = await self.callback(*self.args, **self.kwargs)
            callback = action
            args = (result,)
            kwargs = {}

        else:
            callback = self.callback
            args = self.args
            kwargs = self.kwargs

        if timeout is None:
            return await maybe_awaitable(callback, *args, **kwargs)
        else:
            async with trio.fail_after(timeout):
                return await maybe_awaitable(callback, *args, **kwargs)


def rest_shit(*, cls=None):
    """A decorator that turns the decorated function into a :class:`RESTShit`.

    This decorator also allows you to pass your own custom class for RESTShits
    to extend its functionality.

    .. note:: Any passed class should inherit from :class:`RESTShit`.

    .. code-block:: python

        \"\"\"
        User: Wow! This is really awesome shit! Can I make my own RESTShits?
        Vale: Sure! Let me give you an example.
        \"\"\"

        @shitcord.rest_shit()
        async def my_rest_shit():
            ...

    Parameters
    ----------
    cls : :class:`RESTShit`, optional
        An optional class the decorated function should be turned to.
        Please don't change the default value unless you know what you are doing.
    """

    if cls is None:
        cls = RESTShit

    def decorator(func):
        if isinstance(func, RESTShit):
            raise TypeError('Callback is already a RESTShit.')
        if not inspect.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cls(func, *args, **kwargs)

        return wrapper
    return decorator
