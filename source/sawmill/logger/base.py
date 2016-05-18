# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sawmill
from ..log import Log


class Logger(Log):
    '''Helper for emitting logs.

    A logger can be used to preset common information (such as a name) and then
    emit :py:class:`~sawmill.log.Log` records with that information already
    present.

    '''

    def __init__(self, _handler=sawmill.root, **kw):
        '''Initialise logger.

        If you need to override the default handler then pass in a custom
        *_handler*

        '''
        super(Logger, self).__init__(**kw)
        self._handler = _handler

    def prepare(self, *args, **kw):
        '''Prepare and return a log for emission.

        *kw* arguments are automatically mixed in to a
        :py:class:`~sawmill.log.Log` record made by copying this current logger.

        '''
        log = self.clone()
        log.update(**kw)
        return log

    def log(self, *args, **kw):
        '''Emit a :py:class:`~sawmill.log.Log` record.'''
        log = self.prepare(*args, **kw)
        self._handler.handle(log)

