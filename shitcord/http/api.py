# -*- coding: utf-8 -*-

import json
import logging
from contextlib import contextmanager

import contextvars

from .http import HTTP
from .routes import Endpoints
from .. import models

logger = logging.getLogger(__name__)


def optional(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


class API:
    """This class represents a wrapper for all endpoints of the Discord REST API."""

    def __init__(self, token):
        self.http = HTTP(token)
        self._storage = contextvars.ContextVar('_storage', default=[])

    @property
    def token(self):
        return self.http._token

    async def make_request(self, route, fmt=None, **kwargs):
        response = await self.http.make_request(route, fmt, **kwargs)
        self._capture_response(response)

        return response

    def _capture_response(self, response):
        self._storage.get().append(response)  # Quite ugly, but does its job.
        logger.debug('Added response "%s" to the cache.', response)

    @contextmanager
    def raw_responses(self):
        """A contextmanager that yields all the captured raw responses from the requests we made.

        PLEASE DO ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING!
        """

        responses = self._storage.get()

        try:
            yield responses
        finally:
            self._storage.set([])

    def get_api(self):
        """Returns a new instance of :class:`API`.

        The main reason for this is to not pass cached response data to the models.
        """

        return API(self.token)

    # --- Channel ------------------------------------------------------------------- #

    async def create_message(self, channel_id, content=None, nonce=None, tts=False, files=None, embed=None):
        payload = {
            'tts': tts,
        }

        if content:
            payload['content'] = content

        if embed:
            payload['embed'] = embed.to_json()

        if nonce:
            payload['nonce'] = nonce

        if files:
            if len(files) == 1:
                attachments = {
                    'file': tuple(files[0]),
                }
            else:
                attachments = {
                    'file{}'.format(index): tuple(file) for index, file in enumerate(files)
                }

            message = await self.make_request(Endpoints.CREATE_MESSAGE, dict(channel=channel_id),
                                              files=attachments, data={'payload_json': json.dumps(payload)})
            return models.Message(message, self.get_api())

        message = await self.make_request(Endpoints.CREATE_MESSAGE, dict(channel=channel_id), json=payload)
        return models.Message(message, self.get_api())

    # --- Audit Log ----------------------------------------------------------------- #

    async def get_guild_audit_log(self, guild_id, user_id=None, action_type=None, before=None, after=None):
        params = optional(**{
            'user_id': user_id,
            'action_type': action_type,
            'before': before,
            'after': after,
        })

        entries = await self.make_request(Endpoints.GET_GUILD_AUDIT_LOG, dict(guild=guild_id), params=params)
        return entries  # TODO: Audit Log model

    # --- Emoji --------------------------------------------------------------------- #

    async def list_guild_emojis(self, guild_id):
        emojis = await self.make_request(Endpoints.LIST_GUILD_EMOJIS, dict(guild=guild_id))
        return [models.Emoji(guild_id, emoji, self.get_api()) for emoji in emojis]

    async def get_guild_emoji(self, guild_id, emoji_id):
        emoji = await self.make_request(Endpoints.GET_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id))
        return models.Emoji(guild_id, emoji, self.get_api())

    async def create_guild_emoji(self, guild_id, name, image, roles, reason=None):
        payload = optional(**{
            'name': name,
            'image': image,
            'roles': roles,
        })

        emoji = await self.make_request(Endpoints.CREATE_GUILD_EMOJI, dict(guild=guild_id), json=payload, reason=reason)
        return models.Emoji(guild_id, emoji, self.get_api())

    async def modify_guild_emoji(self, guild_id, emoji_id, name, roles, reason=None):
        payload = optional(**{
            'name': name,
            'roles': roles,
        })

        emoji = await self.make_request(Endpoints.MODIFY_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id), json=payload, reason=reason)
        return models.Emoji(guild_id, emoji, self.get_api())

    async def delete_guild_emoji(self, guild_id, emoji_id, reason=None):
        return await self.make_request(Endpoints.DELETE_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id), reason=reason)

    # --- Invite -------------------------------------------------------------------- #

    async def get_invite(self, invite_code, with_counts=None):
        invite = await self.make_request(Endpoints.GET_INVITE, dict(invite=invite_code), params=optional(with_counts=with_counts))
        return models.Invite(invite, self.get_api())

    async def delete_invite(self, invite_code, reason=None):
        invite = await self.make_request(Endpoints.DELETE_INVITE, dict(invite=invite_code), reason=reason)
        return models.Invite(invite, self.get_api())

    # --- User ---------------------------------------------------------------------- #

    async def get_current_user(self):
        user = await self.make_request(Endpoints.GET_CURRENT_USER)
        return models.User(user, self.get_api())

    async def get_user(self, user_id):
        user = await self.make_request(Endpoints.GET_USER, dict(user=user_id))
        return models.User(user, self.get_api())

    async def modify_current_user(self, username=None, avatar=None):
        user = await self.make_request(Endpoints.MODIFY_CURRENT_USER, json=optional(username=username, avatar=avatar))
        return models.User(user, self.get_api())

    async def get_current_user_guilds(self, before=None, after=None, limit=None):
        guilds = await self.make_request(Endpoints.GET_CURRENT_USER_GUILDS, params=optional(before=before, after=after, limit=limit))
        return [models.PartialGuild(guild, self.get_api()) for guild in guilds]
        pass

    async def leave_guild(self, guild_id):
        return await self.make_request(Endpoints.LEAVE_GUILD, dict(guild=guild_id))

    async def get_user_dms(self):
        channels = await self.make_request(Endpoints.GET_USER_DMS)
        return [models.DMChannel(channel, self.get_api()) for channel in channels]

    async def create_dm(self, user_id):
        channel = await self.make_request(Endpoints.CREATE_DM, json={'recipient_id': user_id})
        return models.DMChannel(channel, self.get_api())

    async def create_group_dm(self, access_tokens=None, nicks=None):
        channel = await self.make_request(Endpoints.CREATE_GROUP_DM, json=optional(access_tokens=access_tokens, nicks=nicks))
        return models.GroupDMChannel(channel, self.get_api())

    async def get_user_connections(self):
        connections = await self.make_request(Endpoints.GET_USER_CONNECTIONS)
        return [models.Connection(connection) for connection in connections]

    # --- Voice --------------------------------------------------------------------- #

    async def list_voice_regions(self):
        regions = await self.make_request(Endpoints.LIST_VOICE_REGIONS)
        return [models.VoiceRegion(region, self.get_api()) for region in regions]

    # --- Webhook ------------------------------------------------------------------- #

    async def create_webhook(self, channel_id, name, avatar=None):
        payload = {
            'name': name,
        }.update(optional(avatar=avatar))

        webhook = await self.make_request(Endpoints.CREATE_WEBHOOK, dict(channel=channel_id), json=payload)
        return models.Webhook(webhook, self.get_api())

    async def get_channel_webhooks(self, channel_id):
        webhooks = await self.make_request(Endpoints.GET_CHANNEL_WEBHOOKS, dict(channel=channel_id))
        return [models.Webhook(webhook, self.get_api()) for webhook in webhooks]

    async def get_guild_webhooks(self, guild_id):
        webhooks = await self.make_request(Endpoints.GET_GUILD_WEBHOOKS, dict(guild=guild_id))
        return [models.Webhook(webhook, self.get_api()) for webhook in webhooks]

    async def get_webhook(self, webhook_id):
        webhook = await self.make_request(Endpoints.GET_WEBHOOK, dict(webhook=webhook_id))
        return models.Webhook(webhook, self.get_api())

    async def get_webhook_with_token(self, webhook_id, webhook_token):
        webhook = await self.make_request(Endpoints.GET_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token))
        return models.Webhook(webhook, self.get_api())

    async def modify_webhook(self, webhook_id, name=None, avatar=None, channel_id=None, reason=None):
        webhook = await self.make_request(
            Endpoints.MODIFY_WEBHOOK,
            dict(webhook=webhook_id),
            json=optional(name=name, avatar=avatar, channel_id=channel_id),
            reason=reason
        )
        return models.Webhook(webhook, self.get_api())

    async def modify_webhook_with_token(self, webhook_id, webhook_token, name=None, avatar=None, reason=None):
        webhook = await self.make_request(
            Endpoints.MODIFY_WEBHOOK_WITH_TOKEN,
            dict(webhook=webhook_id, token=webhook_token),
            json=optional(name=name, avatar=avatar),
            reason=reason
        )
        return models.Webhook(webhook, self.get_api())

    async def delete_webhook(self, webhook_id, reason=None):
        return await self.make_request(Endpoints.DELETE_WEBHOOK, dict(webhook=webhook_id), reason=reason)

    async def delete_webhook_with_token(self, webhook_id, webhook_token, reason=None):
        return await self.make_request(Endpoints.DELETE_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token), reason=reason)

    async def execute_webhook(self, webhook_id, webhook_token, data, wait=False):
        message = await self.make_request(
            Endpoints.EXECUTE_WEBHOOK,
            dict(webhook=webhook_id, token=webhook_token),
            json=optional(**data),
            params={'wait': wait}
        )

        if wait:
            return models.Message(message, self.get_api())

    # --- OAuth2 -------------------------------------------------------------------- #

    async def get_current_application_info(self):
        return await self.make_request(Endpoints.GET_CURRENT_APPLICATION_INFO)

    # --- Gateway ------------------------------------------------------------------- #

    async def get_gateway(self):
        return await self.make_request(Endpoints.GET_GATEWAY)

    async def get_gateway_bot(self):
        response = await self.make_request(Endpoints.GET_GATEWAY_BOT)

        return response['url'], response['shards'], response['session_start_limit']
