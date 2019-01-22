# -*- coding: utf-8 -*-

from enum import Enum
from typing import List, Union

from .errors import InvalidPermission

PossiblePermissionTypes = Union[Enum, str, int]
ValidPermissionTypes = Union[List[PossiblePermissionTypes], PossiblePermissionTypes]


class PermissionTypes(Enum):
    CREATE_INSTANT_INVITE = 0x00000001  # noqa
    KICK_MEMBERS          = 0x00000002  # noqa
    BAN_MEMBERS           = 0x00000004  # noqa
    ADMINISTRATOR         = 0x00000008  # noqa
    MANAGE_CHANNELS       = 0x00000010  # noqa
    MANAGE_GUILD          = 0x00000020  # noqa
    ADD_REACTIONS         = 0x00000040  # noqa
    VIEW_AUDIT_LOG        = 0x00000080  # noqa
    VIEW_CHANNEL          = 0x00000400  # noqa
    SEND_MESSAGES         = 0x00000800  # noqa
    SEND_TTS_MESSAGES     = 0x00001000  # noqa
    MANAGE_MESSAGES       = 0x00002000  # noqa
    EMBED_LINKS           = 0x00004000  # noqa
    ATTACH_FILES          = 0x00008000  # noqa
    READ_MESSAGE_HISTORY  = 0x00010000  # noqa
    MENTION_EVERYONE      = 0x00020000  # noqa
    USE_EXTERNAL_EMOJIS   = 0x00040000  # noqa
    CONNECT               = 0x00100000  # noqa
    SPEAK                 = 0x00200000  # noqa
    MUTE_MEMBERS          = 0x00400000  # noqa
    DEAFEN_MEMBERS        = 0x00800000  # noqa
    MOVE_MEMBERS          = 0x01000000  # noqa
    USE_VAD               = 0x02000000  # noqa
    PRIORITY_SPEAKER      = 0x00000100  # noqa
    CHANGE_NICKNAME       = 0x04000000  # noqa
    MANAGE_NICKNAMES      = 0x08000000  # noqa
    MANAGE_ROLES          = 0x10000000  # noqa
    MANAGE_WEBHOOKS       = 0x20000000  # noqa
    MANAGE_EMOJI          = 0x40000000  # noqa


def match_permission_type(value: str) -> int:
    for permission in PermissionTypes:
        if permission.name == value.upper().replace(' ', '_'):
            return permission.value

    else:
        raise InvalidPermission('Unable to find permission: "{}"'.format(value))


def to_bitset(value: PossiblePermissionTypes) -> int:
    if isinstance(value, Enum):
        return value.value

    elif isinstance(value, str):
        return match_permission_type(value)

    elif isinstance(value, int):
        return value

    raise InvalidPermission('Invalid type for permission bitset. Must be shitcord.utils.PermissionTypes, str or int.')


class Permissions:
    """A class that wraps around a permissions value from the Discord API.

    Permissions are used to limit or grant certain abilities on a Guild to Members or Roles.

    Attributes
    ----------
    value : int, optional
        The permissions value.
    """

    __slots__ = ('value', )

    def __init__(self, perms: PossiblePermissionTypes = 0):
        self.value = to_bitset(perms)

    def __repr__(self):
        return '<shitcord.Permissions value={}>'.format(self.value)

    def __contains__(self, item: PossiblePermissionTypes):
        if self.value & to_bitset(item) == to_bitset(item):
            return True
        return False

    def __eq__(self, other):
        return isinstance(other, Permissions) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def __int__(self):
        return self.value

    def __iter__(self):
        for permission in PermissionTypes:
            yield (permission.name, permission.value in self)

    def has(self, *permissions: ValidPermissionTypes) -> bool:
        """Indicates whether some certain permissions are included in the permission value for this object."""

        for permission in permissions:
            if permission not in self:
                break

        else:
            return True

        return False

    def add(self, *permissions: ValidPermissionTypes):
        """Adds a set of permissions to the current permission value of this object."""

        for permission in permissions:
            self.value |= to_bitset(permission)

        return self

    def sub(self, *permissions: ValidPermissionTypes):
        """Removes a set of permissions from the current permission value of this object."""

        for permission in permissions:
            self.value &= ~to_bitset(permission)

        return self

    __iadd__ = add
    __isub__ = sub

    def handle_overwrite(self, allowed_permission, denied_permission):
        # You basically have an original bit array.
        # Then you have another one that is forbidden and one that is allowed.
        # The original bit array should be modified that the denied bit array is set to 0.
        # Then you take this value and look at those that are allowed and set these to 1.
        # To remove the denied perm, you use base & ~denied_permission.
        # Then to set the allowed permissions, you use base | allowed.
        self.value = (self.value & ~denied_permission) | allowed_permission

    # TODO: Add more classmethods for creating objects with a set of specific permissions.
    # TODO: Add properties for indicating whether a user has a specific permission or not.

    @classmethod
    def text(cls):
        """A factory method that returns a new :class:`Permissions` instance with all text-based permissions granted."""

        return cls(523328)

    @classmethod
    def voice(cls):
        """A factory method that returns a new :class:`Permissions` instance with all voice-based permissions granted."""

        return cls(66060544)
