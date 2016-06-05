..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _tutorial:

********
Tutorial
********

Using Sawmill is straightforward::

    >>> import sawmill
    >>> from sawmill.log import Log
    >>> sawmill.configure()
    >>> sawmill.root.handle(Log(message='Hello World!'))
    Hello World!

Voila! You asked Sawmill to :py:func:`~sawmill.configure` itself in a classic
fashion and then called the main :py:data:`~sawmill.root.handle` method with a
:py:class:`~sawmill.log.Log` instance. The resulting message appeared on
:py:attr:`sys.stderr`.

.. note::

    :py:func:`sawmill.configure` is a helper function that attempts to
    configure Sawmill in a way that is useful to most applications. However,
    there is no requirement to use this helper or the default configurators
    (see :ref:`configuration`).

Loggers
=======

If you find that you are regularly inputting the same information for each
log instance then you can create a :py:meth:`~sawmill.logger.base.Logger` to
hold common information. Any values you set on the logger will automatically
propagate into the log messages you generate using the
:py:meth:`~sawmill.logger.base.Logger.log` method::

    >>> logger = Logger(name='my.logger')
    >>> logger.log(message='Hi there')
    my.logger:Hi there
    >>> logger['level'] = 'info'
    >>> logger.log(message='Some information')
    my.logger:info:Hi there

Sawmill comes with some different logger implementations to handle common
scenarios, but you can also define your own. Here is the
:py:class:`~sawmill.logger.classic.Classic` logger in action that mimics the
standard Python logger behaviour::

    >>> from sawmill.logger.classic import Classic as Logger
    >>> logger = Logger('my.logger')
    >>> logger.info('An informational message')
    my.logger:info:An informational message
    >>> logger.error('An error message')
    my.logger:error:An error message

Handlers
========

So, how are those messages ending up on :py:attr:`sys.stderr`? This is because
the configure function adds a :py:class:`~sawmill.handler.stream.Stream` handler
configured to output all messages to standard error. It does this by
registering the handler with the :py:data:`~sawmill.root` handler which, by
default, is a :py:class:`~sawmill.handler.distribute.Distribute` handler. The
distribute handler simply relays all the logs it receives to other handlers
registered with it.

Let's add another stream handler to the root handler, but this time outputting
to a :py:class:`~StringIO.StringIO` instance::

    >>> from StringIO import StringIO
    >>> from sawmill.handler.stream import Stream
    >>> my_stream = StringIO()
    >>> my_handler = Stream(stream=my_stream)

All that you have to do to register a handler with a distribute handler is
set it with a unique key on the handlers dictionary of the distribute handler::

    >>> sawmill.root.handlers['my_handler'] = my_handler

Now we can log as normal using our logger from before::

    >>> logger.info('Some more information.')
    my.logger:info:Some more information.

Same as before, but take a look at *my_stream*::

    >>> print my_stream.getvalue()
    {'name': 'my.logger', 'level': 'info', 'message': 'Some more information.'}

The reason it contains just a string representation of the log (dictionary) is
because no formatter has been set on our custom handler.

Formatters
==========

A formatter takes a list of :py:class:`~sawmill.log.Log` instances and returns
a corresponding list of formatted data that a handler can output. Typically the
returned data will be a string, but it is important to note that it does not
have to be. The only condition is that the returned data works with the
handler's output method.

.. note::

    Due to the tight contract between a formatter and handler you cannot use
    every formatter with every handler. Instead check the documentation for
    which ones work well together.

Add a :py:class:`~sawmill.formatter.template.Template` formatter to the handler
created above::

    >>> from sawmill.formatter.template import Template
    >>> my_formatter = Template('{level}:{message}\n')
    >>> my_handler.formatter = my_formatter

Now logging a message will result in the formatter being called for the
handler *my_handler*::

    >>> my_stream.truncate(0)
    >>> logger.info('Yet more information.')
    >>> print my_stream.getvalue()
    info:Yet more information.

Filterers
=========

A filterer controls whether a log should be handled by a particular handler. A
typical usage of a filterer is to restrict a particular handler to only handle
serious errors. Add a :py:class:`~sawmill.filterer.level.Level` filterer to
*my_handler* so that it only handles error messages (or greater)::

    >>> from sawmill.filterer.level import Level
    >>> my_handler.filterer = Level(min='error', max=None)

.. note::

    The level values available and their respective order is set, by default,
    according to the :py:data:`sawmill.levels` array.

Now try logging an info level message::

    >>> my_stream.truncate(0)
    >>> logger.info('I will not appear in the stringio instance.')
    my.logger:info:I will not appear in the stringio instance.

Whilst the log was still handled by the default stream handler (that does not
filter info level messages) it was not handled by *my_handler*::

    >>> print my_stream.getvalue()

If you wanted a group of handlers to have the same filterer you could set them
up under a distribute handler and then set the filterer on that handler. For
example, here is how to limit all the handlers using a filterer on the root
handler::

    >>> sawmill.root.filterer = Level(min='error', max=None)
    >>> logger.info('I will not appear anywhere.')

You can also quickly combine different filterers for more complex effects::

    >>> from sawmill.filterer.pattern import Pattern
    >>> sawmill.root.filterer &= Pattern('my\..*', mode=Pattern.EXCLUDE)

The above would filter any log that had too low a level *or* had a name value
that started with 'my.'.

