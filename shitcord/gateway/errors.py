# -*- coding: utf-8 -*-


class GatewayException(Exception):
    """Represents the base exception class for all Gateway-related errors."""


class ConnectingFailed(GatewayException):
    """Will be raised when the client times out on connecting to the Gateway."""


class NoMoreReconnects(GatewayException):
    """Will be raised when the client has exceeded the total amount of allowed reconnects."""


class InvalidEvent(GatewayException):
    """Will be raised when an event without parser was received."""

    def __init__(self, event_name):
        super().__init__('Received event without parser: {}'.format(event_name))

        self.event = event_name
