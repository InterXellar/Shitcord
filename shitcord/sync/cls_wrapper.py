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


class Client(shitcord.Client, SyncMeta):
    pass


class DiscordWebSocketClient(shitcord.gateway.DiscordWebSocketClient, SyncMeta):
    pass


class Colour(shitcord.Colour, SyncMeta):
    pass


Color = Colour


class Emoji(shitcord.Emoji, SyncMeta):
    pass


class Guild(shitcord.Guild, SyncMeta):
    pass


class PartialGuild(shitcord.PartialGuild, SyncMeta):
    pass


class Invite(shitcord.Invite, SyncMeta):
    pass


class Member(shitcord.Member, SyncMeta):
    pass


class PartialChannel(shitcord.PartialChannel, SyncMeta):
    pass


class PartialEmoji(shitcord.PartialEmoji, SyncMeta):
    pass


class Attachment(shitcord.Attachment, SyncMeta):
    pass


class File(shitcord.File, SyncMeta):
    pass


class Message(shitcord.Message, SyncMeta):
    pass


class Permissions(shitcord.Permissions, SyncMeta):
    pass


class TextChannel(shitcord.TextChannel, SyncMeta):
    pass


class DMChannel(shitcord.DMChannel, SyncMeta):
    pass


class Role(shitcord.Role, SyncMeta):
    pass


class VoiceChannel(shitcord.VoiceChannel, SyncMeta):
    pass


class GroupDMChannel(shitcord.GroupDMChannel, SyncMeta):
    pass


class CategoryChannel(shitcord.CategoryChannel, SyncMeta):
    pass


class User(shitcord.User, SyncMeta):
    pass


class VoiceState(shitcord.VoiceState, SyncMeta):
    pass


class VoiceRegion(shitcord.VoiceRegion):
    pass


class Webhook(shitcord.Webhook, SyncMeta):
    pass


class HTTP(shitcord.http.HTTP, SyncMeta):
    pass


class CooldownBucket(shitcord.http.CooldownBucket, SyncMeta):
    pass


class Limiter(shitcord.http.Limiter, SyncMeta):
    pass


class API(shitcord.http.API, SyncMeta):
    pass


class RESTShit(shitcord.http.RESTShit, SyncMeta):
    pass


class EventEmitter(shitcord.EventEmitter, SyncMeta):
    pass


class GatewayLimiter(shitcord.utils.Limiter, SyncMeta):
    pass


class Cache(shitcord.utils.Cache, SyncMeta):
    pass
