# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Handler


class Distribute(Handler):
    '''Distribute log records to other named handlers.

    Any log record handled by this handler will first be filtered and formatted
    by this handler before being passed to the other registered handlers.

    The other handlers will still have opportunity to further filter and format
    the log record as required.

    The registered handlers are called in no particular order.

    .. note::

        The data returned by any registered formatter on this handler
        will be passed directly to the registered handlers' handle
        methods. Therefore, it must be a valid
        :py:class:`~sawmill.log.Log` record.

    '''

    def __init__(self, handlers=None, *args, **kw):
        '''Initialise handler with mapping of *handlers* to distribute to.'''
        self.handlers = handlers or {}
        super(Distribute, self).__init__(*args, **kw)

    def output(self, data):
        '''Output formatted *data*.

        As *data* is passed directly to other handlers' handle methods, it
        should be a list of valid :py:class:`~sawmill.log.Log` records.

        '''
        for handler in self.handlers.values():
            handler.handle(*data)
