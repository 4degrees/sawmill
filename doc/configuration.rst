..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _configuration:

*************
Configuration
*************

Sawmill comes with some default *configurators* that are simple helper functions
for configuring the system. Each one is registered in the
:py:data:`sawmill.configurators` dictionary and can be called through the
:py:func:`sawmill.configure` function.

The default configurator is the :py:mod:`~sawmill.configurator.classic` one
which you would have used in the :ref:`tutorial`.

.. note::

    You can find reference for each configurator that comes with Sawmill in the
    :mod:`sawmill.configurator` section.

You don't have to use a configurator though (or you might want to create your
own) so let's take a look at manually configuring the system.

First, decide what you want to handle, where it should go and how it should be
formatted. For our purposes, we will configure Sawmill to:

* Send all logs to :py:attr:`sys.stderr` that have a level greater than
  'warning' or have been tagged with a 'user' key. The format will be just
  the level and message.

* Send all logs to a file displaying all available fields verbosely starting
  with date, level, name, message.

* Send a formatted email for any log with a level of 'error' or higher to our
  support team including the traceback and a *buffer* of recent logs.

Before you start make sure you import all the necessary modules:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 5-16

User Visible Or High Level To Standard Error
============================================

First up we need a :py:class:`~sawmill.handler.stream.Stream` handler to direct
output to :py:attr:`sys.stderr`:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 29

We want to use a simple :py:class:`~sawmill.formatter.template.Template`
formatter to display each log as a string of level and message:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 30

And attach that as the formatter for the *stderr_handler*:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 31

Now we need to filter all logs that don't meet the level requirement unless
they are tagged with a 'user' key:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 33,34

And attach as the filterer for the *stderr_handler*:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 35

Next we just need to register this handler under a sensible name like
*stderr*:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 37

All To File
===========

Logging everything to a file means we need another
:py:class:`~sawmill.handler.stream.Stream` handler, but pointing at a file this
time:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 40-45

We don't need any filterer as all logs should go to the file, but we do want a
specific formatter to try and capture as much information as the logs can
provide:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 47-50

.. note::

    The '*' is special and means capture all other fields present ordered
    alphabetically by key.

And register that one as well:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 52

Errors To Email
===============

Finally create an email handler that will send any errors to a predefined
email address, including a buffer of recent messages. First setup the email
handler with the default template:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 55-63

Next, we need a buffer so that errors will have context. This buffer will wrap
the email handler and only pass on messages when the set trigger is activated:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 65-77

And register the buffer handler as the email handler:

.. literalinclude:: /../source/sawmill/configurator/alpha.py
    :language: python
    :lines: 79

.. seealso::

    The :py:mod:`~sawmill.configurator.alpha` configurator used for this
    example.

