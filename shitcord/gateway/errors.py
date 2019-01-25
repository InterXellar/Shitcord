# -*- coding: utf-8 -*-


class GatewayException(Exception):
    """Represents the base exception class for all Gateway-related errors."""


class ConnectingFailed(GatewayException):
    """Will be raised when the client times out on connecting to the Gateway."""


class NoMoreReconnects(GatewayException):
    """Will be raised when the client has exceeded the total amount of allowed reconnects."""
