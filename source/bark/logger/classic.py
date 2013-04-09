# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .dynamic import Dynamic
from .traceback import Traceback
from .audit import Audit


class Classic(Dynamic, Traceback, Audit):
    '''Classic logger compatible with standard Python logger.'''

    def __init__(self, name, **kw):
        '''Initialise logger with identifying *name*.'''
        kw['name'] = name
        super(Classic, self).__init__(**kw)

    def prepare(self, message, **kw):
        '''Prepare and return a log for emission.'''
        kw['message'] = message
        return super(Classic, self).prepare(**kw)

    def log(self, message, **kw):
        '''Log a *message* with additional *kw* arguments.'''
        super(Classic, self).log(message, **kw)

    def debug(self, message, **kw):
        '''Log a debug level *message*.'''
        kw['level'] = 'debug'
        self.log(message, **kw)

    def info(self, message, **kw):
        '''Log an info level *message*.'''
        kw['level'] = 'info'
        self.log(message, **kw)

    def warning(self, message, **kw):
        '''Log a warning level *message*.'''
        kw['level'] = 'warning'
        self.log(message, **kw)

    def error(self, message, **kw):
        '''Log an error level *message*.'''
        kw['level'] = 'error'
        self.log(message, **kw)
