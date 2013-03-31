# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import copy

import bark
from .log import Log


class Logger(Log):
    '''Helper for emitting logs.

    A logger can be used to preset common information (such as a name) and then
    emit :py:class:`~bark.log.Log` records with that information already
    present.

    '''

    def __init__(self, name, _handle=bark.handle, **kw):
        '''Initialise logger with identifying *name*.

        If you need to override the default handle then pass in a custom 
        *_handle*

        '''
        kw['name'] = name
        super(Logger, self).__init__(**kw)
        self._handle = _handle

    def log(self, message, **kw):
        '''Emit a :py:class:`~bark.log.Log` record.

        A copy of this logger's information is made and then merged with the
        passed in *kw* arguments before being emitted.

        '''
        log = copy.deepcopy(self)
        log.update(**kw)
        log['message'] = message

        self._handle(log)

