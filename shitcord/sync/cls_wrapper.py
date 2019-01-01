import inspect
from functools import wraps

import shitcord

from . import _thread


class SyncMeta:
    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if inspect.iscoroutinefunction(attr):

            @wraps(attr)
            def decorator(*args, **kwargs):
                return _thread.execute_coro(attr, *args, **kwargs)

            setattr(self, item, decorator)
            return decorator
        return attr


class HTTP(shitcord.http.HTTP, SyncMeta):
    pass


class Limiter(shitcord.http.Limiter, SyncMeta):
    pass


class Endpoints(shitcord.http.Endpoints, SyncMeta):
    pass
