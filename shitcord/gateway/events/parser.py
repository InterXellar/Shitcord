# -*- coding: utf-8 -*-

from .event_models import *
from .parsers import ModelParser, NullParser
from ... import models

event_parsers = dict(
    # Gateway stuff
    hello=NullParser(),
    ready=NullParser(),
    resumed=NullParser(),
    invalid_session=NullParser(),

    # Channel stuff
    channel_create=ModelParser(models._channel_from_payload),
    channel_update=ModelParser(models._channel_from_payload),
    channel_delete=ModelParser(models._channel_from_payload),
    channel_pins_update=NullParser(),

    # Guild stuff
    guild_create=ModelParser(models.Guild),
    guild_update=ModelParser(models.Guild),
    guild_delete=ModelParser(models.Guild),
    guild_ban_add=NullParser(),
    guild_ban_remove=NullParser(),
    guild_emojis_update=NullParser(),
    guild_integrations_update=NullParser(),
    guild_member_add=ModelParser(models.Member),
    guild_member_remove=NullParser(),
    guild_member_update=NullParser(),
    guild_members_chunk=NullParser(),
    guild_role_create=NullParser(),
    guild_role_update=NullParser(),
    guild_role_delete=NullParser(),

    # Message stuff
    message_create=ModelParser(models.Message),
    message_update=ModelParser(models.Message),
    message_delete=ModelParser(MessageDelete),
    message_delete_bulk=ModelParser(MessageDeleteBulk),
    message_reaction_add=ModelParser(MessageReaction),
    message_reaction_remove=ModelParser(MessageReaction),
    message_reaction_remove_all=ModelParser(MessageReactionRemoveAll),

    # Presence stuff
    presence_update=ModelParser(PresenceUpdate),

    # Typing stuff
    typing_start=ModelParser(TypingStart),

    # Voice stuff
    voice_state_update=ModelParser(models.VoiceState),
    voice_server_update=ModelParser(VoiceServerUpdate),

    # Webhook stuff
    webhooks_update=ModelParser(WebhooksUpdate),
)

default_aliases = dict(
    message='message_create',
    member_add='guild_member_add',
    member_remove='guild_member_remove',
    kick='guild_member_remove',
    ban='guild_ban_add',
    unban='guild_ban_remove',
    typing='typing_start'
)


def _resolve_alias(event):
    if event in default_aliases:
        return default_aliases[event]

    return event


def parse_event(event, data, http):
    real_event = _resolve_alias(event)
    if real_event not in event_parsers:
        return

    return real_event, event_parsers[real_event].parse(data, http)
