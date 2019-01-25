.. currentmodule:: shitcord

.. _intro:

Introduction
============

Thanks for your interest in this project! Shitcord is a library that aids with creating applications
that utilize the Discord API. Let's have a look at a small introduction to the library.

Prerequisites
-------------

Shitcord works with Python 3.5.2+. Support for lower versions isn't supported due to a dependency
(``asks``) that doesn't support any Python versions lower than Python 3.5.2.

.. _dependencies:

Shitcord's dependencies
-----------------------

At this point, we want to say thanks to the developers of a few awesome libraries that Shitcord
requires to work.

trio
****

Once upon a time, people thought that asyncio is total bullshit. Then they attempted to create a
better asynchronous I/O framework without all the mistakes asyncio made. And trio is the result.
It's a great concurrency framework and is the core of Shitcord.
Definitely check it out `here <https://github.com/python-trio/trio>`_.

asks
****

asks is an awesome but messy HTTP library that was built to be similar to the requests library.
It is used for performing HTTP requests to the Discord REST API and parsing the responses.
Check it out `here <https://github.com/theelous3/asks>`_.

trio-websocket
**************

trio-websocket is a library that implements the WebSocket protocol handling I/O using trio.
It is used for connecting and interacting with the Discord Gateway.
it is a great library striving for safety, correctness and ergonomics and is based on wsproto.
Check out the project `here <https://github.com/HyperionGray/trio-websocket>`_.

.. _installation:

Installation
------------

As this library is still WIP, it isn't published on PyPI yet.
So you can install the most recent version from GitHub: ::

    # Windows:
    py -3 -m pip install -U git+https://github.com/itsVale/Shitcord@async#egg=shitcord

    # Linux & macOS:
    python3 -m pip install -U git+https://github.com/itsVale/Shitcord@async#egg=shitcord

This is the preferred way of installing Shitcord. If you want to use other installation methods,
please don't expect support for the installation of this library.

.. warning:: If you're using Python 3.6+ on macOS, please make sure to
    run the ``Install certificates.command`` located in the Python folder
    inside your ``Applications`` directory. This is important, because
    Python 3.6+ comes with its own bundled version of OpenSSL because
    Apple only provides deprecated binaries. Without this step, you're most
    likely getting an `SSLError` whenever you try to run your bot.

Basic Usage
-----------

As the following documentation is incomplete and the library due to WIP may be changed dramatically
at any time, we don't provide a usage example yet. Also, it is not very user-friendly yet, so better
stay patient unless you are willing to read the source code.

.. literalinclude:: examples/beginners_example.py
    :linenos:

Support
-------

If you need help with this library or have a question about how its usage, you could either create an
issue on GitHub or, and this is the most preferred way, you join the official `support server <https://discord.gg/HbKGrVT>`_.