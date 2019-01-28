# -*- coding: utf-8 -*-

from ...utils import parse_time

from ... import models


class MessageDelete:
    __slots__ = ('id', 'channel_id', 'guild_id')

    def __init__(self, data, _):
        self.id = data['id']
        self.channel_id = int(data['channel_id'])
        self.guild_id = int(data['guild_id']) if data.get('guild_id') else None


class MessageDeleteBulk:
    __slots__ = ('ids', 'channel_id', 'guild_id')

    def __init__(self, data, _):
        self.ids = [int(id) for id in data['ids']]
        self.channel_id = int(data['channel_id'])
        self.guild_id = int(data['guild_id']) if data.get('guild_id') else None


class MessageReaction:
    __slots__ = ('user_id', 'channel_id', 'message_id', 'guild_id', 'emoji')

    def __init__(self, data, http):
        self.user_id = int(data['user_id'])
        self.channel_id = int(data['channel_id'])
        self.message_id = int(data['message_id'])
        self.guild_id = int(data['guild_id']) if data.get('guild_id') else None
        self.emoji = models.PartialEmoji(data['emoji'], http)


class MessageReactionRemoveAll:
    __slots__ = ('channel_id', 'message_id', 'guild_id')

    def __init__(self, data, _):
        self.channel_id = int(data['channel_id'])
        self.message_id = int(data['message_id'])
        self.guild_id = int(data['guild_id']) if data.get('guild_id') else None


class PresenceUpdate:
    __slots__ = ('user', 'roles', 'game', 'guild_id', 'status', 'activities')

    def __init__(self, data, http):
        self.user = models.User(data['user'], http)
        self.roles = [int(role_id) for role_id in data.get('roles', [])]
        self.game = models.Activity.from_json(data['game']) if data.get('game') else None
        self.guild_id = int(data['guild_id'])
        self.status = data['status']
        self.activities = [models.Activity.from_json(activity) for activity in data['activities']]


class TypingStart:
    __slots__ = ('channel_id', 'guild_id', 'user_id', 'timestamp')

    def __init__(self, data, _):
        self.channel_id = data['channel_id']
        self.guild_id = int(data['guild_id']) if data.get('guild_id') else None
        self.user_id = data['user_id']
        self.timestamp = parse_time(data['timestamp'])


class VoiceServerUpdate:
    __slots__ = ('token', 'guild_id', 'endpoint')

    def __init__(self, data, _):
        self.token = data['token']
        self.guild_id = int(data['guild_id'])
        self.endpoint = data['endpoint']


class WebhooksUpdate:
    __slots__ = ('guild_id', 'channel_id')

    def __init__(self, data, _):
        self.guild_id = int(data['guild_id'])
        self.channel_id = int(data['channel_id'])


class ChannelPinsUpdate:
    __slots__ = ('channel_id', 'timestamp')

    def __init__(self, data, _):
        self.channel_id = int(data['channel_id'])
        self.timestamp = parse_time(data.get('timestamp'))


class GuildBanAdd:
    __slots__ = ('guild_id', 'user')

    def __init__(self, data, http):
        self.guild_id = int(data['guild_id'])
        self.user = models.User(data['user'], http)


class GuildBanRemove:
    __slots__ = ('guild_id', 'user')

    def __init__(self, data, http):
        self.guild_id = int(data['guild.id'])
        self.user = models.User(data['user'], http)


class GuildEmojisUpdate:
    __slots__ = ('guild_id', 'emojis')

    def __init__(self, data, http):
        self.guild_id = int(data['guild.id'])
        self.emojis = [models.Emoji(self.guild_id, emoji, http) for emoji in data['emojis']]


class GuildIntegrationsUpdate:
    __slots__ = ('guild_id')

    def __init__(self, data, _):
        self.guild_id = data['guild_id']


class GuildMemberRemove:
    __slots__ = ('guild_id', 'user')

    def __init__(self, data, http):
        self.guild_id = data['guild_id']
        self.user = models.User(data['user'], http)


class GuildMemberUpdate:
    __slots__ = ('guild_id', 'roles', 'user', 'nick')

    def __init__(self, data, http):
        self.guild_id = data['guild_id']
        self.roles = [int(role_id) for role_id in data.get('roles', [])]
        self.user = models.User(data['user'], http)
        self.nick = data['nick']


class GuildMembersChunk:
    __slots__ = ('guild_id', 'members')

    def __init__(self, data, http):
        self.guild_id = int(data['guild_id'])
        self.members = [models.Member(member, http) for member in data['members']]


class GuildRoleCreate:
    __slots__ = ('guild_id', 'role')

    def __init__(self, data, http):
        self.guild_id = int(data['guild_id'])
        self.role = models.Role(data['role'], http)


class GuildRoleUpdate:
    __slots__ = ('guild_id', 'role')

    def __init__(self, data, http):
        self.guild_id = int(data['guild_id'])
        self.role = models.Role(data['role'], http)


class GuildRoleDelete:
    __slots__ = ('guild_id', 'role_id')

    def __init__(self, data, _):
        self.guild_id = int(data['guild_id'])
        self.role_id = int(data['role_id'])
