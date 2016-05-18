# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from __future__ import absolute_import

import os
import traceback

from .base import Logger


class Traceback(Logger):
    '''Support extracting traceback information automatically.'''

    def prepare(self, *args, **kw):
        '''Prepare and return a log for emission.

        If 'traceback' is present in *kw* arguments and is set to the value
        True then attempt to extract current traceback information and
        set as real value.

        .. warning::

            If no traceback could be extracted the traceback value will be
            the string 'None'.

        '''
        value = kw.get('traceback')
        if value is True:
            kw['traceback'] = traceback.format_exc().strip(os.linesep)

        return super(Traceback, self).prepare(*args, **kw)
