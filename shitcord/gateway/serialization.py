import functools
import json
import sys

from .opcodes import Opcodes
from ..utils.jsonenum import EnumEncoder


def dump(val):
    return json.dumps(val, cls=EnumEncoder)


def dump_result(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return dump(func(*args, **kwargs))

    return wrapped


class JSON:

    @staticmethod
    @dump_result
    def heartbeat(d=None):
        return {
            'op': Opcodes.HEARTBEAT,
            'd': d
        }

    @staticmethod
    @dump_result
    def identify(token, game=None):
        return dict(
            op=Opcodes.IDENTIFY,
            d=dict(
                token=token,
                properties={
                    '$os': sys.platform,
                    '$browser': "Shitcord",
                    '$device': "Shitcord",
                }
            ),
            compress=False,
            large_threshold=250,
            shard=[0, 1],
            presence=game or {"status": "online", "since": 91879201, "afk": False}
        )
