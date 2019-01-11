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

.. _rest_shit

RESTShit
--------

Let me introduce you to `RESTShit`! This is our way of performing requests to the
Discord REST API. Ideally speaking, this is a terminal between **what** should be done
and **how** it should be done.


.. autoclass:: RESTShit()
    :members:

.. autofunction:: rest_shit