# -*- coding: utf-8 -*-

from enum import IntEnum
from itertools import starmap


class HTTPCodes(IntEnum):
    INVALID_TOKEN             = 0    # noqa
    BAD_REQUEST               = 400  # noqa
    UNAUTHORIZED              = 401  # noqa
    FORBIDDEN                 = 403  # noqa
    NOT_FOUND                 = 404  # noqa
    METHOD_NOT_ALLOWED        = 405  # noqa
    INTERNAL_SERVER_ERROR     = 500  # noqa
    NOT_IMPLEMENTED           = 501  # noqa
    GATEWAY_UNAVAILABLE       = 502  # noqa
    SERVICE_UNAVAILABLE       = 503  # noqa
    GATEWAY_TIMEOUT           = 504  # noqa
    API_VERSION_NOT_SUPPORTED = 505  # noqa
    NOT_EXTENDED              = 510  # noqa


class JSONCodes(IntEnum):
    UNKNOWN_ACCOUNT                            = 10001  # noqa
    UNKNOWN_APPLICATION                        = 10002  # noqa
    UNKNOWN_CHANNEL                            = 10003  # noqa
    UNKNOWN_GUILD                              = 10004  # noqa
    UNKNOWN_INTEGRATION                        = 10005  # noqa
    UNKNOWN_INVITE                             = 10006  # noqa
    UNKNOWN_MEMBER                             = 10007  # noqa
    UNKNOWN_MESSAGE                            = 10008  # noqa
    UNKNOWN_OVERWRITE                          = 10009  # noqa
    UNKNOWN_PROVIDER                           = 10010  # noqa
    UNKNOWN_ROLE                               = 10011  # noqa
    UNKNOWN_TOKEN                              = 10012  # noqa
    UNKNOWN_USER                               = 10013  # noqa
    UNKNOWN_EMOJI                              = 10014  # noqa
    UNKNOWN_WEBHOOK                            = 10015  # noqa
    BOTS_CANNOT_USE_THIS_ENDPOINT              = 20001  # noqa
    ONLY_BOTS_CAN_USE_THIS_ENDPOINT            = 20002  # noqa
    MAXIMUM_GUILDS_REACHED                     = 30001  # noqa
    MAXIMUM_FRIENDS_REACHED                    = 30002  # noqa
    MAXIMUM_PINS_REACHED                       = 30003  # noqa
    MAXIMUM_GUILD_ROLES_REACHED                = 30005  # noqa
    MAXIMUM_REACTIONS_REACHED                  = 30010  # noqa
    MAXIMUM_GUILD_CHANNELS_REACHED             = 30013  # noqa
    UNAUTHORIZED                               = 40001  # noqa
    MISSING_ACCESS                             = 50001  # noqa
    INVALID_ACCOUNT_TYPE                       = 50002  # noqa
    CANNOT_EXECUTE_ON_DM_CHANNEL               = 50003  # noqa
    WIDGET_DISABLED                            = 50004  # noqa
    CANNOT_EDIT_MESSAGE_BY_ANOTHER_USER        = 50005  # noqa
    CANNOT_SEND_EMPTY_MESSAGE                  = 50006  # noqa
    CANNOT_SEND_MESSAGE_TO_USER                = 50007  # noqa
    CANNOT_SEND_MESSAGE_IN_VOICE               = 50008  # noqa
    CHANNEL_VERIFICATION_TOO_HIGH              = 50009  # noqa
    OAUTH2_APPLICATION_DOES_NOT_HAVE_A_BOT     = 50010  # noqa
    OAUTH2_APPLICATION_LIMIT_REACHED           = 50011  # noqa
    INVALID_OAUTH2_STATE                       = 50012  # noqa
    MISSING_PERMISSIONS                        = 50013  # noqa
    INVALID_AUTH_TOKEN                         = 50014  # noqa
    NOTE_IS_TOO_LONG                           = 50015  # noqa
    TOO_MANY_OR_FEW_MESSAGES_TO_DELETE         = 50016  # noqa
    MESSAGE_CAN_ONLY_PINNED_IN_MESSAGE_CHANNEL = 50019  # noqa
    INVITE_TOKEN_INVALID_OR_TAKEN              = 50020  # noqa
    CANNOT_EXECUTE_ON_SYSTEM_MESSAGE           = 50021  # noqa
    INVALID_OAUTH2_ACCESS_TOKEN                = 50025  # noqa
    MESSAGE_TO_OLD_TO_BULK_DELETE              = 50034  # noqa
    INVALID_FORM_BODY                          = 50035  # noqa
    INVITE_WAS_ACCEPTED_WHERE_BOT_IS_NOT_IN    = 50036  # noqa
    INVALID_API_VERSION                        = 50041  # noqa
    REACTION_BLOCK                             = 90001  # noqa


class ShitRequestFailed(Exception):
    """An error that will be raised when you received a non-success status code or ran out of retries."""

    def __init__(self, response, data, bucket, *, retries=None):
        self.response = response
        self.bucket = bucket

        self.status_code = None
        self.errors = None
        self.message = None

        self.failed = 'Your shit {0.bucket} failed with code {0.status_code.value} (HTTP code {0.response.status_code}): {0.message}'
        if retries:
            self.failed += 'after fucking {} retries!'.format(retries)

        # Try to get any useful data from the data
        if isinstance(data, dict):
            raw_status_code = data.get('code', 0)
            if raw_status_code <= 600:
                self.status_code = HTTPCodes(raw_status_code)
            else:
                self.status_code = JSONCodes(raw_status_code)

            self.errors = data.get('errors', {})
            self.message = data.get('message', '')
        else:
            self.message = data
            self.status_code = 0

        if self.errors:
            error_list = starmap('{}: {}'.format, self.errors.items())
            self.failed += '\nHere\'s a bunch of errors for you. Have fun with that crap:\n' + '\n'.join(error_list)

        super().__init__(self.failed.format(self))
