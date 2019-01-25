# -*- coding: utf-8 -*-

import enum
import typing

from .user import User


class StatusType(enum.Enum):
    """An enumeration for all the different status types supported by the Discord API.

    Attributes
    ----------
    ONLINE : str
        Indicates an online status.
    DND : str
        Indicates a Do Not Disturb status.
    IDLE : str
        Indicates an Idle status.
    INVISIBLE : str
        Indicates an invisible status.
    OFFLINE : str
        Indicates an offline status.
    """

    ONLINE         = 'online'  # noqa
    DND            = 'dnd'  # noqa
    IDLE           = 'idle'  # noqa
    INVISIBLE      = 'invisible'  # noqa
    OFFLINE        = 'offline'  # noqa


class ActivityType(enum.IntEnum):
    """An enumeration for all the different activity types supported by the Discord API.

    Attributes
    ----------
    PLAYING : int
        Use this for a ``playing ...`` presence. The value is 0.
    STREAMING : int
        Use this for a ``streaming ...`` presence. The value is 1.
    LISTENING : int
        Use this for a ``listening to ...`` presence. The value is 2.
    WATCHING : int
        Use this for a ``watching ...`` presence. The value is 3.
    """

    PLAYING   = 0  # noqa
    STREAMING = 1  # noqa
    LISTENING = 2  # noqa
    WATCHING  = 3  # noqa


class Activity:
    """Represents the activity of a User or a Bot

    Activities show what a User or Bot is doing right now.

    .. note:: This Model doesn't have Rich Presence stuff implemented.

    Attributes
    ----------
    name : str
        The activity's name.
    type : int
        The type of the activity.
    url : str, optional
        The URL of the stream, only when stream type is 1.
    """

    __slots__ = ('name', 'type', 'url')

    def __init__(self, *, name='', activity_type: typing.Union[int, ActivityType] = ActivityType.PLAYING, url=None):
        self.name = name
        self.type = activity_type.value if isinstance(activity_type, ActivityType) else activity_type
        self.url = url

    @classmethod
    def from_json(cls, data):
        return cls(name=data.get('name', ''), activity_type=data.get('activity_type', 0), url=data.get('url'))

    def to_json(self):
        # TODO: validate twitch.tv url
        if self.type == 1 and self.url is None:
            raise ValueError('Streaming status isn\'t allowed without a valid twitch.tv url provided.')

        return {
            'name': self.name,
            'type': self.type,
            'url': self.url
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<shitcord.Activity name={}>'.format(self.name)


class Presence:
    """Represents the current Presence of a User on a Guild.

    A user's presence is their current state on a guild.
    This event is sent when a user's presence or info, such as name or avatar, is updated.

    Attributes
    ----------
    user : :class:`User`
        The user presence is being updated for.
    roles : List[int]
        Roles the user is in.
    game : :class:`Activity`
        Null, or the user's current activity.
    guild_id : int
        ID of the guild.
    status : str
        Either idle, dnd, online, or offline.
    activities : List[:class:`Activity`]
        User's current activities.
    """

    __slots__ = ('user', 'roles', 'game', 'guild_id', 'status', 'activities')

    def __init__(self, data, http):
        self.user = data.get('user')
        if self.user:
            self.user = User(self.user, http)

        self.roles = data.get('roles')
        self.guild_id = data.get('guild_id')
        self.status = data.get('status')
        self.activities = [Activity.from_json(activity) for activity in data.get('activities', [])]

        self.game = data.get('game')
        if self.game:
            self.game = Activity.from_json(self.game)
