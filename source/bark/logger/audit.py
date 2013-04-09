# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import getpass
import time

from .base import Logger


class Audit(Logger):
    '''Add timestamp and username information automatically.'''

    def prepare(self, *args, **kw):
        '''Prepare and return a log for emission.'''
        log = super(Audit, self).prepare(*args, **kw)

        if not 'username' in log:
            log['username'] = getpass.getuser()

        if not 'timestamp' in log:
            log['timestamp'] = time.time()

        return log
