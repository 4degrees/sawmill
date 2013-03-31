# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Logger


class Classic(Logger):
    '''Classic logger compatible with standard Python logger.'''

    def __init__(self, name, **kw):
        '''Initialise logger with identifying *name*.'''
        kw['name'] = name
        super(Classic, self).__init__(**kw)

    def prepare(self, message, **kw):
        '''Emit a :py:class:`~bark.log.Log` record.

        A copy of this logger's information is made and then merged with the
        passed in *kw* arguments before being emitted.

        '''
        kw['message'] = message
        return super(Classic, self).prepare(**kw)

    def log(self, message, **kw):
        '''Log a *message* with additional *kw* arguments.'''
        super(Classic, self).log(message, **kw)
