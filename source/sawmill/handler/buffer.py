# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import collections

from .base import Handler


class Buffer(Handler):
    '''Buffer log records and distribute to another handler on trigger.

    Any log record handled by this handler will first be filtered and formatted
    by this handler before being added to the buffer.

    The wrapped handler will still have opportunity to further filter and
    format the log records as required.

    .. note::

        The data returned by any registered formatter on this handler will be
        passed directly to the wrapped handler's handle method. Therefore, it
        must be a valid :py:class:`~sawmill.log.Log` record.

    '''

    def __init__(self, handler, trigger, limit=50, *args, **kw):
        '''Initialise handler with wrapped *handler* and *trigger*.

        *trigger* should be a callable that accepts the new data being handled
        and the buffer contents (including the new data). It should return True
        if the wrapped *handler* should be called with the buffer else False.

        *limit* will set the maximimum size of the buffer. When the buffer size
        exceeds the limit and new logs are added, logs will be removed from
        the opposite end

        .. note::

            By default the buffer is cleared after each successful trigger.

        '''
        self.buffer = collections.deque(maxlen=limit)
        self.handler = handler
        self.trigger = trigger
        super(Buffer, self).__init__(*args, **kw)

    def output(self, data):
        '''Output formatted *data*.

        As *data* is eventually passed directly to other handlers' handle
        methods, it should be a list of valid :py:class:`~sawmill.log.Log`
        records.

        '''
        self.buffer.extend(data)
        if self.trigger(data, self.buffer):
            self.handler.handle(*self.buffer)
            self.reset()

    def reset(self):
        '''Reset buffer.'''
        self.buffer.clear()

