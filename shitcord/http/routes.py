# -*- coding: utf-8 -*-

from enum import Enum


class Methods(Enum):
    GET    = 'GET'  # noqa
    POST   = 'POST'  # noqa
    PUT    = 'PUT'  # noqa
    PATCH  = 'PATCH'  # noqa
    DELETE = 'DELETE'  # noqa


class Endpoints:
    # Guild
    GUILD                             = '/guilds'  # noqa
    CREATE_GUILD                      = (Methods.POST, GUILD)  # noqa
    GET_GUILD                         = (Methods.GET, GUILD + '/{guild}')  # noqa
    MODIFY_GUILD                      = (Methods.PATCH, GUILD + '/{guild}')  # noqa
    DELETE_GUILD                      = (Methods.DELETE, GUILD + '/{guild}')  # noqa
    GET_GUILD_CHANNELS                = (Methods.GET, GUILD + '/{guild}/channels')  # noqa
    CREATE_GUILD_CHANNEL              = (Methods.POST, GUILD + '/{guild}/channels')  # noqa
    MODIFY_GUILD_CHANNEL_POSITIONS    = (Methods.PATCH, '/{guild}/channels')  # noqa
    GET_GUILD_MEMBER                  = (Methods.GET, GUILD + '/{guild}/members/{member}')  # noqa
    LIST_GUILD_MEMBERS                = (Methods.GET, GUILD + '/{guild}/members')  # noqa
    ADD_GUILD_MEMBER                  = (Methods.PUT, GUILD + '/{guild}/members/{member}')  # noqa
    MODIFY_GUILD_MEMBER               = (Methods.PATCH, GUILD + '/{guild}/members/{member}')  # noqa
    MODIFY_CURRENT_USER_NICK          = (Methods.PATCH, GUILD + '/{guild}/members/@me/nick')  # noqa
    ADD_GUILD_MEMBER_ROLE             = (Methods.PUT, GUILD + '/{guild}/members/{member}/roles/{role}')  # noqa
    REMOVE_GUILD_MEMBER_ROLE          = (Methods.DELETE, GUILD + '/{guild}/members/{member}/roles/{role}')  # noqa
    REMOVE_GUILD_MEMBER               = (Methods.DELETE, GUILD + '/{guild}/members/{member}')  # noqa
    GET_GUILD_BANS                    = (Methods.GET, GUILD + '/{guild}/bans')  # noqa
    GET_GUILD_BAN                     = (Methods.GET, GUILD + '/{guild}/bans/{user}')  # noqa
    CREATE_GUILD_BAN                  = (Methods.PUT, GUILD + '/{guild}/bans/{user}')  # noqa
    REMOVE_GUILD_BAN                  = (Methods.DELETE, GUILD + '/{guild}/bans/{user}')  # noqa
    GET_GUILD_ROLES                   = (Methods.GET, GUILD + '/{guild}/roles')  # noqa
    CREATE_GUILD_ROLE                 = (Methods.POST, GUILD + '/{guild}/roles')  # noqa
    MODIFY_GUILD_ROLE_POSITIONS       = (Methods.PATCH, GUILD + '/{guild}/roles')  # noqa
    MODIFY_GUILD_ROLE                 = (Methods.PATCH, GUILD + '/{guild}/roles/{role}')  # noqa
    DELETE_GUILD_ROLE                 = (Methods.DELETE, GUILD + '/{guild}/roles/{role}')  # noqa
    GET_GUILD_PRUNE_COUNT             = (Methods.GET, GUILD + '/{guild}/prune')  # noqa
    BEGIN_GUILD_PRUNE                 = (Methods.POST, GUILD + '/{guild}/prune')  # noqa
    GET_GUILD_VOICE_REGIONS           = (Methods.GET, GUILD + '/{guild}/regions')  # noqa
    GET_GUILD_INVITES                 = (Methods.GET, GUILD + '/{guild}/invites')  # noqa
    GET_GUILD_INTEGRATIONS            = (Methods.GET, GUILD + '/{guild}/integrations')  # noqa
    CREATE_GUILD_INTEGRATION          = (Methods.POST, GUILD + '/{guild}/integrations')  # noqa
    MODIFY_GUILD_INTEGRATION          = (Methods.PATCH, GUILD + '/{guild}/integrations/{integration}')  # noqa
    DELETE_GUILD_INTEGRATION          = (Methods.DELETE, GUILD + '/{guild}/integrations/{integration}')  # noqa
    SYNC_GUILD_INTEGRATION            = (Methods.POST, GUILD + '/{guild}/integrations/{integration}/sync')  # noqa
    GET_GUILD_EMBED                   = (Methods.GET, GUILD + '/{guild}/embed')  # noqa
    MODIFY_GUILD_EMBED                = (Methods.PATCH, GUILD + '/{guild}/embed')  # noqa
    GET_GUILD_VANITY_URL              = (Methods.GET, GUILD + '/{guild}/vanity-url')  # noqa

    # Channel
    CHANNEL                           = '/channels/{channel}'  # noqa
    GET_CHANNEL                       = (Methods.GET, CHANNEL)  # noqa
    MODIFY_CHANNEL                    = (Methods.PATCH, CHANNEL)  # noqa
    DELETE_CHANNEL                    = (Methods.DELETE, CHANNEL)  # noqa
    GET_CHANNEL_MESSAGES              = (Methods.GET, CHANNEL + '/messages')  # noqa
    GET_CHANNEL_MESSAGE               = (Methods.GET, CHANNEL + '/messages/{message}')  # noqa
    CREATE_MESSAGE                    = (Methods.POST, CHANNEL + '/messages')  # noqa
    CREATE_REACTION                   = (Methods.PUT, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')  # noqa
    DELETE_OWN_REACTION               = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')  # noqa
    DELETE_USER_REACTION              = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/{user}')  # noqa
    GET_REACTIONS                     = (Methods.GET, CHANNEL + '/messages/{message}/reactions/{emoji}')  # noqa
    DELETE_ALL_REACTIONS              = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions')  # noqa
    EDIT_MESSAGE                      = (Methods.PATCH, CHANNEL + '/messages/{message}')  # noqa
    DELETE_MESSAGE                    = (Methods.DELETE, CHANNEL + '/messages/{message}')  # noqa
    BULK_DELETE_MESSAGES              = (Methods.POST, CHANNEL + '/messages/bulk-delete')  # noqa
    EDIT_CHANNEL_PERMISSIONS          = (Methods.PUT, CHANNEL + '/permissions/{permission}')  # noqa
    GET_CHANNEL_INVITES               = (Methods.GET, CHANNEL + '/invites')  # noqa
    CREATE_CHANNEL_INVITE             = (Methods.POST, CHANNEL + '/invites')  # noqa
    DELETE_CHANNEL_PERMISSION         = (Methods.DELETE, CHANNEL + '/permissions/{permission}')  # noqa
    TRIGGER_TYPING_INDICATOR          = (Methods.POST, CHANNEL + '/typing')  # noqa
    GET_PINNED_MESSAGES               = (Methods.GET, CHANNEL + '/pins')  # noqa
    ADD_PINNED_CHANNEL_MESSAGE        = (Methods.PUT, CHANNEL + '/pins/{message}')  # noqa
    DELETE_PINNED_CHANNEL_MESSAGE     = (Methods.DELETE, CHANNEL + '/pins/{message}')  # noqa
    GROUP_DM_ADD_RECIPIENT            = (Methods.PUT, CHANNEL + '/recipients/{user}')  # noqa
    GROUP_DM_REMOVE_RECIPIENT         = (Methods.DELETE, CHANNEL + '/recipients/{user}')  # noqa

    # Audit Log
    GET_GUILD_AUDIT_LOG               = (Methods.GET, GUILD + '/{guild}/audit-logs')  # noqa

    # Emoji
    EMOJI                             = '/emojis'  # noqa
    LIST_GUILD_EMOJIS                 = (Methods.GET, GUILD + '/{guild}' + EMOJI)  # noqa
    GET_GUILD_EMOJI                   = (Methods.GET, GUILD + '/{guild}' + EMOJI + '/{emoji}')  # noqa
    CREATE_GUILD_EMOJI                = (Methods.POST, GUILD + '/{guild}' + EMOJI)  # noqa
    MODIFY_GUILD_EMOJI                = (Methods.PATCH, GUILD + '/{guild}' + EMOJI + '/{emoji}')  # noqa
    DELETE_GUILD_EMOJI                = (Methods.DELETE, GUILD + '/{guild}' + EMOJI + '/{emoji}')  # noqa

    # Invite
    INVITE                            = '/invites/{invite}'  # noqa
    GET_INVITE                        = (Methods.GET, INVITE)  # noqa
    DELETE_INVITE                     = (Methods.DELETE, INVITE)  # noqa

    # User
    USER                              = '/users'  # noqa
    GET_CURRENT_USER                  = (Methods.GET, USER + '/@me')  # noqa
    GET_USER                          = (Methods.GET, USER + '/{user}')  # noqa
    MODIFY_CURRENT_USER               = (Methods.PATCH, USER + '/@me')  # noqa
    GET_CURRENT_USER_GUILDS           = (Methods.GET, USER + '/@me/guilds')  # noqa
    LEAVE_GUILD                       = (Methods.DELETE, USER + '/@me/guilds/{guild}')  # noqa
    GET_USER_DMS                      = (Methods.GET, USER + '/@me/channels')  # noqa
    CREATE_DM                         = (Methods.POST, USER + '/@me/channels')  # noqa
    CREATE_GROUP_DM                   = (Methods.POST, USER + '/@me/channels')  # noqa
    GET_USER_CONNECTIONS              = (Methods.GET, USER + '/@me/connections')  # noqa

    # Voice
    VOICE                             = '/voice/regions'  # noqa
    LIST_VOICE_REGIONS                = (Methods.GET, VOICE)  # noqa

    # Webhook
    WEBHOOK                           = '/webhooks'  # noqa
    CREATE_WEBHOOK                    = (Methods.POST, CHANNEL + WEBHOOK)  # noqa
    GET_CHANNEL_WEBHOOKS              = (Methods.GET, CHANNEL + WEBHOOK)  # noqa
    GET_GUILD_WEBHOOKS                = (Methods.GET, GUILD + '/{guild}' + WEBHOOK)  # noqa
    GET_WEBHOOK                       = (Methods.GET, WEBHOOK + '/{webhook}')  # noqa
    GET_WEBHOOK_WITH_TOKEN            = (Methods.GET, WEBHOOK + '/{webhook}/{token}')  # noqa
    MODIFY_WEBHOOK                    = (Methods.PATCH, WEBHOOK + '/{webhook}')  # noqa
    MODIFY_WEBHOOK_WITH_TOKEN         = (Methods.PATCH, WEBHOOK + '/{webhook}/{token}')  # noqa
    DELETE_WEBHOOK                    = (Methods.DELETE, WEBHOOK + '/{webhook}')  # noqa
    DELETE_WEBHOOK_WITH_TOKEN         = (Methods.DELETE, WEBHOOK + '/{webhook}/{token}')  # noqa
    EXECUTE_WEBHOOK                   = (Methods.POST, WEBHOOK + '/{webhook}/{token}')  # noqa
    EXECUTE_SLACK_COMPATIBLE_WEBHOOK  = (Methods.POST, WEBHOOK + '/{webhook}/{token}/slack')  # noqa
    EXECUTE_GITHUB_COMPATIBLE_WEBHOOK = (Methods.POST, WEBHOOK + '/{webhook}/{token}/github')  # noqa

    # OAuth2
    OAUTH                             = '/oauth2/applications'  # noqa
    GET_CURRENT_APPLICATION_INFO      = (Methods.GET, OAUTH + '/@me')  # noqa

    # Gateway
    GATEWAY                           = '/gateway'  # noqa
    GET_GATEWAY                       = (Methods.GET, GATEWAY)  # noqa
    GET_GATEWAY_BOT                   = (Methods.GET, GATEWAY + '/bot')  # noqa
