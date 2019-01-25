.. currentmodule:: shitcord

.. _get_started

Get Started
===========

This page provides a short tutorial about the necessary features of this
library and introduces the most important aspects to you. Let's get started!

Let's start with a quick example on how to use this library:

.. literalinclude:: examples/beginners_example.py
    :linenos:

In the following we will introduce some concepts of the library that will be
very useful for you.

.. _blocking

Blocking
--------

Let's say you want to implement some feature that requires a special lib. And this library
doesn't support async/await syntax. This would cause your bot to block.

In asynchronous programming a blocking call is essentially any line that are not `await`ed.
When a line blocks, it stops the entire rest of the bot from functioning, including commands and
even functions that keep the bot alive. Ideally speaking, blocking affects performance and even stability of your bot.
A common example for blocking is the usage of ``time.sleep()`` instead of ``await trio.sleep()``.

But don't worry. I've got something nice for you. It is called `trio.run_sync_in_worker_thread <https://trio.readthedocs.io/en/latest/reference-core.html#trio.run_sync_in_worker_thread>`_!

Let's have a look at an image processing example with PIL to get a closer understanding of this method.

.. literalinclude:: examples/blocking_io.py
    :linenos:

.. _shitcord_sync

shitcord.sync
-------------

.. note:: shitcord.sync is experimental and may cause unexpected issues.

There might be cases where you want to use Shitcord without depending on async/await syntax.
For this case, we've got your back with ``shitcord.sync``.

This module wraps all classes of this library so you can use them entirely without async/await.
All you have to do is quite simple:

.. code-block:: python

    import shitcord.sync as sync

    ...

.. warning::

    It is recommended to not mix up ``import shitcord`` and ``import shitcord.sync as shitcord`` in your bot.
    It is preferred to stick with one of them in your entire bot.

.. _rest_shit_interface

The RESTShit Interface
----------------------

Let me introduce you to `RESTShit`! This is our way of performing requests to the
Discord REST API. Ideally speaking, this is a terminal between **what** should be done
and **how** it should be done.


.. autoclass:: RESTShit()
    :members:

.. autofunction:: rest_shit