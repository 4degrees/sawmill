# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys
import tempfile
from datetime import datetime

import sawmill
from sawmill.handler.stream import Stream
from sawmill.filterer.level import Level
from sawmill.formatter.field import Field


def configure(level='info', filepath=None, *args, **kw):
    '''Configure the logging system in a classic manner.

    *level* will determine the minimum level to display on stderr. *filepath*
    can be used to set where the log file should be stored. It defaults to a
    temporary file named after the current date and time.

    '''
    stderr_handler = Stream(
        sys.stderr,
        filterer=Level(min=level, max=None),
        formatter=Field(keys=['level', 'name', 'message', 'traceback'],
                        template='{value}')
    )
    sawmill.root.handlers['stderr'] = stderr_handler

    if filepath is None:
        prefix = datetime.now().strftime('sawmill-%Y_%m_%d-%H_%M_%S-')
        _, filepath = tempfile.mkstemp(prefix=prefix, suffix='.log')

    file_descriptor = open(filepath, 'a')
    file_handler = Stream(
        file_descriptor,
        filterer=Level(min=None, max=None),
        formatter=Field(keys=['timestamp', 'level', 'name', 'message',
                              'traceback'])
    )
    sawmill.root.handlers['file'] = file_handler

