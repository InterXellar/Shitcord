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

.. autoclass:: shitcord.http.HTTP
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

Permissions
~~~~~~~~~~~

.. autoclass:: Permissions
    :members:

Role
~~~~

.. autoclass:: Role()
    :members:

.. _utils:

User
~~~~

.. autoclass:: User()
    :members:
    :inherited-members:

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

Exceptions
----------

The following exceptions are thrown by Shitcord.

.. autoexception:: shitcord.http.ShitRequestFailed()

.. autoexception:: shitcord.models.ModelError

.. autoexception:: shitcord.models.InvalidPermission

.. autoexception:: shitcord.models.MissingProfile