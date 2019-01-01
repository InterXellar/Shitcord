# -*- coding: utf-8 -*-

import platform


def identify(token, compress=True, large_threshold=50, *, shard=None, presence=None):
    """Returns a payload in JSON format for identifying."""

    # Defining the default values for bots that use this Gateway client if no custom one is provided.
    presence = presence or {'since': None, 'game': None, 'status': 'online', 'afk': False}
    shard = shard or [0, 1]

    return {
        'token': token,
        'properties': {
            '$os': platform.system(),
            '$browser': 'Shitcord',
            '$device': 'Shitcord',
            '$referrer': '',
        },
        'compress': compress,
        'large_threshold': large_threshold,
        'shard': shard,
        'presence': presence
    }


def resume(token, session_id, seq):
    """Returns a payload in JSON format used to reconnect when a client needs to be reconnected."""

    return {
        'token': token,
        'session_id': session_id,
        'seq': seq
    }
