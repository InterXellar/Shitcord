# -*- coding: utf-8 -*-

import logging
from contextlib import contextmanager

import contextvars

from .http import HTTP
from .routes import Endpoints
from ..models import Connection, DMChannel, GroupDMChannel, Invite, User, Webhook

logger = logging.getLogger(__name__)


def optional(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


class API:
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

    # --- Invite -------------------------------------------------------------------- #

    async def get_invite(self, invite_code, with_counts=None):
        invite = await self.make_request(Endpoints.GET_INVITE, dict(invite=invite_code), params=optional(with_counts=with_counts))
        return Invite(invite, self.get_api())

    async def delete_invite(self, invite_code, reason=None):
        invite = await self.make_request(Endpoints.DELETE_INVITE, dict(invite=invite_code), reason=reason)
        return Invite(invite, self.get_api())

    # --- User ---------------------------------------------------------------------- #

    async def get_current_user(self):
        user = await self.make_request(Endpoints.GET_CURRENT_USER)
        return User(user, self.get_api())

    async def get_user(self, user_id):
        user = await self.make_request(Endpoints.GET_USER, dict(user=user_id))
        return User(user, self.get_api())

    async def modify_current_user(self, username=None, avatar=None):
        user = await self.make_request(Endpoints.MODIFY_CURRENT_USER, json=optional(username=username, avatar=avatar))
        return User(user, self.get_api())

    async def get_current_user_guilds(self, before=None, after=None, limit=None):
        # guilds = await self.make_request(Endpoints.GET_CURRENT_USER_GUILDS, params=optional(before=before, after=after, limit=limit))
        # TODO: Implement the PartialGuild model!!!!!1111!!!
        # return [PartialGuild(guild, self.get_api()) for guild in guilds]
        pass

    async def leave_guild(self, guild_id):
        return await self.make_request(Endpoints.LEAVE_GUILD, dict(guild=guild_id))

    async def get_user_dms(self):
        channels = await self.make_request(Endpoints.GET_USER_DMS)
        return [DMChannel(channel, self.get_api()) for channel in channels]

    async def create_dm(self, user_id):
        channel = await self.make_request(Endpoints.CREATE_DM, json={'recipient_id': user_id})
        return DMChannel(channel, self.get_api())

    async def create_group_dm(self, access_tokens=None, nicks=None):
        channel = await self.make_request(Endpoints.CREATE_GROUP_DM, json=optional(access_tokens=access_tokens, nicks=nicks))
        return GroupDMChannel(channel, self.get_api())

    async def get_user_connections(self):
        connections = await self.make_request(Endpoints.GET_USER_CONNECTIONS)
        return [Connection(connection) for connection in connections]

    # --- Voice --------------------------------------------------------------------- #

    async def list_voice_regions(self):
        return await self.make_request(Endpoints.LIST_VOICE_REGIONS)

    # --- Webhook ------------------------------------------------------------------- #

    async def create_webhook(self, channel_id, name, avatar=None):
        payload = {
            'name': name,
        }.update(optional(avatar=avatar))

        webhook = await self.make_request(Endpoints.CREATE_WEBHOOK, dict(channel=channel_id), json=payload)
        return Webhook(webhook, self.get_api())

    async def get_channel_webhooks(self, channel_id):
        webhooks = await self.make_request(Endpoints.GET_CHANNEL_WEBHOOKS, dict(channel=channel_id))
        return [Webhook(webhook, self.get_api()) for webhook in webhooks]

    async def get_guild_webhooks(self, guild_id):
        webhooks = await self.make_request(Endpoints.GET_GUILD_WEBHOOKS, dict(guild=guild_id))
        return [Webhook(webhook, self.get_api()) for webhook in webhooks]

    async def get_webhook(self, webhook_id):
        webhook = await self.make_request(Endpoints.GET_WEBHOOK, dict(webhook=webhook_id))
        return Webhook(webhook, self.get_api())

    async def get_webhook_with_token(self, webhook_id, webhook_token):
        webhook = await self.make_request(Endpoints.GET_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token))
        return Webhook(webhook, self.get_api())

    async def modify_webhook(self, webhook_id, name=None, avatar=None, channel_id=None, reason=None):
        webhook = await self.make_request(
            Endpoints.MODIFY_WEBHOOK,
            dict(webhook=webhook_id),
            json=optional(name=name, avatar=avatar, channel_id=channel_id),
            reason=reason
        )
        return Webhook(webhook, self.get_api())

    async def modify_webhook_with_token(self, webhook_id, webhook_token, name=None, avatar=None, reason=None):
        webhook = await self.make_request(
            Endpoints.MODIFY_WEBHOOK_WITH_TOKEN,
            dict(webhook=webhook_id, token=webhook_token),
            json=optional(name=name, avatar=avatar),
            reason=reason
        )
        return Webhook(webhook, self.get_api())

    async def delete_webhook(self, webhook_id, reason=None):
        return await self.make_request(Endpoints.DELETE_WEBHOOK, dict(webhook=webhook_id), reason=reason)

    async def delete_webhook_with_token(self, webhook_id, webhook_token, reason=None):
        return await self.make_request(Endpoints.DELETE_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token), reason=reason)

    async def execute_webhook(self, webhook_id, webhook_token, data, wait=False):
        # message = await self.make_request(
        #     Endpoints.EXECUTE_WEBHOOK,
        #     dict(webhook=webhook_id, token=webhook_token),
        #     json=optional(**data),
        #     params={'wait': wait}
        # )

        # if wait:
        #     # TODO: IMPLEMENT THE FUCKING MESSAGE MODEL!!!111!!!!
        #     # return Message(message, self.get_api())
        #     pass
        pass

    # --- OAuth2 -------------------------------------------------------------------- #

    async def get_current_application_info(self):
        return await self.make_request(Endpoints.GET_CURRENT_APPLICATION_INFO)

    # --- Gateway ------------------------------------------------------------------- #

    async def get_gateway(self):
        return await self.make_request(Endpoints.GET_GATEWAY)

    async def get_gateway_bot(self):
        response = await self.make_request(Endpoints.GET_GATEWAY_BOT)

        return response['url'], response['shards'], response['session_start_limit']
