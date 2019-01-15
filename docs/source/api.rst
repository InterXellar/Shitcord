.. currentmodule:: shitcord

API Reference
=============

A full documentation of Shitcord's public API.


.. note::
    Shitcord is still a WIP, so don't expect too much. And also, some of the models
    might be incomplete or just haven't been documented yet. If you find such a case
    in the source code, feel free to create a pull request that adds documentation as
    it is really appreciated.

Version Info
------------

There are two main ways to retrieve the version of Shitcord.

.. data:: version_info

    A named tuple similar to `sys.version_info`_.

    Just like in `sys.version_info`_, the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.

    .. _sys.version_info: https://docs.python.org/3.5/library/sys.html#sys.version_info

.. data:: __version__

    A string representation of the version, e.g. ``'0.0.2-beta0'``.

.. _http:

HTTP
----

Shitcord's HTTP interface that is used for making requests to the REST API, parsing responses
and handling rate limits is documented in the following. There might be cases where you want to
make your own requests instead of using the library's interface. E.g. when new API endpoints were
published that aren't implemented yet. Or cases where you need a raw response. The full HTTP interface
is documented in the following. **However, don't use this if you aren't 100% sure you know what you
are doing! The implemented interface is way more user-friendly and safe to use.**

HTTP
~~~~

.. autoclass:: shitcord.http.HTTP()
    :members:

API
~~~

.. autoclass:: shitcord.http.API()
    :members:

.. _gateway:

Gateway
-------

Discord uses gateways for real-time communication with clients over WebSocket connections.
These will be documented in the following. There are two gateway implementations, one for voice
and the other for regular data like event dispatches.

Shitcord has a full implementation of the Discord Gateway which basically represents the core of
Shitcord's internal logic.

JSONEncoder
~~~~~~~~~~~

.. autoclass:: shitcord.gateway.encoding.JSONEncoder()
    :members:

ETFEncoder
~~~~~~~~~~

.. autoclass:: shitcord.gateway.encoding.ETFEncoder()
    :members:

Gateway
~~~~~~~

.. autoclass:: shitcord.gateway.DiscordWebSocketClient()
    :members:

.. _models:

Models
------

Shitcord's models either are implementations of objects that the Discord API uses,
or helpers that make it easier to interact with some concepts of the API.

Don't create objects of them manually. There is always a way to retrieve them from Shitcord.

Snowflake
~~~~~~~~~

.. autoclass:: Snowflake()
    :members:

PartialChannel
~~~~~~~~~~~~~~

.. autoclass:: PartialChannel()
    :members:
    :inherited-members:

TextChannel
~~~~~~~~~~~

.. autoclass:: TextChannel()
    :members:
    :inherited-members:

DMChannel
~~~~~~~~~

.. autoclass:: DMChannel()
    :members:
    :inherited-members:

VoiceChannel
~~~~~~~~~~~~

.. autoclass:: VoiceChannel()
    :members:
    :inherited-members:

GroupDMChannel
~~~~~~~~~~~~~~

.. autoclass:: GroupDMChannel()
    :members:
    :inherited-members:

CategoryChannel
~~~~~~~~~~~~~~~

.. autoclass:: CategoryChannel()
    :members:
    :inherited-members:

Colour
~~~~~~

.. autoclass:: Colour
    :members:

Embed
~~~~~

.. autoclass:: Embed
    :members:

EmbedThumbnail
**************

.. autoclass:: EmbedThumbnail()
    :members:

EmbedVideo
**********

.. autoclass:: EmbedVideo()
    :members:

EmbedImage
**********

.. autoclass:: EmbedImage()
    :members:

EmbedProvider
*************

.. autoclass:: EmbedProvider()
    :members:

EmbedAuthor
***********

.. autoclass:: EmbedAuthor()
    :members:

EmbedFooter
***********

.. autoclass:: EmbedFooter()
    :members:

EmbedField
**********

.. autoclass::EmbedField()
    :members:

Emoji
~~~~~

.. autoclass:: Emoji()
    :members:
    :inherited-members:

PartialEmoji
~~~~~~~~~~~~

.. autoclass:: PartialEmoji()
    :members:
    :inherited-members:

Activity
~~~~~~~~

.. autoclass:: Activity()
    :members:


ActivityType
~~~~~~~~~~~~

.. autoclass:: ActivityType()
    :inherited-members:


Presence
~~~~~~~~

.. autoclass:: Presence()
    :members:


StatusType
~~~~~~~~~~

.. autoclass:: StatusType()
    :inherited-members:

Invite
~~~~~~

.. autoclass:: Invite()
    :members:

Member
~~~~~~

.. autoclass:: Member()
    :members:
    :inherited-members:

Permissions
~~~~~~~~~~~

.. autoclass:: Permissions
    :members:

Role
~~~~

.. autoclass:: Role()
    :members:

User
~~~~

.. autoclass:: User()
    :members:
    :inherited-members:

Webhook
~~~~~~~

.. autoclass:: Webhook()
    :members:

.. _utils:

Utils
-----

Shitcord uses a couple of utils that are helpers for the API implementation. But some of them
might also be useful for developers using this library as they might want to add functionality
or use existing utils like the event emitter for their own project. These utils are fully documented
in the following section.

EventEmitter
~~~~~~~~~~~~

.. autoclass:: EventEmitter
    :members:

.. _exceptions

Exceptions
----------

The following exceptions are thrown by Shitcord.

ShitRequestFailed
~~~~~~~~~~~~~~~~~

This exception receives its own section because this one is a bit different from the others.
Errors like

.. code-block:: python

    shitcord.http.errors.ShitRequestFailed: Your shit ('GET', '/users/01234') failed with code 10013 (HTTP code 404): Unknown User

are quite special. They look a bit cryptic, but they are easy to understand.

First of all, you need to know that Shitcord only raises one error for any HTTP request failure: ``ShitRequestFailed``.
And because of that, this one contains all necessary information.

They contain a **JSON code** and an **HTTP response code** as well as the **bucket** the request was made to.
The bucket represents the endpoint of the Discord API + the used HTTP method. The JSON and the HTTP code can be looked up `here <https://discordapp.com/developers/docs/topics/opcodes-and-status-codes#http-http-response-codes>`_.

This is the recommended way to look up the codes you received for you to know why the request failed.

.. autoexception:: shitcord.http.ShitRequestFailed()

.. autoexception:: shitcord.gateway.GatewayException

.. autoexception:: shitcord.gateway.ConnectingFailed

.. autoexception:: shitcord.gateway.NoMoreReconnects

.. autoexception:: shitcord.gateway.InvalidEvent
    :members:

.. autoexception:: shitcord.models.ModelError

.. autoexception:: shitcord.models.InvalidPermission

.. autoexception:: shitcord.models.MissingProfile

.. autoexception:: shitcord.models.TooLarge