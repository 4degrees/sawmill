..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _bark.guide.configuration:

Configuration
=============

Bark comes with some default *configurators* that are simple helper functions
for configuring the system. Each one is registered in the
:py:data:`bark.configurators` dictionary and can be called through the
:py:func:`bark.configure` function.

The default configurator is the :py:mod:`~bark.configurator.classic` one which
you would have used in the :ref:`bark.guide.getting_started` guide.

.. note::

    You can find reference for each configurator that comes with Bark in the
    :mod:`bark.configurator` section.

You don't have to use a configurator though (or you might want to create your
own) so let's take a look at manually configuring the system.

First, decide what you want to handle, where it should go and how it should be
formatted. For our purposes, we will configure Bark to:

* Send all logs to :py:attr:`sys.stderr` that have a level greater than
  'warning' or have been tagged with a 'user' key. The format will be just
  the level and message.

* Send all logs to a file displaying all available fields verbosely starting
  with date, level, name, message.

* Send a formatted email for any log with a level of 'error' or higher to our
  support team including the traceback and a *buffer* of recent logs.

Before you start make sure you import all the necessary modules:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 5-12

User Visible Or High Level To Standard Error
--------------------------------------------

First up we need a :py:class:`~bark.handler.stream.Stream` handler to direct
output to :py:attr:`sys.stderr`:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 18

We want to use a simple :py:class:`~bark.formatter.template.Template` formatter
to display each log as a string of level and message:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 19

And attach that as the formatter for the *stderr_handler*:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 20

Now we need to filter all logs that don't meet the level requirement unless
they are tagged with a 'user' key:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 22,23

And attach as the filterer for the *stderr_handler*:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 24

Next we just need to register this handler under a sensible name like
*stderr*:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 26

All To File
-----------

Logging everything to a file means we need another
:py:class:`~bark.handler.stream.Stream` handler, but pointing at a file this
time:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 29-31

We don't need any filterer as all logs should go to the file, but we do want a
specific formatter to try and capture as much information as the logs can
provide:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 33-36

.. note::

    The '*' is special and means capture all other fields present ordered
    alphabetically by key.

And register that one as well:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 38

Errors To Email
---------------

Finally create an email handler that will send any errors to a predefined
email address, including a buffer of recent messages. First setup the email
handler with the default template:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 41-45

Next, we need a buffer so that errors will have context. This buffer will wrap
the email handler and only pass on messages when the set trigger is activated:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 47-59

And register the buffer handler as the email handler:

.. literalinclude:: /resource/configurator.py
    :language: python
    :lines: 61

.. seealso::

    See :ref:`Configurator Example <bark.guide.example.configurator>` for the
    full code used in this tutorial.
