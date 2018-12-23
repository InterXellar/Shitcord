# -*- coding: utf-8 -*-

from enum import Enum
from typing import List, Union

from .errors import InvalidPermission

PossiblePermissionTypes = Union[Enum, str, int]
ValidPermissionTypes = Union[List[PossiblePermissionTypes], PossiblePermissionTypes]


class PermissionTypes(Enum):
    CREATE_INSTANT_INVITE = 0x00000001
    KICK_MEMBERS          = 0x00000002
    BAN_MEMBERS           = 0x00000004
    ADMINISTRATOR         = 0x00000008
    MANAGE_CHANNELS       = 0x00000010
    MANAGE_GUILD          = 0x00000020
    ADD_REACTIONS         = 0x00000040
    VIEW_AUDIT_LOG        = 0x00000080
    VIEW_CHANNEL          = 0x00000400
    SEND_MESSAGES         = 0x00000800
    SEND_TTS_MESSAGES     = 0x00001000
    MANAGE_MESSAGES       = 0x00002000
    EMBED_LINKS           = 0x00004000
    ATTACH_FILES          = 0x00008000
    READ_MESSAGE_HISTORY  = 0x00010000
    MENTION_EVERYONE      = 0x00020000
    USE_EXTERNAL_EMOJIS   = 0x00040000
    CONNECT               = 0x00100000
    SPEAK                 = 0x00200000
    MUTE_MEMBERS          = 0x00400000
    DEAFEN_MEMBERS        = 0x00800000
    MOVE_MEMBERS          = 0x01000000
    USE_VAD               = 0x02000000
    PRIORITY_SPEAKER      = 0x00000100
    CHANGE_NICKNAME       = 0x04000000
    MANAGE_NICKNAMES      = 0x08000000
    MANAGE_ROLES          = 0x10000000
    MANAGE_WEBHOOKS       = 0x20000000
    MANAGE_EMOJI          = 0x40000000


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
    value = 0

    def __init__(self, perms: PossiblePermissionTypes = 0):
        self.value = max(self.value, to_bitset(perms))

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
        for permission in permissions:
            if permission not in self:
                break

        else:
            return True

        return False

    def add(self, *permissions: ValidPermissionTypes):
        for permission in permissions:
            self.value |= to_bitset(permission)

        return self

    def sub(self, *permissions: ValidPermissionTypes):
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
        return cls(523328)

    @classmethod
    def voice(cls):
        return cls(66060544)
