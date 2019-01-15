# -*- coding: utf-8 -*-

import enum

from .user import User


class StatusType(enum.Enum):
    ONLINE         = 'online'
    DND            = 'dnd'
    IDLE           = 'idle'
    INVISIBLE      = 'invisible'
    OFFLINE        = 'offline'


class ActivityType(enum.IntEnum):
    PLAYING   = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING  = 3


class Activity:
    """Represents the activity of a User or a Bot

    Activities show what a User or Bot is doing right now.
    Side note: This Model doesn't have Rich Presence implemented

    Attributes
    ----------
    name : str
        The activity's name.
    type : int
        The type of the activity
    url : str, optional
        The URL of the stream, only when stream type is 1.
    """

    __slots__ = ('name', 'type', 'url')

    def __init__(self, data, activity_type=ActivityType.PLAYING):
        self.name = data['name']
        self.type = activity_type.value
        self.url = data.get('url')

    def to_json(self):
        if self.type is 1 and self.url is None:
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
        self.user = User(data['user'], http)
        self.roles = data['roles']
        self.guild_id = data['guild_id']
        self.status = data['status']
        self.activities = [Activity(activity, http) for activity in data['activities']]

        self.game = data.get('game')
        if self.game:
            self.game = Activity(self.game)
