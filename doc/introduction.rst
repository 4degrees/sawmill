..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _introduction:

************
Introduction
************

Sawmill is an alternative to the standard Python logging library

Its goals are to be simple and consistent in approach as well as making it
easier to customise behaviour even at a low level. However, it does draw
several concepts from the standard library so hopefully it will all appear
vaguely familiar.

Here are some examples of how Sawmill differs:

* No explicit hierarchy of loggers. All handlers have the opportunity to
  handle every message by default. However, using the
  :py:class:`~sawmill.handler.distribute.Distribute` handler you can construct
  your own handler hierarchy if you want.

* Log levels are not treated specially. Instead you can filter based on log
  level by adding a :py:class:`~sawmill.filterer.level.Level` filterer to your
  handlers.

* There is a clearer contract between formatters and handlers. This simplifies
  having a formatter that produces an email with a handler that actually sends
  the mail.

* No passing of format arguments to log calls. Format messages using either
  standard Python string formatting or a dedicated
  :py:class:`~sawmill.formatter.base.Formatter` that acts on the whole log.

* Filterers and formatters are only defined for handlers so it is clearer
  where to use them (though potentially more restrictive).

* The system handles batches of logs by default making it simple to buffer
  logs and generate summary messages.

* Easy to change the root handler (:py:attr:`sawmill.root`).

* Requires Python 2.6 or higher.

* Follows PEP8.
